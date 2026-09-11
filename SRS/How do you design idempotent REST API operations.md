<!--
reps: 0
priority: 0
-->
#API/REST #API/Idempotency #SRS

# How do you design idempotent REST API operations

> [!abstract] Short answer
> Treat idempotence as a per-operation contract: rely on method semantics where they exist (GET safe, PUT and DELETE idempotent by spec), add preconditions so repeated writes cannot double-apply, and give unsafe POSTs an idempotency-key protocol so client retries after timeouts are always safe. Document which calls are retryable and what a replay returns.

## Method semantics, then the gaps

The spec gives you the base table: GET, HEAD, OPTIONS, TRACE are safe; PUT and DELETE are idempotent — N identical requests have the effect of one — because their effect is defined by the target state, not by incrementing something. PUT naturally becomes upsert: sending the same representation twice lands the same state. DELETE repeated must stay terminal — deleting an already-deleted resource returns the same 204 or a documented 404, never a first-time success then an error. POST and PATCH carry no such guarantee, and networks make retries mandatory — a timeout after the server processed the request leaves the client ignorant, and the naive retry double-charges ([[What is idempotency in HTTP and in messaging]] for the shared semantics; [[What is the Idempotency-Key header used for in HTTP APIs]] for the header protocol; [[Why can Kafka retries break ordering without idempotence]] for the same problem in messaging). Conditional requests close another gap: PUT with If-Match turns lost updates into 412 instead of silent clobbering ([[How do you make REST API responses cacheable]] — same validator, write direction).

```text
server: key=k1 -> PROCESS (charge #1)
client: 201 {"charge":"c1","amount":1000}
server: key=k1 -> REPLAY (no second charge)
client: 201 {"charge":"c1","amount":1000}     <- same key, same response
server: key=k2 -> PROCESS (charge #2)
client: 201 {"charge":"c2","amount":1000}     <- new key, new operation
client: 400 {"error":"Idempotency-Key header required"}
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): the server stores key -> response and replays it; retries with the same key cannot double-charge, and a missing key is rejected up front (out/A02_IdempotencyKey.txt).

## The design discipline

Per endpoint, state three things in the contract: the effect of a repeat, the status a replay returns (the stored original response is the Stripe-style gold standard — the client cannot even tell it retried), and the retry rules (which statuses and errors are retryable, with backoff). Natural keys beat protocol where possible — a client-supplied request id or business key (order number) deduplicates at the application layer regardless of transport ([[How would you design a delete operation or endpoint]]'s terminal-state rule is the same discipline). On the server, make dedupe atomic: put-if-absent in a keyed store with a retention window, and reject key reuse with a different payload (409/422) — that mismatch is a client bug, not a retry ([[What are the key principles of good API design]] consistency; [[Which HTTP status codes matter most in REST API design]] for 409 versus 412). PATCH deserves honesty: it is not idempotent by definition (a relative patch re-applies), so either document it as such or define patches that converge to the same final state.

```d2
retry: client retry after timeout
q: method idempotent?
(GET/PUT/DELETE)
yes: resend safely
no: POST / PATCH
k: Idempotency-Key discipline?
same: same key -> stored response
replayed, no re-execution
new: new key -> second logical
operation (double charge!)
retry -> q
q -> yes
q -> no -> k
k -> same
k -> new
```

**Fig. 1.** The retry decision tree: method semantics or a key discipline decide whether a resend is safe.

> [!warning] Retrying non-idempotent calls "because the server is idempotent" is a category error
> Idempotence is a property of the operation's contract, not the server's mood. If the endpoint does not promise replay safety, a timeout retry can double-order, double-charge, or double-send — the client has no way to know the first attempt's fate.

> [!tip] Interview answer
> I start from method semantics: GET safe, PUT and DELETE idempotent with documented repeat behavior, PUT as upsert. For POST I add an idempotency-key protocol — server stores key to first response and replays it, key reuse with a different payload is rejected — and I use If-Match so writes conflict with 412 instead of clobbering. The contract states what a repeat returns and what is retryable; networks guarantee retries, so every write endpoint must answer for them.
