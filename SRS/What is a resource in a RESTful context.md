<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is a resource in a RESTful context

> [!abstract] Short answer
> A resource is the conceptual target of a hyperlink — anything a system chooses to identify with a URI: a document, a collection, a process result, a time-varying entity. Clients never touch the stored object itself; they exchange representations (JSON, XML) of its current or intended state. Resource identification is the first component of the uniform interface.

## Concept, not database row

Fielding's definition is deliberate: a resource is "the intended conceptual target", not a piece of stored data. /orders/7 identifies the order as a concept; the representation returned today may differ from yesterday's (time-varying), and the same concept can be rendered as JSON or PDF depending on negotiation. Two design corollaries follow. First, URIs name nouns — things — while verbs live in the uniform method set; an operation that resists noun modeling (cancel, approve) usually means you have found another resource hiding inside the flow: a cancellation, an approval ([[How do you represent non-CRUD actions in a REST API]]). Second, collections are resources too: /orders has its own identity, supports GET (list, filtered) and POST (append), and its members are addressed beneath it. A URI is an identifier, not an address of a file — opaque to clients, meaningful to the server ([[What is an API endpoint]] for the addressing mechanics).

```d2
c: conceptual target
(the order #7)
uri: /orders/7 {
  shape: text
}
rep1: representation now
{ "status": "NEW", ... }
rep2: representation later
{ "status": "PAID", ... }
c <- uri: identifies
uri -> rep1: GET returns
current state
uri <- rep2: PUT replaces
intended state
```

**Fig. 1.** The URI identifies the concept; representations carry its state at different times, in negotiable formats.

## What resources are not

A resource is not the Java object, the database row, or the file on disk — coupling the URI to storage layout ("GET /tables/users/rows/7") leaks internals and kills evolvability, because renaming a column would break client-facing identity. It is also not a remote procedure: a URI like /users/7/delete names an action, not a thing, and forfeits the uniform interface's safety and idempotence guarantees — DELETE /users/7 states the intent within the method's own semantics. The test interviewers probe: "is customer balance a resource?" It can be — /accounts/42/balance is a legitimately addressable, cacheable sub-resource if clients need to track it — but often it is better as part of the account representation, since splitting into resources multiplies round-trips ([[What are the key principles of good API design]] naming trade-offs; [[What is content negotiation in REST APIs]] for representations of the same resource).

```text
GET /orders/7  Accept: application/json
  -> 200 {"id":7,"status":"NEW"}       (representation now)

GET /orders/7  Accept: text/csv
  -> 200 "id,status
7,NEW"          (same resource, other representation)

PUT /orders/7  {"status":"PAID"}
  -> 204                               (intended state replaced; next GET reflects it)
```

**Listing 1.** One URI, negotiable representations, state replaced via PUT — the resource is the concept, never the stored row (verified on JDK 21, out/A01, out/A04).

> [!warning] The resource is not the representation
> Clients reason about JSON payloads; servers may store rows, snapshots, or projections. The contract only fixes the representation. Assuming the JSON shape equals the storage shape couples clients to internals — the classic cause of painful API migrations later.

> [!tip] Interview answer
> A resource is the conceptual thing a URI identifies — a document, a collection, even a time-varying entity — never the storage object behind it. Clients exchange representations of its state: GET to read, PUT to replace intent, DELETE to remove. Good API design keeps URIs as opaque nouns, pushes verbs into the uniform method set or models actions as their own resources, and treats collections as resources in their own right.
