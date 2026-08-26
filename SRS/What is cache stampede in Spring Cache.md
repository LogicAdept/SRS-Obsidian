<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Caching #SRS

# What is cache stampede in Spring Cache?

> [!abstract] Short answer
> A **stampede** (thundering herd) is many concurrent **misses for the same key** — typically after expiry or at startup — so every thread **loads the DB**. Spring’s abstraction **does not lock by default**, so the value can be **computed several times**. **`@Cacheable(sync = true)`** serializes loads **in one process** if the provider supports it. It is **not** a cluster lock.

## Unlocked get-if-absent

*Understanding the Cache Abstraction*: programmatic get-if-not-found-then-put applies **no locks**; several threads may load the same item. Eviction has the same race. *Synchronized Caching*: concurrent invoke for the same argument **defeats caching** unless you set **`sync`**.

```java
@Cacheable(cacheNames = "foos", sync = true)
public Foo executeExpensiveOperation(String id) {
    return repository.load(id);
}
```

**Listing 1.** Official `sync` example — one `Callable` loader per key in that JVM. Limits (`unless` unsupported, one cache name): [[What is the sync attribute on Cacheable]].

Across **nodes**, each JVM can still miss Redis at once. Spring does **not** document `SETNX` as part of `@Cacheable`. Use the **provider** (Redis lock, Caffeine `refreshAfterWrite` in **Caffeine** config, jittered TTL on the store) or an application lock. Multi-process: configure the **cache product** — [[How do you choose a Spring Cache provider]].

```d2
direction: down
exp: "Hot key expires / cold start" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
herd: "N threads Cache.get miss" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
db: "N identical DB loads" {
  width: 220
  height: 50
  style.fill: "#ffebee"
}

exp -> herd -> db
```

**Fig. 1.** `sync = false` (default) path. With `sync = true`, one load, others block **on that Cache implementation**.

TTL expiry makes this worse on **shared Redis** (every instance sees the miss together) than on an unexpired local Caffeine map.

> [!warning] `sync` is not distributed
> Two pods, one Redis key: **two** loaders unless Redis/Caffeine implements cross-process coordination. Core Framework `CacheManager`s support in-process `get(key, Callable)` — Redis support is **provider-specific**.

> [!warning] Optional feature
> If the library ignores `sync`, you still stampede. Check that `Cache`’s `get(key, Callable)` contract.

> [!tip] Interview answer
> **Stampede is many threads missing the same key and all hitting the database.** Spring Cache does not lock unless `sync = true`, and that only coordinates **one JVM**. For a cluster, lock or refresh in the cache product, not in `@Cacheable` attributes.
