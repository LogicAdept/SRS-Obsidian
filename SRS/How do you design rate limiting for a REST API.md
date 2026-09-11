<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# How do you design rate limiting for a REST API

> [!abstract] Short answer
> Decide the quota per caller (per API key, token, or IP), enforce it with a token-bucket or windowed counter at the gateway or service edge, and communicate it: 429 Too Many Requests with Retry-After when the quota is gone, plus headers for limit, remaining, and reset so well-behaved clients throttle themselves before the wall.

## Enforcement and the contract

The algorithm choice is a classic systems question — fixed window (simple, bursty at boundaries), sliding window, token bucket / leaky bucket (smooths bursts, the usual default; [[How would you explain rate limiter]] covers it) — but the API design questions are orthogonal: where (edge gateway so limits are visible and cheap, or in-service for per-tenant nuance), keyed on what (API key first, user id, then IP as fallback with its NAT caveats), and what happens at the limit. The contract: 429 with Retry-After (seconds or HTTP-date), plus quota headers — the de-facto X-RateLimit-Limit/Remaining/Reset or the newer RateLimit-Limit/Remaining/Reset draft fields — on responses while things are healthy, not only after the cutoff, so clients can pace themselves. Distributed enforcement needs a shared counter store (Redis-style) or per-node partitioning; per-node counters silently multiply your real quota by node count ([[What is the API gateway pattern in microservices]] for where the edge lives).

```text
client #1: 200 remaining=2 {"results":["hit"]}
client #2: 200 remaining=1 {"results":["hit"]}
client #3: 200 remaining=0 {"results":["hit"]}
client #4: 429 remaining=0 retryAfter=30 {"error":"rate limit exceeded"}
client #5: 429 remaining=0 retryAfter=30 {"error":"rate limit exceeded"}
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): a fixed-window limiter exposing RateLimit-Remaining on every response and 429 with Retry-After once the window quota is gone (out/A08_RateLimit.txt).

```d2
c: client
gw: edge limiter {
  b: token bucket
(refills r/sec)
}
up: upstream service
c -> gw: request (consumes 1 token)
gw -> up: tokens available -> 200
+ RateLimit-Remaining
gw -> c: quota gone -> 429
+ Retry-After: 30
```

**Fig. 1.** The limiter sits at the edge; requests either consume a token and proceed, or bounce as 429 with a retry hint.

## Design decisions beyond the happy path

Publish limits in documentation and in headers, not as folklore; differentiate classes (free tier versus paid, cheap reads versus expensive reports) and endpoints rather than one global number. Decide the over-limit behavior deliberately: 429 for API callers, but abuse cases may need 403 or account-level action. Distinguish rate limiting from throttling/load-shedding (deliberate slowdowns and priority dropping at overload — [[How do you protect a slower downstream service from overload]]), from GraphQL's per-query cost accounting ([[Why is rate limiting harder in GraphQL than REST]] — a single request's cost varies, so the quota unit becomes complexity, not count), and from circuit breakers ([[How does Resilience4j circuit breaker work with Spring]] — client-side protection, whereas rate limiting is provider-side). 503 with Retry-After is the overload story, 429 the quota story — keep them distinct.

> [!warning] Per-node counters are the silent multipler
> A naive in-memory counter per instance with N replicas behind the balancer enforces N times the intended quota, and the effective limit drifts with autoscaling. Quota state must live in a shared store or be partitioned deliberately by key.

> [!tip] Interview answer
> I enforce quotas at the edge, keyed by API key or user, usually with a token bucket over a shared counter store, and I publish the budget: limit, remaining, and reset headers on healthy responses, 429 with Retry-After at the wall. Limits differ per tier and per endpoint cost. I keep 429 for quota, 503 for overload, and I know per-node counters multiply the real limit by replica count.
