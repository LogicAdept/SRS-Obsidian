<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS

# How do you configure TTL for Spring Cache?

> [!abstract] Short answer
> **`@Cacheable` has no `ttl` attribute.** Expiration is **provider configuration** on the `CacheManager` (or native XML/spec). **Redis:** `RedisCacheConfiguration.entryTtl(...)` or Boot `spring.cache.redis.time-to-live`. **Caffeine:** spec `expireAfterWrite` / `expireAfterAccess`. **`ConcurrentMapCacheManager`:** **no TTL**.

## Abstraction vs store

Spring *How can I Set the TTL/TTI/Eviction policy*: expose TTL in the abstraction would be useless for `ConcurrentHashMap`. Set policies on the **backing cache**.

**Redis (Spring Data Redis / Boot):**

```java
@Bean
RedisCacheManager cacheManager(RedisConnectionFactory connectionFactory) {
    RedisCacheConfiguration defaults = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofHours(1));
    return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(defaults)
            .build();
}
```

**Listing 1.** Same pattern as [[How do you use Redis as a Spring CacheManager]]. Per-cache: `withInitialCacheConfigurations` / `RedisCacheManagerBuilderCustomizer`. Boot:

```properties
spring.cache.cache-names=cache1,cache2
spring.cache.redis.time-to-live=10m
```

**Caffeine:** `CaffeineCacheManager.setCacheSpecification(...)` or Boot `spring.cache.caffeine.spec=maximumSize=500,expireAfterAccess=600s`.

**JCache / Ehcache 3:** expiry in the **JCache/Ehcache** configuration file, then `JCacheCacheManager`.

```d2
direction: down
ann: "@Cacheable — no ttl attribute" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
mgr: "CacheManager / native spec" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
store: "Redis EXPIRE / Caffeine ticker / …" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}

ann -> mgr -> store
```

**Fig. 1.** Eviction after TTL is the product’s job. Map store: [[What is ConcurrentMapCacheManager]].

> [!warning] Simple Boot default never expires
> In-memory concurrent maps grow until restart or explicit `@CacheEvict`. Do not expect `@Cacheable` to time out on its own.

> [!warning] Different caches, different clocks
> A one-hour Redis TTL and a Caffeine `expireAfterAccess` are **not** the same semantics. Per-name overrides exist on Redis/Caffeine builders; global `entryTtl` does not apply to ConcurrentMap.

> [!tip] Interview answer
> **TTL is not on `@Cacheable`.** Configure it on Redis (`entryTtl` / `spring.cache.redis.time-to-live`) or Caffeine (spec). The Spring cache abstraction only get/put/evict; ConcurrentMap has no expire.
