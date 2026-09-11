<!--
reps: 0
priority: 0
-->
#Debugging #Observability #SystemDesign/Performance #SRS

# How to find where a slow method actually spends its time

> [!abstract] Short answer
> No — a slow method is usually not slow because of its own code: the method is the container that waits. Profile first and split the wall time into segments: database queries (the most common culprit — N+1, missing indexes, wide scans), remote calls (HTTP/RPC to slower services), locks and synchronization, IO (files, queues), and only then CPU work in the method itself. Measure before optimizing — and ask whether the operation should be faster or should not run at all.

## The segmentation method

Wall time of a method = its own CPU work + everything it waits for. The first measurement splits those. Distributed tracing and profilers (continuous or sampled) attribute time to spans: a method taking 700 ms where 500 ms is a database call and 150 ms is an HTTP call to a third party leaves 50 ms of actual code — optimizing the loop there is noise. The database share decomposes further: an N+1 pattern (one query per item in a loop), missing or unusable indexes ([[What is a database index and why does it speed up queries]], [[What is sargability in SQL]]), or a single query needing an index or a rewrite — the vault's query-debugging cards ([[How do you identify slow or non-performant SQL queries]], [[How do you debug a slow PostgreSQL query]], [[How do you debug a slow ClickHouse query]]) are the concrete toolkit per engine. The remote-call share suggests caching ([[When is caching useful and when is it dangerous]]), parallelizing independent calls, or timeouts on the slow dependency; the lock share suggests contention analysis. The business question comes first, though: is 15 seconds for a 15 MB CSV wrong, or is that the acceptable contract? A requirement question answered by measurement, not by instinct.

```text
method wall time: 700ms
  |- DB:   500ms  (N+1: 1 + 50 queries; idx missing on orders.user_id)
  |- HTTP: 150ms  (sync call to pricing-service)
  |- CPU:    50ms (the loop everyone was about to "optimize")
priority: fix N+1 / add index (500ms) -> parallelize or cache HTTP (150ms)
          -> only then touch the loop (50ms)
```

**Listing 1.** Attributing wall time before optimizing anything.

## Why "always app code" is false at system level

The code may be innocent at every layer: the database host is undersized, a dependency is degraded, the connection pool is saturated by another feature, GC pauses steal the thread, the network is lossy, or cold caches ([[What difficulties arise when working with caching]]) make every request pay first-touch costs. That is why the diagnosis chain is: SLO metrics and traces localize the slow segment ([[How do you monitor an application with Spring Boot Actuator]]-style dashboards for trends), the segment's owner debugs it (query plan, dependency latency, pool stats), and the fix is verified by re-measurement — latency wins claimed without a before/after distribution are anecdotes. The scalable habit: latency budgets per segment so regressions localize themselves. When the slow path is inherent — genuinely heavy computation — the answers change shape: async processing, precomputation, or tiering by data temperature ([[What is cold data and hot data]]).

> [!warning] Optimizing the visible line before measuring is how weeks vanish
> The hot line everyone stares at is rarely where the wall time goes; without a profile, effort lands on the 50 ms of CPU while a 500 ms query hums underneath. Measure, attribute, then optimize the largest bucket — in that order.

> [!tip] Interview answer
> No — the method is usually a container of waits. I segment wall time with tracing and profilers: database share (N+1, missing indexes), remote-call share (cache or parallelize), locks, IO, and only then the method's own CPU. First I also ask whether the operation should be fast at all — then fix the biggest measured bucket and re-measure.
