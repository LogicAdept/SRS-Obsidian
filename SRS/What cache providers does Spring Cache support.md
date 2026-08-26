<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS

# What cache providers does Spring Cache support?

> [!abstract] Short answer
> The abstraction is **`Cache` + `CacheManager`**, not a product. **Core Framework** ships **ConcurrentMap**, **Caffeine**, **JSR-107 / JCache** (Ehcache 3.x, Hazelcast, Infinispan, …), and **GemFire** adapters. **Anything else** needs a `CacheManager`/`Cache` adapter (`AbstractCacheManager`). **Boot** auto-detects Generic, JCache, Hazelcast, Infinispan, Couchbase, **Redis**, Caffeine, Cache2k, then **Simple**.

## Framework vs Boot lists

*Understanding the Cache Abstraction* / *Configuring the Cache Storage*:

| Store | Typical class | Notes |
| --- | --- | --- |
| JDK map | `ConcurrentMapCacheManager` | No TTL; one JVM |
| Caffeine | `CaffeineCacheManager` | Local, size/expire spec |
| JSR-107 | `JCacheCacheManager` | Ehcache 3, others; wrap `javax.cache.CacheManager` |
| GemFire | Spring Data GemFire | Distributed |
| Composite / no-op | `CompositeCacheManager` | Chain managers; `fallbackToNoOpCache` |

Ehcache **3.x** is **JCache-compliant** — no dedicated Ehcache 3 `CacheManager` in core Spring. Redis is **Spring Data Redis** `RedisCacheManager`, wired by **Boot** when Redis is configured.

Boot detection order (after `@EnableCaching`, no user `CacheManager`): Generic → JCache → Hazelcast → Infinispan → Couchbase → Redis → Caffeine → Cache2k → Simple. Override: `spring.cache.type`. Starter: [[What is spring-boot-starter-cache]]. Default Simple: [[Which CacheManager does Spring Boot configure by default]].

Non-JSR-107 products: implement `Cache` + `CacheManager` (*Plugging-in Different Back-end Caches*).

```d2
direction: down
spi: "Cache / CacheManager SPI" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
core: "ConcurrentMap · Caffeine · JCache · GemFire" {
  width: 340
  height: 60
  style.fill: "#fff3e0"
}
boot: "+ Redis · Couchbase · Cache2k · Simple" {
  width: 340
  height: 60
  style.fill: "#e8f5e9"
}

spi -> core -> boot
```

**Fig. 1.** Business code stays on annotations; the bean chooses the product. How to pick: [[How do you choose a Spring Cache provider]].

> [!warning] Not Hibernate L2 or a CDN
> `jakarta.persistence.Cacheable` / Hibernate second-level cache and Varnish/CDN are **other layers**. This list is Spring **method** cache `CacheManager`s.

> [!warning] Classpath changes Boot’s pick
> Add Caffeine or Redis and Boot may **stop** using Simple unless you set `spring.cache.type`.

> [!warning] Support ≠ every feature
> TTL, clustering, and `sync` locking are **provider** capabilities. ConcurrentMap has none of the first two.

> [!tip] Interview answer
> **Spring Cache talks to `CacheManager`, not to Redis directly.** Framework adapters cover concurrent maps, Caffeine, and JCache (Ehcache 3). Boot also auto-configures Redis and others from the classpath. Simple in-memory is last; production usually Caffeine (one node) or Redis (many nodes).
