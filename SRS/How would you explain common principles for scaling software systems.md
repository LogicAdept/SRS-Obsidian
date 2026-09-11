<!--
reps: 0
priority: 0
-->
#SystemDesign/Scalability #SRS

# How would you explain common principles for scaling software systems

> [!abstract] Short answer
> Scaling principles form a repeatable ladder: measure first (SLOs and bottleneck metrics); remove work (cache, offload, async, precompute); split state and compute (statelessness, replication for reads, sharding for writes); isolate failures (bulkheads, backpressure, graceful degradation); and automate elasticity (autoscaling on the measured signal). Each step buys headroom by paying in complexity — the discipline is doing the cheapest step that removes the measured bottleneck, not the most impressive one.

## The ladder, step by step

First, measure: scaling without a bottleneck metric is decoration — latency percentiles, throughput at the SLO, saturation of the constrained resource (CPU, pool, disk, a downstream's rate limit). Second, remove work: caches serve repeats ([[What is caching used for]]), CDNs offload static and media, async queues move non-interactive work out of the request path, precomputation turns per-request aggregation into per-write maintenance (the denormalization logic of [[What is database denormalization for]]). Third, split: stateless services replicate freely behind load balancers ([[What is the difference between a stateful service and a stateless service]]); reads scale by replication ([[How would you explain database replication strategies]]); writes and datasets scale by sharding ([[What problem does database sharding solve]]) — the classic "scale cube" axes of clone (X), split-by-function (Y), split-by-data (Z). Fourth, isolate: timeouts, bulkheads, rate limiting and load shedding keep one slow dependency or tenant from collapsing the fleet ([[How do you protect a slower downstream service from overload]]) — a scaled system that fails as one unit is only a bigger single point of failure. Fifth, automate: autoscaling on measured load, capacity reviews, and load tests ([[What is load testing]]) that verify each rung before peak season does.

```text
1 measure   -> SLO, p95/p99, saturation of the binding resource
2 remove    -> cache, CDN, async queues, precompute
3 split     -> stateless clones | read replicas | shards (scale cube)
4 isolate   -> timeouts, bulkheads, rate limits, degradation
5 automate  -> autoscaling on the signal, capacity process
order: always the cheapest step that fixes the measured bottleneck
```

**Listing 1.** The scaling ladder with its ordering rule.

## The economics and the anti-patterns

Each rung pays complexity: caches pay staleness and invalidation, replicas pay replication lag ([[What is eventual consistency]]), sharding pays key-shaped queries and cross-shard transactions ([[How would you explain horizontal database sharding]]), async pays operational infrastructure. That is why the ordering rule exists — premature sharding or a distributed cache before measurement adds all the complexity and none of the headroom. The recurring anti-patterns: scaling a component that is not the bottleneck (ten replicas in front of one saturated database); scaling stateful by cloning without externalizing state (sticky-session dependence — [[How would you explain Sticky sessions]]); treating scaling as one big-bang rewrite instead of rung-by-rung; and ignoring the failure modes the new scale introduces (a herd of cold caches at failover — [[What difficulties arise when working with caching]]). The mature habit is the loop itself: measure, remove the bottleneck, re-measure — the same discipline as [[How do you optimize a high traffic web service]], generalized from one service to the system.

> [!warning] Scalability is not capacity — buy the rung the metric demands
> Adding nodes to a system whose bottleneck is a lock or a single database writer adds cost, not headroom. Every rung of the ladder only works when it addresses the measured binding resource; otherwise it is complexity theater.

> [!tip] Interview answer
> The principles form a ladder: measure the bottleneck against SLOs, remove work (cache, async, precompute), split by cloning stateless services, replicating reads and sharding writes, isolate failures with timeouts and load shedding, then automate scaling on the measured signal. Each rung pays in complexity, so I always buy the cheapest one that fixes the measured constraint.
