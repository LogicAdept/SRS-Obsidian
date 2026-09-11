<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# How do you represent non-CRUD actions in a REST API

> [!abstract] Short answer
> Three standard moves: model the action as a resource (POST /orders/7/cancellation creates a Cancellation), use a custom verb method on the resource (POST /orders/7:cancel, the Google AIP custom-method convention), or reframe the action as a state transition via PATCH to a status field. Never abuse GET for state changes, and keep the choice consistent across the API.

## Choosing between the three shapes

The action-as-resource shape fits when the action has its own lifecycle data — a cancellation has reason, timestamp, actor, maybe a refund trail — and becomes addressable: POST /orders/7/cancellation returns 201 with Location /orders/7/cancellations/99, and auditors can later GET that cancellation. The custom method (POST /orders/7:cancel) fits verbs that genuinely have no artifact: an explicit Google AIP convention using a colon-suffixed verb, which keeps HTTP semantics honest (POST, not GET), documents the boundary of the uniform interface, and stays greppable in codegen and logs. The state-transition shape fits when the action is only a field flip with validation: PATCH /orders/7 with {"status":"CANCELLED"} — the state machine lives in validation rules. Same effect in all three; the decision hinges on whether the action produces data worth addressing, whether the domain is verb-shaped, and what your docs and SDKs must explain ([[What are the key principles of good API design]]; [[What is a resource in a RESTful context]] for when something is a resource at all).

```text
GET state: {"id":7,"status":"NEW"}
server: POST /orders/7/cancellation -> 201 (state=CANCELLED)
GET state: {"id":7,"status":"CANCELLED"}
server: POST /orders/7:cancel -> 200 (state=CANCELLED)
GET state: {"id":7,"status":"CANCELLED"}
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): both shapes flip the same state — the action-resource additionally returns 201 with a Location for the created artifact (out/A09_NonCrud.txt).

```d2
o: order /orders/7
a1: action as resource {
  x: POST /orders/7/cancellation
-> 201 Cancellation #99
}
a2: custom method {
  x: POST /orders/7:cancel
-> 200
}
a3: state transition {
  x: PATCH status=CANCELLED
-> 200
}
o -> a1: has artifact + lifecycle
o -> a2: pure verb, no artifact
o -> a3: just a validated field flip
```

**Fig. 1.** The decision tree: artifact, verb, or field flip — all uniform-POST-based, never GET.

## The forbidden moves and the gray zones

GET /orders/7/cancel is the classic anti-pattern: GET must be safe, so caches, prefetchers, and link checkers would cancel orders. RPC-in-URL paths like /api/cancelOrder with a body-id (verb in the path, identifier in the body) abandon resource addressing entirely and sink you to maturity level 0 ([[What does RESTful mean compared with REST]]). Batch operations surface the same question at the collection level — POST /orders/batch-cancellation as an action resource, or the AIP batch custom method — with 207-style partial outcomes needing their own contract ([[How do you design idempotent REST API operations]] because batch retries multiply). Search endpoints (POST /products/search) are the read-side special case: a body too big for a URL justifies POST without state change — a documented, conscious exception ([[How do you design filtering and sorting for a REST API]] for when query strings suffice).

> [!warning] The colon convention is a convention
> /orders/7:cancel is not in any RFC — it is Google's API design guide style (AIP-136), adopted widely but not universal. State whose convention you follow; do not present the syntax as standard HTTP, and expect proxies and caches to treat it as a normal opaque path.

> [!tip] Interview answer
> I have three shapes: model the action as a resource when it leaves an artifact — POST /orders/7/cancellation gives me 201, a Location, and an auditable Cancellation; use a custom verb method like POST /orders/7:cancel when the action has no artifact, following the AIP convention; or PATCH a status field when it is only a validated transition. GET never changes state, and I keep the choice consistent and documented across the API.
