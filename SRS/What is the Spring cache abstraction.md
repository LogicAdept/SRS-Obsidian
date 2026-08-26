<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS

# What is the Spring cache abstraction?

> [!abstract] Short answer
> Since **3.1**, Spring applies **cache-aside to methods**: on an advised call it looks up a **key**, **skips** the method on a hit, **invokes then puts** on a miss. The store is **not** Spring — you plug a **`CacheManager`** that vends **`org.springframework.cache.Cache`**. Annotations (`@Cacheable`, `@CachePut`, `@CacheEvict`) are only metadata until **`@EnableCaching`**.

## Method caching, not a product

*Understanding the Cache Abstraction*: the logic is **transparent to the caller**. It only fits methods that return the **same result for the same arguments**. Updates and evicts exist because data can change.

The SPI is two interfaces:

* **`Cache`** — `get` / `put` / `evict` / `clear` on one named region
* **`CacheManager`** — retrieve named `Cache`s

Business code talks to those types (or to annotations). Core Framework adapters include JDK **`ConcurrentMap`**, **Caffeine**, **JSR-107** (Ehcache 3.x and other JCache providers), and GemFire. Redis is a **Spring Data Redis** `RedisCacheManager`, not a core `org.springframework.cache` class.

```java
@Configuration
@EnableCaching
class CacheConfig {

    @Bean
    CacheManager cacheManager() {
        return new CaffeineCacheManager();
    }
}
```

**Listing 1.** Conceptual enablement: declaration (`@EnableCaching`) plus a store (`CacheManager`). Annotation catalog: [[What is the Spring Cacheable annotation]]. Internals: [[How does Cacheable work internally]].

```d2
direction: right
ann: "@Cacheable / @CachePut / @CacheEvict" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
abs: "CacheInterceptor\nCache + CacheManager SPI" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
store: "Caffeine / JCache /\nConcurrentMap / Redis …" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

ann -> abs -> store
```

**Fig. 1.** Spring writes the get-if-absent-then-put path; the provider owns TTL, clustering, and locking.

Two setup pieces: **declaration** (which methods, which policy) and **configuration** (the backing store). Spring Boot auto-configures a `CacheManager` **only after** `@EnableCaching`; with no cache library it uses in-memory concurrent maps. Provider order and `spring.cache.type`: [[What cache providers does Spring Cache support]].

> [!warning] Not JPA / Hibernate cache
> `jakarta.persistence.Cacheable` on an **entity** is the **second-level** persistence cache. Spring’s `org.springframework.cache.annotation.Cacheable` is **method** AOP. They do not share a `CacheManager`.

> [!warning] Annotations do nothing without enablement
> Remove `@EnableCaching` (or XML `<cache:annotation-driven/>`) and every `@Cacheable` is ignored — that is how you turn the feature off in one place.

> [!warning] No built-in cluster or lock
> The abstraction does **not** special-case multi-thread or multi-node behavior. Concurrent loads of the same key can stampede unless the provider (or `sync=true`) supports it. Shared data across nodes needs a **shared** store (for example Redis), not `ConcurrentMapCacheManager`.

> [!tip] Interview answer
> **Spring Cache is an AOP cache-aside layer over `Cache` and `CacheManager`, not a cache product.** You declare methods with `@Cacheable` / `@CachePut` / `@CacheEvict` and plug Caffeine, JCache, Redis, or a concurrent map. Enable it with `@EnableCaching`; without that, the annotations are inert. It is not Hibernate’s first- or second-level cache.
