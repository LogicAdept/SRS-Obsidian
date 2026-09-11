<!--
reps: 0
priority: 0
-->
#SystemDesign/Reliability #SRS

# How do you protect a slower downstream service from overload

> [!abstract] Short answer
> Slowing down is how services fail, so protection is about giving the slow dependency less work, not more: rate-limit what you send it (throttling), bound concurrent calls with a bulkhead, shed or fail fast when it is unhealthy (circuit breaker, load shedding), decouple via a queue so it consumes at its own pace, and retry with backoff and jitter — never blind retries, which multiply load exactly when the dependency is weakest.

## The toolkit, per failure mode

A downstream that serves 200 TPS while callers can send 1000 TPS needs its callers to cap themselves. Client-side rate limiting (a token-bucket per downstream, as in Resilience4j's RateLimiter with limitForPeriod/limitRefreshPeriod) caps the offered load. A bulkhead bounds concurrency — a semaphore cap like Resilience4j's maxConcurrentCalls (default 25) — so stalls in one downstream cannot consume every thread and cascade to unrelated calls. The circuit breaker ([[How would you explain Circuit Breaker]], with the Spring wiring in [[How does Resilience4j circuit breaker work with Spring]]) stops sending traffic entirely once failure or slow-call rates cross threshold, letting the dependency drain its queue. Load shedding is the server-side twin: the slow service itself rejects or degrades excess traffic based on SLOs — the Google SRE approach of redirecting or serving degraded results rather than dying. When delivery can be asynchronous, a queue between the services is the strongest answer: the producer writes at full speed and the slow consumer processes at its own rate — queue-based load leveling; the trade is latency and the new question of queue overflow.

```text
protect B (200 TPS) from A (1000 TPS):
  sync path : rate limit on A's client -> bulkhead -> circuit breaker
  async path: A -> queue -> B consumes at 200 TPS   (levels the load)
  on B's side: load shedding by SLO, degrade or reject excess
never: retry immediately at full rate (amplifies the overload)
```

**Listing 1.** The protection stack for a slow dependency, sync and async.

## Combining and ordering

The patterns compose in a deliberate order on the caller: rate limit (shape the offered load) → bulkhead (isolate the resource) → circuit breaker (stop when it is unhealthy) → retry with exponential backoff and jitter on transient errors only, honoring Retry-After headers — Azure's retry guidance stresses that retries without idempotency checks and backoff multiply load. Timeouts bound every call so a hung dependency cannot hold resources; they are sized against the dependency's normal latency, not generous defaults. The decision between sync protection and an async queue follows the semantics: commands that must be durable go through the queue; interactive reads need rate limiting, bulkheads and graceful degradation (cached or partial responses). [[When is a retry policy suitable for a command or API call]] details the retry leg, [[How do you handle a two second network outage]] the failure drill.

> [!warning] Retries are load multipliers during incidents
> Ten callers retrying a struggling dependency three times turn 1x load into up to 4x — the retry storm. Retry budgets, exponential backoff with jitter, honoring Retry-After, and stopping at the circuit breaker are what keep a hiccup from becoming an outage.

> [!tip] Interview answer
> I protect a slow downstream by reducing what it sees: client-side rate limiting and bulkheads cap the offered load, a circuit breaker stops traffic when it degrades, and for async-able work a queue levels the load to its real capacity. On its side it sheds load against SLOs. Retries only with backoff, jitter and idempotency — never full-rate retries during degradation.
