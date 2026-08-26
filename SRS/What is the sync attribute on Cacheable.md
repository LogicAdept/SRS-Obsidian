<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is the `sync` attribute on `Cacheable`?

> [!abstract] Short answer
> **`sync = true` (since 4.3) asks the provider to lock that cache key while the value is loaded.** One thread runs the method; others **wait** for the same key instead of all hitting the database. Default **`false`**: the abstraction **does not lock** — concurrent misses can compute the value several times. It is a **hint**; support is **provider-specific**.

## One loader per key (in-process)

Spring *Synchronized Caching*: concurrent calls with the same arguments (often at startup) defeat caching if every thread misses. `sync` tells the store to lock the **entry** during computation, via **`Cache.get(key, Callable)`**.

```java
@Cacheable(cacheNames = "foos", sync = true)
public Foo executeExpensiveOperation(String id) {
    return remote.load(id);
}
```

**Listing 1.** Official example. Core Framework `CacheManager`s support the hint; a third-party `Cache` might ignore it — check that provider. Stampede context: [[What is cache stampede in Spring Cache]]. Internals: [[How does Cacheable work internally]].

`Cacheable` javadoc limitations when `sync = true`:

1. **`unless` is not supported**
2. **Only one cache name**
3. **No other cache operation** combined on the method

It is a **combined** get-or-load. If that combined access **fails** on first contact, there is **no separate put**. With `sync = false`, get and put are independent (`CacheErrorHandler` can swallow get errors and still put).

```d2
direction: down
miss: "Several threads, same key, miss" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
sync: "sync=true: one Callable\nothers block on the entry" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
nosync: "sync=false: every thread\ninvokes the method" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

miss -> sync
miss -> nosync
```

**Fig. 1.** Locking is **per JVM / per cache implementation**, not a cluster mutex.

> [!warning] Not a distributed lock
> Two application nodes can both miss a Redis key and both load. `sync` does not replace Redisson/`SET NX` (or the provider’s own locking). Local `ConcurrentMapCache` only serializes threads **in that process**.

> [!warning] Optional feature
> If the library does not implement synchronized `get(key, Callable)`, you may still stampede — or get an error. Do not assume Redis/`JCache` matches Caffeine.

> [!warning] Cannot mix `unless` or extra caches
> `sync = true` plus `unless = "#result == null"` or `cacheNames = {"a","b"}` violates the documented constraints.

> [!tip] Interview answer
> **`sync = true` serializes loads of the same key so only one thread computes the miss.** Default Spring Cache does not lock. It is per-process and provider-dependent — not a cluster lock — and it forbids `unless`, multiple cache names, and combined cache operations.
