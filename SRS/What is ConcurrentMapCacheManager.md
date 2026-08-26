<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS

# What is `ConcurrentMapCacheManager`?

> [!abstract] Short answer
> **`ConcurrentMapCacheManager` is Spring’s JDK `ConcurrentHashMap` `CacheManager`.** It lazily builds a **`ConcurrentMapCache` per name** (dynamic mode) or a **fixed name set** (static constructor / `setCacheNames`). Fine for tests and simple in-process caching. **No TTL, no size limit, no clustering** — javadoc points to **Caffeine** or **JCache** for real local caches.

## Heap map per cache name

Package `org.springframework.cache.concurrent` (since 3.1). *Configuring the Cache Storage*: the JDK cache is fast and scales for basic use, but it **does not** provide management, persistence, or eviction contracts. Lifecycle is the **application process**.

```java
@Configuration
@EnableCaching
class CacheConfig {

    @Bean
    CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("books", "authors");
    }
}
```

**Listing 1.** **Static** mode: only those names exist; further `getCache` names are not created. No-arg constructor is **dynamic** (create on first request). `setCacheNames(null)` returns to dynamic. SPI: [[What is CacheManager]].

Defaults: **`allowNullValues = true`** (holder object; `ConcurrentHashMap` cannot store null). **`storeByValue = false`** (references; `true` copies via serialization, 4.3+). Changing either **resets** existing caches.

```d2
direction: right
mgr: "ConcurrentMapCacheManager" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
c1: "ConcurrentMapCache\n\"books\"" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
c2: "ConcurrentMapCache\n\"authors\"" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

mgr -> c1
mgr -> c2
```

**Fig. 1.** Each region is a map in **this JVM**. Spring Boot’s **Simple** provider is this family when no other cache library is present — [[Which CacheManager does Spring Boot configure by default]].

`resetCaches()`: dynamic mode **drops** regions for on-demand recreate; static mode **clears entries**. `removeCache(name)` since 6.1.15. Async `retrieve` is a basic `CompletableFuture` adaptation.

> [!warning] One process, one heap
> Entries **die on restart** and are **invisible** to other instances. `allEntries` / `clear` does not invalidate other nodes. Use Redis/JCache for a cluster.

> [!warning] Unbounded growth
> No max size, no expire. A hot `@Cacheable` can retain every distinct key until OOM. Production local cache → **CaffeineCacheManager** (or JCache) with a spec.

> [!warning] Not a sophisticated manager
> Javadoc: useful for **testing or simple scenarios**. `SimpleKey` is documented as safe with this store; remote serializers are a different problem.

> [!tip] Interview answer
> **`ConcurrentMapCacheManager` wraps `ConcurrentHashMap` regions in-process.** Dynamic or fixed names, no TTL. Boot uses something in this family when you enable caching with no cache library. It is not shared across nodes and will not evict by time or size.
