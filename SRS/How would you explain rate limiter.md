<!--
reps: 0
priority: 0
-->
#SystemDesign/Reliability #SRS

# How would you explain rate limiter

> [!abstract] Short answer
> A rate limiter caps how many operations a client (or key, or tenant) may perform per time window, rejecting or delaying the excess. The classic algorithms are token bucket (refill a bucket at a rate; each request takes a token — allows short bursts up to bucket size) and sliding window (count requests in the last N seconds — strict, no bursts). In distributed deployments the counters live in a shared store (Redis) with atomic Lua/compare-and-set updates, because limiter state must be shared and mutation must be atomic.

## The algorithms

Token bucket: a bucket holds up to `capacity` tokens and refills at `rate` tokens/second; a request takes one token or is rejected. It averages to the refill rate but allows bursts up to the capacity — friendly to real clients that legitimately send a burst then idle. Resilience4j's RateLimiter is exactly this: limitForPeriod tokens per limitRefreshPeriod, with a timeout for waiting on permission. Sliding window log: record each request's timestamp, count those within the window — exact, memory-hungry; sliding window counter interpolates between fixed windows as a cheap approximation. Fixed window is cheapest but fails at boundaries (a client can send 2x the limit across two half-windows). The choice is burst tolerance versus memory versus accuracy — Cloudflare's engineering writeup on counting rate limits walks exactly this tradeoff at fleet scale, where per-request exactness is unaffordable and approximations with local state win.

```java
// Resilience4j token bucket: 50 permits per 500 ns refresh period
RateLimiterConfig config = RateLimiterConfig.custom()
    .limitRefreshPeriod(Duration.ofNanos(500))
    .limitForPeriod(50)
    .timeoutDuration(Duration.ofSeconds(5))   // wait vs fail fast
    .build();
```

**Listing 1.** Token bucket configuration: rate (50/period), burst (capacity), and the waiting behavior on exhaustion.

## Making it distributed and deciding the response

A single-node limiter is trivial; the design questions start when many nodes share the limit. State must be centralized (Redis counters or sorted sets keyed by client) and updated atomically — a Lua script or native atomic operations make check-and-decrement one step, because a non-atomic read-then-write races under concurrency and lets clients exceed the limit. Sharded or per-node quotas (each node gets limit/N) avoid the round trip but over-accept when traffic skews. The response side is policy: reject with 429 and a Retry-After header, queue until a token frees (with a timeout), or degrade to a cheaper response; per-tenant tiers map to different buckets. Placement matters too — at the edge (API gateway/CDN) before expensive work, and client-side limiters ([[How do you protect a slower downstream service from overload]]) protect specific dependencies. [[When is a retry policy suitable for a command or API call]] pairs with it: rejected clients should back off, not retry hot.

> [!warning] A distributed limiter without atomicity is a suggestion
> Read-count-then-write in Redis is a race: two gateways read "49 left", both admit, the limit is exceeded. The check and the decrement must be one atomic operation (Lua script, single-threaded Redis command) — or the limiter only works on paper.

> [!tip] Interview answer
> A rate limiter caps operations per key per window: token bucket averages a rate with bounded bursts, sliding window enforces exactly. Distributedly, counters live in Redis and are decremented atomically via Lua; excess gets 429 with Retry-After or queues. I place it at the edge before expensive work, with per-tenant buckets tuned for burst tolerance.
