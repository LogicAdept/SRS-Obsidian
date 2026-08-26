<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS

# How do you implement multi-level caching in Spring Boot?

> [!abstract] Short answer
> **Spring Boot has no L1/L2 cache annotation.** `@Cacheable` talks to **one** `Cache` from **one** `CacheManager.getCache(name)`. A **Caffeine + Redis** “near + far” store is a **custom `Cache`/`CacheManager`**: get local, then Redis, then load; put/evict **both**. **`CompositeCacheManager` is not that** — it only **picks which delegate owns the cache name**.

## Not CompositeCacheManager

`CompositeCacheManager` javadoc: **iterate delegates** until one returns a non-null `Cache` for the **name**. Delegates must return **`null` for unknown names**. Most managers **lazily create** any name, so the **first** delegate swallows every request. `fallbackToNoOpCache` appends a no-op for missing names (tests / missing store) — *Configuring the Cache Storage*. That is **name routing**, not “read Caffeine then Redis for the same key.”

```java
@Bean
CacheManager cacheManager(CacheManager caffeine, CacheManager redis) {
    CompositeCacheManager composite = new CompositeCacheManager();
    composite.setCacheManagers(List.of(caffeine, redis));
    composite.setFallbackToNoOpCache(true);
    return composite;
}
```

**Listing 1.** Official composite pattern — **not** two-level values. Static `setCacheNames` on the first manager is required if Redis should own some names.

**True L1/L2** (dump sketch): implement `org.springframework.cache.Cache` that `get`s Caffeine, then Redis, then caller; `put`/`evict`/`clear` both; short local TTL via Caffeine spec; optional Redis pub/sub to `clear` L1 on other nodes. That class is **application code**, not a Boot starter. Register it through a `CacheManager`. Abstraction: [[What is the Spring cache abstraction]]. Redis manager: [[How do you use Redis as a Spring CacheManager]].

```d2
direction: down
aop: "@Cacheable → one Cache" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
comp: "CompositeCacheManager\nfirst name match wins" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
l12: "Custom Cache:\nCaffeine then Redis" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

aop -> comp
aop -> l12
```

**Fig. 1.** Two different designs. Only the custom `Cache` implements stacked lookups.

> [!warning] No `@EnableTwoLevelCache`
> Adding Caffeine **and** Redis on the classpath makes Boot **pick one** provider (JCache/Redis/Caffeine order), not both. Declare **your** `CacheManager` bean.

> [!warning] Lazy create blocks the chain
> If Caffeine is dynamic, `getCache("books")` never falls through to Redis. Use **static** names on the first manager or do not use `CompositeCacheManager` for L2.

> [!warning] L1 stale across nodes
> Local Caffeine is per JVM. Redis puts on another instance do not update L1 unless you **evict locally** (pub/sub, TTL, or skip L1).

> [!tip] Interview answer
> **Multi-level caching is not a Boot feature.** `CompositeCacheManager` chooses a delegate **by cache name**. A Caffeine-then-Redis stack is a **custom `Cache`** that get/put/evict both layers. Spring’s interceptor still sees a single `Cache` SPI.
