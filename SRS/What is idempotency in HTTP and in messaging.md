<!--
reps: 0
priority: 0
-->
#API/Idempotency #Messaging #Networking/Web/Protocols/HTTP #SRS

# What is idempotency in HTTP and in messaging

> [!abstract] Short answer
> An operation is idempotent when performing it once or N times leaves the same result: f(f(x)) = f(x). HTTP builds it into methods — GET, HEAD, OPTIONS, TRACE are safe, PUT and DELETE are idempotent — while POST and PATCH are not. In messaging, at-least-once delivery makes the consumer's idempotence mandatory: duplicate delivery is a fact, so processing must converge to the same state.

## Why the distinction carries systems

The point is not purity, it is retry safety: any distributed interaction can time out after the work happened, so the caller's retry is only safe if repeating the operation cannot double-apply it. HTTP encodes the guarantee in method semantics so clients know what may be resent blindly — and servers keep the promise in surprising places: repeated DELETE must stay terminal (204 or a documented 404, never "first success then error"), repeated PUT re-lands the same state (upsert semantics), and a repeated ranged GET returns the same window ([[Can a GET request include a body]] for a related spec subtlety; [[Which common HTTP methods are not idempotent]] for the method-level view). POST breaks the model — "create order" twice creates two orders — which is why systems add the Idempotency-Key protocol on top ([[What is the Idempotency-Key header used for in HTTP APIs]]) and why conditional requests (If-Match) turn blind writes into guarded ones ([[How do you design idempotent REST API operations]]).

```d2
f: f(f(x)) = f(x)
http: HTTP methods {
  safe: GET HEAD OPTIONS TRACE
  idem: PUT DELETE (safe to repeat)
  not: POST PATCH (retry = risk)
}
msg: messaging {
  al: at-least-once delivery
(duplicates guaranteed)
  con: consumer dedupe:
message id / version /
natural key
}
goal: safe retries everywhere
http -> goal
msg -> goal
```

**Fig. 1.** The same equation serves two stacks: HTTP method semantics on the wire, consumer-side dedupe under at-least-once delivery.

## The messaging half

Brokers promise at-least-once because exactly-once delivery across failures is either impossible or expensive to prove; the consumer therefore sees duplicates as a certainty, not an anomaly. The defense is application-level: key processing by a stable business identity (order id, message id, a version number for state-machine updates) and make the state change converge — check-then-act under a transaction, conditional writes, or a dedupe table holding processed ids ([[What is the Idempotent Receiver pattern]] names the pattern; [[Why must RabbitMQ consumers be idempotent]] and [[What are at-most-once at-least-once and exactly-once semantics in Kafka]] ground it per broker; [[What is an idempotent Kafka producer for]] and [[Why can Kafka retries break ordering without idempotence]] show the producer side of the same equation). Exactly-once processing exists only as an engineered composite — transactional producers, dedupe stores, outbox patterns — never as a checkbox ([[What is the difference between Kafka delivery guarantees and application exactly-once]] for the boundary). The unified lesson for interviews: idempotence is a property you design into an operation's contract so that retries — inevitable in both HTTP and messaging — are safe.

```text
safe         : GET, HEAD, OPTIONS, TRACE           (read-only)
idempotent   : PUT, DELETE                         (repeat -> same state)
not by spec  : POST, PATCH                         (repeat may double-apply)
messaging    : at-least-once delivery -> consumer dedupes by id,
               state changes converge; exactly-once = engineered composite
```

**Listing 1.** The idempotence map: protocol-guaranteed methods, the unsafe pair, and the messaging consequence (conceptual, per RFC 9110 method semantics).

> [!warning] "Exactly-once delivery" is marketing; exactly-once processing is engineering
> No broker makes the network deliver exactly once. The achievable goal is exactly-once effects: duplicates may arrive, but dedupe plus convergent state changes make them vanish. Candidates who repeat the marketing phrase at interview lose standing fast.

> [!tip] Interview answer
> Idempotence means N repetitions equal one application — f(f(x)) = f(x). HTTP builds it into methods: GET is safe, PUT and DELETE idempotent, POST and PATCH not, which is why retries against unsafe methods need keys or preconditions. In messaging, at-least-once delivery guarantees duplicates, so consumers must be idempotent by design: dedupe on message or business id, converge state changes, and treat exactly-once as an engineered outcome of transactional writes and dedupe stores — never as a delivery promise.
