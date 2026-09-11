<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> The response envelope has two top-level keys: `data` and `errors`. The `errors` array holds one entry per failed field or invalid request; each entry carries `message` (required), `locations` (line/column in the document), `path` (where in the response this failure happened), and optionally `extensions` (a server-defined map, e.g. `classification` or error codes). `data` and `errors` coexist — a partially failed request returns both, which is the definition of a partial response.

## Anatomy of one entry

The spec fixes only the shape, not the vocabulary: `message` is the only required field; `locations` points into the request document; `path` mirrors the response structure so clients can bind failures to result positions — `["user", "friends", 1, "name"]` means the second friend's name. Everything custom travels in `extensions`, the sanctioned place for machine-readable codes, retry hints, or classification ([[Why does GraphQL often return HTTP 200 when a field errors]]).

```java
// graphql-java 26.1: two root fields, "ok" succeeds, "failing" throws IllegalStateException.
// { ok failing } ->
// {"errors":[{"message":"Exception while fetching data (/failing) : boom: secret stack detail",
//   "locations":[{"line":1,"column":6}],"path":["failing"],
//   "extensions":{"classification":"DataFetchingException"}}],
//  "data":null}
// error entry keys: [message, locations, path, extensions]
```

**Listing 1.** Verified on graphql-java 26.1. The default handler kept the exception message but hid the class name — and because `failing` was non-null, the null bubbled and `data` was lost entirely ([[How does null bubbling work when a GraphQL field is null]]).

Validation errors look different in one respect: they fail before execution, so they carry `locations` but **no `path`** and no `data` key at all — `{"message":"Validation error (MissingFieldArgument@[character]) : Missing field argument 'id'","locations":[{"line":1,"column":3}],"extensions":{"classification":"ValidationError"}}` ([[How do you pass arguments to a GraphQL field]]).

```d2
direction: down
Req: "one request" { width: 160; height: 50 }
OK: "resolved fields\ndata" { width: 230; height: 60 }
F: "failed fields\nerrors[]" { width: 210; height: 60 }
E: "message (required)\nlocations, path, extensions" { width: 330; height: 70 }
Partial: "data + errors together\n= partial response" { width: 300; height: 65 }
Req -> OK
Req -> F
F -> E
OK -> Partial
F -> Partial
```

**Fig. 1.** Errors are field-scoped entries, not a global failure flag; the envelope mixes successes and failures in one response.

> [!warning] Error messages are an information-disclosure surface
> Three practical rules. First: exception details leak by default — stack traces, SQL fragments, or internal hostnames in `message` are a real vulnerability class; production servers should map exceptions to stable codes in `extensions` and keep details in logs ([[How do you authenticate and authorize a GraphQL request]]). Second: do not invent your own top-level keys next to `data` and `errors` — transport-level clients assume the spec envelope; put anything custom under `extensions` ([[What is GraphQL introspection]]). Third: `errors` is not a logging system — per-field entries multiply on large selections, so retry logic based on error entries must read `path` and `extensions`, not string-match messages.

Design guidance for senior interviews: define an error taxonomy per API (domain errors as `extensions.code`, e.g. `NOT_FOUND`, `FORBIDDEN`), keep `path`-based binding for list positions, and consider the "payload with `userErrors`" pattern for mutations whose failures are business-as-usual rather than exceptional ([[Why do GraphQL mutations use input types instead of object types]]).

> [!tip] Interview answer
> The errors array is half of the response envelope: field-scoped entries with message, locations, path, and a free-form extensions map. Data and errors coexist — partial success is the normal case. Validation errors have no path because nothing executed; resolver errors carry the response path where the failure happened. Keep secrets out of messages, encode machine-readable info in extensions, and let path bind failures for clients.

