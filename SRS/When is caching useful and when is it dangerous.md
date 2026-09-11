<!--
reps: 0
priority: 0
-->
#Caching #SystemDesign/Tradeoffs #SRS

# When is caching useful and when is it dangerous

> [!abstract] Short answer
> Caching pays when the same data is read far more often than it changes — read-heavy, tolerate-staleness, well-shaped access (hot keys). It is dangerous when values change between reads more often than they are read, when correctness depends on a fresh value (balances, stock, permissions), when keys are so uniformly distributed that the hit rate stays near zero, or when invalidation is harder than recomputing the value.

## The conditions that make it pay

The economic argument is a ratio: reuse versus mutation. A product catalog page or an exchange-rate lookup is read millions of times between updates, so a few minutes of TTL removes almost all origin load. The AWS caching whitepaper frames the two fill strategies around this: lazy loading tolerates staleness bounded by the TTL and only caches what is requested, while write-through keeps the copy coherent at the cost of writing every value even if it is never read — the whitepaper notes write-through is almost always combined with lazy loading plus a TTL for that reason. Metrics make the decision measurable: if [[How would you explain cache hit rate and cache miss rate]] shows a hit rate of a few percent, the cache is paying rent in memory and invalidation bugs without removing load.

## The failure modes

The dangerous side has names. Stale reads violate user expectations when the cached value is an authorization decision or an account balance. Invalidation on write is a distributed commit in disguise: every writer must update or evict every copy, which is why the saying "there are only two hard things in computer science: cache invalidation and naming things" survives. A cache in the critical path adds a new dependency — with a cache-aside design the origin must survive a cold cache, or a restart becomes an outage through a thundering herd. [[What difficulties arise when working with caching]] lists the operational traps, [[What is caching used for]] the benefits, and [[How do you invalidate Spring Cache in a cluster]] shows how a concrete stack (Spring + Redis) attacks the invalidation problem.

```text
read x:   hit  (1 RAM round trip)          -> serve copy
read x:   miss (1 RAM trip + origin trip)  -> serve origin, fill cache
write x:  cache-aside -> evict x, origin owns truth
          write-through -> origin + cache updated together
```

**Listing 1.** The four cases a caching decision must cover: hits pay, misses cost double, and writes decide the coherence model.

> [!warning] Don't cache before measuring
> Adding a cache to a low-reuse access path lowers latency for a warm few and raises it for the cold majority, while adding staleness and a second failure mode. Confirm reuse (hit-rate potential) and staleness tolerance before adding the layer.

> [!tip] Interview answer
> Cache when reuse is high and staleness is tolerable: read-heavy data, hot keys, expensive computation. It is dangerous when data changes per read, when freshness is correctness, or when invalidation logic becomes harder than the query it replaces — then the cache adds cost without removing load.
