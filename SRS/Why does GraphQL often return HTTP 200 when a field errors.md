<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Because GraphQL separates **transport** from **execution**: a request that parses and validates but has field-level failures is a *successful HTTP delivery* of a partially failed operation. The HTTP status describes the request/response exchange; the GraphQL envelope describes operation outcomes — `data` plus `errors`. Field errors therefore routinely arrive with HTTP 200. Statuses regain meaning at the transport edges: malformed JSON, missing document, or unsupported media types are transport errors, and a server may map request-level failures to 4xx.

## What the separation buys — and what it costs

The value: one operation can succeed field-by-field — `data` holds resolved fields while `errors` lists the failed ones, and clients render what they got. A single HTTP-level status cannot express "7 of 9 fields are fine", so the envelope does, and partial-response handling becomes uniform across every server and transport ([[What does the GraphQL errors array contain]]).

The cost: naive tooling breaks. Monitoring that alerts on 5xx misses GraphQL failures delivered with 200; generic HTTP clients with "status == success" logic swallow field errors; caches may treat a 200 with errors as cacheable content ([[Why is HTTP caching harder with GraphQL than REST]]). Production setups therefore inspect the envelope: success means `errors` absent or empty — status alone never means success.

```java
// graphql-java 26.1: { publicInfo salary } with anonymous role context.
// The salary resolver threw a forbidden error; publicInfo resolved fine.
// HTTP 200 with body:
// {"errors":[{"message":"Exception while fetching data (/salary) : salary requires role=hr",
//   "path":["salary"],"extensions":{"code":"FORBIDDEN","classification":"DataFetchingException"}}],
//  "data":null}
```

**Listing 1.** Verified on graphql-java 26.1. A field-level authorization failure produced a well-formed GraphQL error — the transport delivery itself succeeded, which is why the status stays 200 on most servers ([[How do you authenticate and authorize a GraphQL request]]).

```d2
direction: down
H: "HTTP layer\nstatus = delivery semantics" { width: 280; height: 65 }
G: "GraphQL layer\ndata + errors = operation semantics" { width: 320; height: 65 }
F: "field error" { width: 160; height: 50 }
Ok: "200 + errors in envelope" { width: 250; height: 60 }
T: "transport failure\n(malformed request)" { width: 250; height: 60 }
B: "4xx / 5xx possible" { width: 200; height: 50 }
H -> G: "body"
F -> Ok
T -> B
```

**Fig. 1.** Two layers, two verdicts: HTTP judges delivery; the envelope judges execution. Field errors live in the second layer, so the first can still say 200.

> [!warning] "Always 200" is a folklore overstatement
> The correction interviewers probe for: GraphQL-over-HTTP specifications describe when non-200 responses are appropriate. A request that is not valid GraphQL at all (unparseable JSON, missing `query`) never reaches execution and may be a 400; server-side infrastructure failures are ordinary 5xx; and some servers deliberately map application errors to 4xx/5xx — an implementation choice, not a spec violation by itself ([[What is the difference between a GraphQL query a mutation and a subscription]]). The honest formulation: field errors are *usually* delivered with 200 because the envelope, not the status, is their channel — not that HTTP status is meaningless for GraphQL APIs ([[Why is rate limiting harder in GraphQL than REST]]).

One more nuance: response media types (`application/json` vs `application/graphql-response+json`) sharpen this — the response type signals whether the status reflects application-level success, so a client can opt into stricter status semantics without abandoning the envelope ([[What is GraphQL introspection]]).

> [!tip] Interview answer
> GraphQL puts execution outcomes in the envelope — data plus errors — and treats HTTP as delivery, so per-field failures ride in a 200 body: partial success is one response with both keys. But "always 200" is folklore: transport-level problems (malformed request, unsupported content type) and infra failures can produce 4xx/5xx. Clients must treat "no errors array" as success, never the status code alone.

