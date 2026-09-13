<!--
reps: 0
priority: 0
-->
#Caching #SRS #SystemDesign/Performance

# Is caching only used with databases?

> [!abstract] Short answer
> No — databases are just the most visible layer. A cache is any **faster tier holding a copy of data that is expensive to recompute or re-fetch**, and the pattern appears at every level of a computing stack: CPU caches and registers copy main memory, the OS page cache copies disk blocks, an application memoizes function results, an ORM keeps an identity map plus an optional second-level tier, HTTP caches copy responses in browsers/CDNs/proxies, resolvers cache DNS answers, build tools cache compiled artifacts, and message brokers lean on the OS page cache for throughput. The invariants are identical everywhere — a copy buys speed at the price of **staleness**, the value of the copy is set by the **hit rate**, and every layer answers the same three design questions: what to key on, when to invalidate, and what happens on a miss. Once you see the pattern, "should this be cached?" stops being a database question and becomes a per-layer cost question.

## The same three questions at every layer

Whatever the layer, the engineering content is identical: choose a **key** (an address, a URL, a query text, method arguments), choose an **invalidation policy** (TTL, explicit eviction, write-through, invalidation on write), and choose a **miss path** (recompute and populate, or fail through). Layers differ only in how much of that the hardware or the framework decides for you. The CPU cache invalidates on its own coherence protocol; a CDN obeys `Cache-Control` headers you set; a method-level cache in your framework keys on arguments and evicts when you say so. What changes across layers is the **cost asymmetry**: the further the data's source, the more a hit saves — which is why a CDN hit (saves a cross-continent round trip and origin load) is worth more engineering attention than an in-process memoization saving a microsecond.

| Layer | Caches a copy of | Typical hit saves | Invalidation driver |
| --- | --- | --- | --- |
| CPU caches | memory lines | ~100× vs RAM | hardware coherence |
| OS page cache | disk blocks | disk vs RAM latency | file writes, memory pressure |
| DNS resolver | name → IP | a resolver round trip | TTL per record |
| ORM L1/L2 | rows as objects | a query round trip | session end / ORM writes |
| Method cache (app) | computed results | the computation | explicit, TTL |
| HTTP: browser/CDN | responses | origin trip entirely | `Cache-Control`, purges |
| Build tools (Docker, compilers) | build artifacts | minutes of rebuild | input hashes |
| Broker (e.g. Kafka) | hot segments in page cache | disk reads on reads/rewinds | segment eviction |

Three observations worth carrying into any design discussion. First, **the layers stack**: a static file may be served from a CDN copy that was built from an origin server, whose page cache served the build that produced it — hits multiply down the chain, and so do staleness bugs. Second, **non-database caches dominate some systems outright**: for a static-assets-heavy site the CDN hit rate *is* the capacity plan; for a log pipeline the page cache absorbs most reads; neither has a database cache in the critical path at all. Third, the database itself is a cache consumer — buffer pools, plan caches, materialized views — so "caching vs databases" is a false opposition; the database is one of the cached-to layers ([[What is the main purpose of caching in an ORM]] covers the ORM tiers specifically).

```java
// the miss path is the invariant: every layer implements this shape
V get(K key) {
    V v = store.get(key);                    // fast tier
    if (v == null) {                         // miss
        v = loadFromSource(key);             // expensive path
        store.put(key, v, ttlOrPolicy);      // populate
    }
    return v;                                // hit: source never touched
}
```

**Listing 1.** Cache-aside read path — the same skeleton runs in a LinkedHashMap-based memoizer, a Redis-backed service, and (conceptually) a CDN: fast tier first, source only on miss, populate after.

> [!warning] More layers mean more copies mean more staleness bugs
> Every added cache layer multiplies the places where a reader can see old data. The classic production bug is not "the cache was slow" but "we invalidated layer 1 and forgot layer 2" — a CDN purge that skipped the browser, an ORM flush that skipped a method cache. Design the invalidation order across layers first; throughput tuning comes second ([[What difficulties arise when working with caching]] collects the failure modes).

> [!tip] Interview answer
> Caching is a universal tiering pattern, not a database feature: CPU and page caches, DNS TTLs, ORM identity maps and L2, method memoization, HTTP/CDN caches, build and page caches in brokers — all hold a copy to trade staleness for speed, all key on something, invalidate somehow, and pay off only through hit rate. The layer changes the cost asymmetry: a CDN hit saves a round trip and origin load, a page-cache hit saves disk, a memoization saves a computation. When asked where caching applies, I enumerate the stack from hardware to CDN, then answer the real question — which layer is worth adding here — from the read/write ratio and the invalidation story, not from habit.

See [[What is caching used for]], [[How would you explain cache hit rate and cache miss rate]], [[How would you explain distributed caching and cache hierarchies at a high level]], [[What is the main purpose of caching in an ORM]], and [[How do you make REST API responses cacheable]].
