<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS

# What is `CacheManager`?

> [!abstract] Short answer
> **`org.springframework.cache.CacheManager` is Spring’s cache-manager SPI** (since 3.1): look up a named **`Cache`** region (`getCache(name)`), list known names, optionally **`resetCaches()`**. Annotation caching **requires** a `CacheManager` bean — the Framework has **no** default store. Implementations wrap ConcurrentMap, Caffeine, JCache, Redis, and others.

## Registry of named `Cache`s

`CacheManager` javadoc: central SPI for **named cache regions**. `getCache` may **lazily create** a region if the provider allows; otherwise it returns **`null`** (unknown name / cannot create).

Annotation-driven caching resolves `cacheNames` / `value` through this manager (default `SimpleCacheResolver`). `@EnableCaching` finds the bean **by type**; XML `<cache:annotation-driven/>` looks for a bean named **`cacheManager`**.

```java
@Bean
CacheManager cacheManager() {
    return new ConcurrentMapCacheManager("books", "authors");
}
```

**Listing 1.** Conceptual bean. This constructor is **static** mode: only those names exist. A no-arg `ConcurrentMapCacheManager` is **dynamic** (creates regions on first `getCache`). Map manager: **no TTL** — javadoc points to Caffeine or JCache for real local caches. Abstraction: [[What is the Spring cache abstraction]].

```d2
direction: right
ann: "@Cacheable(\"books\")" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
mgr: "CacheManager.getCache(\"books\")" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
c: "Cache.get / put / evict" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}

ann -> mgr -> c
```

**Fig. 1.** The interceptor never talks to Redis or Caffeine APIs directly — only `Cache`. Custom which-cache logic: [[What is CacheResolver]].

**Implementations (examples):** `ConcurrentMapCacheManager` (heap, one JVM), `CaffeineCacheManager`, `JCacheCacheManager` (Ehcache 3, Hazelcast, Infinispan, …), Spring Data Redis **`RedisCacheManager`**. Spring 6+ does **not** ship a dedicated `EhCacheCacheManager` for Ehcache 3 — use JCache. Boot auto-detects a provider **after** `@EnableCaching` unless you declare your own `CacheManager` bean (that typically **replaces** auto-config). Detection order: [[What cache providers does Spring Cache support]].

> [!warning] Name mismatch
> In **static** mode, a `@Cacheable("orders")` name that was never registered → `getCache` is **`null`** → runtime failure when the operation runs (often not at startup). Dynamic managers create the region instead.

> [!warning] Not TTL, not clustering
> `CacheManager` does not define expiration. Concurrent maps die with the process and are **not** shared across nodes. TTL and cluster semantics live on the **provider** (`Caffeine` spec, `RedisCacheConfiguration`, JCache config).

> [!warning] Two beans, ambiguous type lookup
> `@EnableCaching` injects **by type**. Two `CacheManager` beans need **`CachingConfigurer`** (or a qualifier) or startup fails to pick one.

> [!tip] Interview answer
> **`CacheManager` is the registry of named `Cache` instances the AOP interceptor uses.** You must provide one — Caffeine, JCache, Redis, or a concurrent map. Boot can auto-configure it after `@EnableCaching`; your own `@Bean` replaces that. Cache names on annotations must resolve through this manager.
