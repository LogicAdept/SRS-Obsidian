<!--
reps: 0
priority: 0
-->
#Caching #SystemDesign/Performance #SRS

# How would you explain cache hit rate and cache miss rate

> [!abstract] Short answer
> The hit rate is the fraction of lookups the cache serves from the cache itself: hits divided by total lookups. The miss rate is its complement — misses divided by total lookups. The two numbers together tell you whether the cache is doing its job, because each miss costs the cache trip plus the origin trip, while a hit costs only the cache trip.

## Definitions and why they matter

For an interval, hit rate = hits / (hits + misses), miss rate = 1 − hit rate. The reason these are first-class metrics is the economics of the read path: if the origin costs 50 ms and the cache 1 ms, average latency = hit_rate · 1 ms + (1 − hit_rate) · 51 ms — so at 95% the mean is about 3.6 ms, and at 50% it is 26 ms. A cache whose hit rate stays near zero adds latency and memory cost while removing no origin load, which is exactly the "caching is dangerous" case in [[When is caching useful and when is it dangerous]]. Misses are also classified by cause — cold (key never cached), capacity (evicted), expired (TTL elapsed) — and the breakdown tells you which lever to pull: warm-up for cold, more memory or better eviction for capacity, longer TTL for expiry.

```text
hits   = lookups served from cache
total  = hits + misses
hit_rate  = hits / total            # e.g. 950 / 1000 = 0.95
miss_rate = misses / total          # 0.05
avg_cost  = hit_rate*Tc + miss_rate*(Tc + To)
          = 0.95*1ms + 0.05*(1+50)ms ~= 3.6 ms
```

**Listing 1.** Hit/miss accounting and the latency model that makes the ratio meaningful.

## Measuring in practice

Instrument the cache layer itself (Redis INFO reports keyspace_hits and keyspace_misses; the Spring cache abstraction exposes hit/miss statistics per cache via its Metrics — [[How do you monitor database health and load]] style dashboards chart them over time). Watch the trend, not the point value: a falling hit rate after a deploy usually means key naming changed, splitting counts across two key spaces. Track origin load alongside: the goal is less origin work, and a hit rate without that context can hide a growing dataset of never-read entries. [[What difficulties arise when working with caching]] maps each miss cause to its mitigation, and [[What is caching used for]] frames why the ratio is the value of the whole layer.

> [!warning] A hit rate is meaningless without the denominator
> 90% of ten requests an hour is nothing; 90% of a million requests a minute is an architecture. Always read hit rate together with request volume and origin load, or a rare-path cache will look like a success.

> [!tip] Interview answer
> Hit rate is hits over total lookups, miss rate is the complement. They matter because a miss costs cache plus origin time, so average latency scales with the miss rate — the difference between 95% and 50% can be an order of magnitude. I break misses into cold, capacity and expired to pick the fix.
