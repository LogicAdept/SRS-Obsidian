<!--
reps: 0
priority: 0
-->
#SystemDesign/Reliability #SRS

# How do you handle a two second network outage

> [!abstract] Short answer
> A two-second blip is the standard drill: time out fast (do not wait minutes on dead connections), retry idempotent operations with exponential backoff and jitter so clients do not sync up, use an idempotency key so a retry after an ambiguous response cannot create a duplicate, fail over or fail fast through a circuit breaker, and degrade gracefully — serve cached or reduced results while the dependency is unreachable. The design goal: the blip costs latency, not correctness or an outage.

## The second-by-second mechanics

During the blip, in-flight requests face three fates: they died before reaching the peer (safe to retry), they were processed but the response was lost (retry must be idempotent — the operation may have committed), or the connection hangs (the timeout converts a hang into a retryable error). That is why timeouts exist on every hop and why retries without idempotency are dangerous: a payment retried after an ambiguous response double-charges. The standard tooling is an idempotency key — Stripe's API pattern: the client sends a unique key per logical operation; the server stores the first response under that key (Stripe retains keys 24 hours) and replays it for retries instead of re-executing. Backoff spreads retries over time (exponential with a cap), jitter randomizes them so a thousand clients that failed together do not hammer together — Azure's transient-fault guidance treats jitter as the default, not an extra. [[What is idempotency in HTTP and in messaging]] grounds the idempotency vocabulary.

```text
t=0.0s blip starts: in-flight calls error or hang
        -> timeout (e.g. 1-5s) converts hangs to errors
t=0.1s retries with backoff+jitter: 100ms, 200ms, 400ms ... (capped)
        -> only with idempotency key or idempotent method
t=0.5s circuit breaker notices failure burst -> HALF-OPEN probes
t=2.0s network returns: probes succeed -> CLOSED, backlog drains
user impact: a few hundred ms of latency, fallbacks served — no dupes
```

**Listing 1.** The drill: timeout, backoff+jitter, idempotent retries, breaker, recovery.

## Designing for the next blip

The two-second case is survivable precisely because it is short — but the design that survives it is the same one that survives worse: retries bounded and idempotent, circuit breakers probing instead of flooding, fallbacks that keep the user moving (cached data, queue-and-continue for commands, degraded read-only mode). What turns a blip into an outage is amplification: full-rate retries, no timeouts on hung sockets, and non-idempotent mutations retried blind. The circuit breaker's states and thresholds are the mechanism for not amplifying ([[How would you explain Circuit Breaker]]), and the protection stack that keeps the dependency itself from collapsing when the backlog arrives is in [[How do you protect a slower downstream service from overload]]. For messaging, the same drill is consumer-visible as redelivery: process idempotently or deduplicate, because at-least-once delivery means the "blip" reaches you as a repeated message.

> [!warning] An ambiguous response is not a failed operation
> If the request may have reached the server, "retry" can mean "execute twice". The only safe retry is an idempotent one — by method semantics (GET, PUT with fixed id) or by an idempotency key the server deduplicates. Retrying a payment without a key is not resilience, it is a second payment.

> [!tip] Interview answer
> Short outages are handled by timeout-convert-hangs, idempotent retries with exponential backoff and jitter, and idempotency keys so ambiguous responses cannot duplicate effects. A circuit breaker stops amplification and probes recovery; users see cached or degraded responses. The two seconds cost latency — the design goal is that they cost nothing else.
