<!--
reps: 0
priority: 0
-->
#SystemDesign/Performance #Networking/Web/Protocols/HTTP #SRS

# How do you optimize a high traffic web service

> [!abstract] Short answer
> Optimization for high traffic is a pipeline of load reduction, in order of leverage: cache and offload before computing (CDN for static/media, caching for hot reads), make each request cheaper (indexes, N+1 removal, compression, connection reuse), scale horizontally behind a load balancer with stateless services, protect the core (rate limiting, timeouts, backpressure), and only then micro-optimize code — guided the whole way by latency percentiles and profiles, not guesses.

## Reduce work before making work faster

Every request you never compute is infinite optimization. Static assets, media and cacheable API responses move to a CDN/edge so origin load drops to misses ([[What is caching used for]]; the CDN is why media-heavy services' origins see a small fraction of user traffic). Application-level caching of hot reads (cache-aside with TTLs) cuts the database share — the hit-rate economics of [[How would you explain cache hit rate and cache miss rate]] decide whether it pays. Then make the surviving requests cheaper: database access fixes (missing indexes, N+1s, wide scans — the query toolkit of [[When a method is slow is the problem always in application code]]), payload trimming (gzip/brotli compression, pagination, field selection), and connection reuse (keep-alive, pooling) to amortize handshakes. These are measurable immediately in p95/p99; code micro-optimization is the last resort because it is the least leveraged layer.

## Scale out and protect the core

With per-request cost minimized, horizontal scaling multiplies it: stateless services ([[What is the difference between a stateful service and a stateless service]]) behind a load balancer with health checks and draining ([[How would you explain Health checks]], [[How would you explain Connection draining]]), sessions externalized or stateless tokens ([[How would you explain Sticky sessions]]), read replicas and/or sharding when the database becomes the bottleneck ([[How would you explain database replication strategies]], [[What problem does database sharding solve]]). Protection completes the design: rate limiting at the edge ([[How would you explain rate limiter]]), timeouts and bulkheads so one slow dependency cannot stall threads ([[How do you protect a slower downstream service from overload]]), async queues for work that does not need a synchronous answer, and load testing ([[What is load testing]]) to prove the ceiling before real traffic finds it. The measurement loop closes the pipeline: percentiles and saturation metrics per hop ([[How do you monitor an application with Spring Boot Actuator]]-style), capacity reviews before launches, and an SLO-driven error budget deciding when to stop optimizing ([[How would you explain common principles for scaling software systems]] generalizes the ladder).

```text
leverage ladder (do top-down):
1. offload:   CDN/static+media, cache hot reads      (remove requests)
2. cheaper:   indexes, N+1, compression, pooling     (per-request cost)
3. multiply:  stateless + LB + replicas/sharding     (horizontal scale)
4. protect:   rate limit, timeouts, bulkheads, async (survive the peak)
5. micro-opt: only measured, last                    (code-level)
```

**Listing 1.** The optimization ladder, highest leverage first.

> [!warning] Scaling out a per-request cost you never measured
> Adding ten replicas to a service whose p99 is a full-table scan buys ten copies of the same slow query plus ten replicas' load on the same database. Fix the per-request cost first — horizontal scaling multiplies whatever it is given, including waste.

> [!tip] Interview answer
> I optimize in leverage order: offload what I can (CDN, caching), make each remaining request cheap (indexes, N+1, compression, pooling), scale horizontally with stateless services and a load balancer, protect the core with rate limits, timeouts and backpressure — and validate with load tests and percentile metrics before and after. Code micro-optimization comes last, guided by profiles.
