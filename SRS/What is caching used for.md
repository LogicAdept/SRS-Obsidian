<!--
reps: 0
priority: 0
-->
#Caching #SystemDesign/Performance #SRS

# What is caching used for

> [!abstract] Short answer
> Caching keeps a copy of expensive-to-compute or expensive-to-fetch data in a faster storage layer, so repeated requests are served without touching the slow origin. It buys latency (RAM-speed reads instead of disk or network round trips), throughput (fewer origin hits per user request), and resilience (a cache can serve reads while the origin is down or slow). Its price is staleness: the copy may lag the source of truth.

## Where caches live

A read path can pass through several cache layers, each trading hit rate against coherence. A client or browser caches static assets; a CDN caches content at edge locations close to users; a reverse proxy or web server caches responses; the application uses an in-memory or distributed cache such as Redis or Memcached between itself and the database; and the database itself has internal caches (buffer pools, the Hibernate first-level cache for an ORM session). The AWS database caching whitepaper describes the two application-level strategies as lazy loading (fill the cache on miss) and write-through (update the cache on every write), and recommends combining write-through with a TTL because a write-through cache only helps data that is actually read.

```sql
-- cache-aside read path (application code, conceptual)
-- 1. GET user:42 from Redis
-- 2. hit  -> return the cached JSON
-- 3. miss -> SELECT ... FROM users WHERE id = 42
-- 4. SETEX user:42 300 '<json>'  (TTL bounds staleness)
```

**Listing 1.** Cache-aside on the read path: miss falls through to the origin, then populates the cache with a TTL.

## What it buys and what it costs

A hit ratio near 100% turns a request that cost one disk seek plus joins into one RAM read, which is why a cache in front of a read-heavy database is often the single cheapest scalability win. The costs show up on the correctness side: every cached value is a second copy that can go stale, so the design has to answer when the copy expires (TTL) and when it is actively invalidated on writes. Caches also add failure modes of their own — a cold cache after restart can hammer the origin (a thundering herd), and a hot key can overload one shard. [[When is caching useful and when is it dangerous]] develops the decision, and [[What difficulties arise when working with caching]] the operational traps; Spring-level mechanics live in [[How do you implement caching in Spring]].

> [!warning] A cache is not a source of truth
> Cached data is a discardable copy. If a service treats the cache as authoritative, a flush or an eviction wipes state that no other component owns. Always keep the origin system capable of regenerating every cached value.

> [!tip] Interview answer
> Caching exists to avoid repeating expensive work: it stores a copy of results in a faster layer so reads skip the database or network. It improves latency and throughput, but introduces staleness, so every design pairs a hit-ratio goal with an invalidation or TTL policy.
