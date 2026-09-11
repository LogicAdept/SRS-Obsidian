<!--
reps: 0
priority: 0
-->
#Caching #Problems/Persistence #SystemDesign/Performance #SRS

# What difficulties arise when working with caching

> [!abstract] Short answer
> The hard problems are coherence and collapse modes: keeping every copy consistent with the origin on writes (invalidation), surviving a cold or overloaded cache (thundering herd, cache stampede), protecting the origin from skewed traffic (hot keys), and bounding memory (eviction choice). Each is operational, not syntactic — a wrong choice shows up only under load or after a restart.

## Coherence: invalidation and staleness

Every cached value is a copy, and writes create the classic consistency problem: which copies are updated, evicted, or allowed to expire? Cache-aside sidesteps distributed writes by evicting on write and refilling lazily, but then reads between the write and the next refill see stale data — the inconsistency window. Write-through closes that window for writes that go through the application, but the AWS caching whitepaper notes it must still be paired with a TTL, because data written before it was cached (or changed out of band) still ages. Distributed deployments add a second layer: when several app nodes each hold a local copy, cluster-wide invalidation must be explicit — [[How do you invalidate Spring Cache in a cluster]] shows the Spring + Redis pattern.

## Collapse modes under load

Three classic failure cascades start at the cache. A thundering herd on miss: one popular key expires, and thousands of concurrent readers all fall to the origin at once; per-key locks or a short-lived stale-serving window prevent the pile-up. A stampede after restart: the cache starts empty and every request misses, so the origin sees full production load with no warming. Hot keys: a handful of keys absorb most of the traffic and overload one cache shard even though the hit rate is fine. Eviction policy is the memory-side counterpart: Redis offers noeviction, allkeys-lru, allkeys-random and volatile- variants (LFU included), and returning errors (noeviction) versus silently dropping data is a product decision, not a setting. [[When is caching useful and when is it dangerous]] covers the decision to cache at all; [[Can LinkedHashMap fully implement an LRU cache]] shows what an LRU actually costs to implement; [[How would you explain cache hit rate and cache miss rate]] gives the metrics to watch while fighting these modes.

```text
t0  key K expires in cache
t1  1000 concurrent requests for K -> all miss -> all hit DB  (stampede)
fix A: per-key mutex — only one request refills, others wait
fix B: serve slightly stale K while one refresher rebuilds
```

**Listing 1.** A stampede timeline and the two standard mitigations.

> [!warning] A full cache that returns errors is a self-inflicted outage
> With noeviction, writes fail when memory is exhausted. If that policy is chosen silently, the cache becomes the least reliable component of the read path. Eviction policy and memory limits must be chosen deliberately, not left at defaults.

> [!tip] Interview answer
> Caching is hard because copies must stay coherent (invalidation, staleness windows) and because the layer itself can fail under load: stampedes on expiry, cold-start herds, hot keys and eviction-policy outages. Mature designs add TTLs, per-key locks, warming, and measured eviction instead of trusting defaults.
