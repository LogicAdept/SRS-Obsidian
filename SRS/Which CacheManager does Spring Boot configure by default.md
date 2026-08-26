<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Boot/AutoConfiguration #SRS

# Which `CacheManager` does Spring Boot configure by default?

> [!abstract] Short answer
> **Only after `@EnableCaching`.** If you have **not** defined a `CacheManager` (or a `CacheResolver` named `cacheResolver`) and **no cache library** is on the classpath, Boot auto-configures the **Simple** provider: in-memory **`ConcurrentHashMap`** regions (`ConcurrentMapCacheManager`). Any earlier provider in Boot’s detection list wins (JCache, Redis, Caffeine, …). Force a type with **`spring.cache.type`**.

## Detection order, Simple last

Spring Boot *Caching*: the cache abstraction does not ship a store. Auto-config **tries providers in this order**:

Generic (`Cache` beans) → **JCache** (Ehcache 3, Hazelcast, Infinispan, …) → Hazelcast → Infinispan → Couchbase → **Redis** → **Caffeine** → Cache2k → **Simple**.

**Simple** is “the default if no caching library is present.” Caches are created **as needed**, unless `spring.cache.cache-names` restricts the set. Boot does **not** recommend Simple for **production**. Tune with `CacheManagerCustomizer<ConcurrentMapCacheManager>` (for example `setAllowNullValues(false)`).

```properties
# force the in-memory map even if Redis is on the classpath
spring.cache.type=simple
```

**Listing 1.** Conceptual override. `spring.cache.type=none` is a **no-op** manager (useful in tests). Full catalog: [[What cache providers does Spring Cache support]]. Map SPI: [[What is ConcurrentMapCacheManager]].

```d2
direction: down
en: "@EnableCaching" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
scan: "Classpath / spring.cache.type" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
simple: "Simple ConcurrentMap\nif nothing else matches" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

en -> scan -> simple
```

**Fig. 1.** Without `@EnableCaching`, Boot does **not** auto-configure this infrastructure. Your own `CacheManager` `@Bean` **replaces** auto-config.

`spring-boot-starter-cache` pulls `spring-context-support` (JCache/Caffeine adapters). The starter **is not** a distributed cache — [[What is spring-boot-starter-cache]].

> [!warning] No TTL, no max size, no cluster
> Simple is a heap map in **one JVM**. Adding **Caffeine** or **Redis** on the classpath **changes** the auto-configured manager unless you set `spring.cache.type`.

> [!warning] Not Spring Framework’s “default CacheManager”
> Core Framework **requires** you to declare a manager; it does not invent Simple. The concurrent-map default is a **Boot** auto-config choice.

> [!warning] Tests
> `@AutoConfigureCache` (or `spring.cache.type=none`) replaces the auto-configured manager with **no-op** so tests do not keep cache state. Avoid `@EnableCaching` on the main application class if slice tests must not require a cache.

> [!tip] Interview answer
> **Boot’s default with `@EnableCaching` and no cache library is an in-memory concurrent map.** It is for getting started, not multi-node production. Classpath order can pick Redis or Caffeine instead; `spring.cache.type` forces the choice. A `CacheManager` bean wins over auto-config.
