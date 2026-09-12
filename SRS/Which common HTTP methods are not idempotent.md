<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #SRS
# Which common HTTP methods are not idempotent

> [!abstract] Short answer
> POST is the core method that is not idempotent — each repeat performs the processing again. PATCH is also not guaranteed idempotent: RFC 5789 leaves it to the patch document's semantics. CONNECT is non-idempotent as well. Everything else in the RFC 9110 core set — GET, HEAD, OPTIONS, TRACE, PUT, DELETE — is idempotent (and the first four are additionally safe).

## The property check, method by method

| Method | Idempotent? | Why |
|---|---|---|
| GET / HEAD | yes | reads; repeating returns the same representation (modulo time) |
| OPTIONS / TRACE | yes | capability query / loopback echo |
| PUT | yes | full replacement: state after N repeats equals state after 1 |
| DELETE | yes | first call removes; repeats hit an already-gone resource (404/204) — no *further* change |
| **POST** | **no** | "process this": each repeat may create another entity, resend a mail, charge a card |
| **PATCH** | **not guaranteed** | `{ "qty": 3 }` is idempotent; a delta like `{ "qty": "+1" }` is not |
| **CONNECT** | no | establishes a tunnel; repeating opens another tunnel |

```d2
direction: down
ok: "Retryable after timeout\nGET, HEAD, OPTIONS, TRACE, PUT, DELETE" { width: 360; height: 90; style.fill: "#e8f5e9" }
no: "Retry needs protection\nPOST (Idempotency-Key),\nPATCH (payload-dependent)" { width: 360; height: 100; style.fill: "#ffebee" }
ok -> no: "the dividing line in retry logic"
```

**Fig. 1.** Retry-safety is the practical meaning of idempotency — it decides what a client may auto-repeat.

## Why the distinction pays rent

1. **Client retry logic.** After a timeout on PUT/DELETE, the client can safely retry; on POST it cannot — unless the API adds an idempotency key that the server deduplicates ([[What is idempotency in HTTP and in messaging]]).
2. **Proxies and infrastructure.** Intermediaries treat methods differently (caching GET; not replaying POST), and connection-loss recovery depends on the declared semantics.
3. **Correct API design.** Making operations idempotent where possible (PUT-like upserts, DELETE-like cancels by id) is how distributed systems survive duplicated messages ([[How do you prevent duplicate message or packet delivery]]).

> [!warning] "DELETE is idempotent" does not mean "DELETE twice is two 404s"
> The spec's wording: repeating leaves the same *state effect* — the resource stays removed; the response code may differ (200 then 404, or a server may return 204 both times by keeping tombstones). Conversely, "PATCH is idempotent when it sets a value" has a concurrency caveat: two *different* clients patching interleaved is a different question from one client repeating ([[What is the difference between POST PUT and PATCH]] carries the trio's full comparison). And a rare follow-up: methods are defined idempotent *by spec*, but a buggy handler that increments a counter on every GET violates the contract — the property is about declared semantics, not accidental behavior.

Family context: [[What are the HTTP request methods]], [[What is the difference between GET and POST]], [[What is HTTP]].

> [!tip] Interview answer
> POST — the headline non-idempotent method; PATCH — only conditionally, depending on the patch document; CONNECT — also not. Everything else (GET, HEAD, OPTIONS, TRACE, PUT, DELETE) is idempotent by RFC 9110. The consequence I lead with: retry logic — clients may auto-retry idempotent calls, while POST needs an Idempotency-Key or similar dedup, and DELETE repeats may still differ in status codes while having no further state effect.
