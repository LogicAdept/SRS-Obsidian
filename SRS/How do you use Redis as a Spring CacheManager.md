<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Data/Redis #SRS

# How do you use Redis as a Spring CacheManager?

> [!abstract] Short answer
> Enable Spring’s cache abstraction (`@EnableCaching`) and expose a **`RedisCacheManager`** bean built from a **`RedisConnectionFactory`**. Configure defaults with **`RedisCacheConfiguration`** (`entryTtl`, serializers, null handling). Shared Redis makes cache entries visible across application instances.

## Wire `RedisCacheManager`

```java
@Configuration
@EnableCaching
class CacheConfig {

  @Bean
  RedisCacheManager cacheManager(RedisConnectionFactory connectionFactory) {
    RedisCacheConfiguration defaults = RedisCacheConfiguration.defaultCacheConfig()
        .entryTtl(Duration.ofHours(1))
        .disableCachingNullValues();

    return RedisCacheManager.builder(connectionFactory)
        .cacheDefaults(defaults)
        .build();
  }
}
```

**Listing 1.** Builder + default TTL (Spring Data Redis: Redis Cache). `RedisCacheManager.create(connectionFactory)` is the minimal one-liner when defaults are enough.

Per-cache overrides use `withInitialCacheConfigurations(Map)`. Optional `.transactionAware()` ties cache puts/evicts to Spring transactions.

```d2
direction: right
ann: "@Cacheable / @CacheEvict" {
  style.fill: "#e3f2fd"
}
mgr: "RedisCacheManager" {
  style.fill: "#fff3e0"
}
redis: "Redis\n(shared keys)" {
  style.fill: "#e8f5e9"
}
nodes: "App instance A / B" {
  style.fill: "#f3e5f5"
}

ann -> mgr -> redis
nodes -> redis
```

**Fig. 1.** Spring Cache APIs talk to `RedisCacheManager`; one Redis keyspace is shared by every node using that manager.

## Defaults that matter

| Setting | Default (docs) |
| --- | --- |
| Key prefix | Cache name + `::` |
| Key serializer | `StringRedisSerializer` |
| Value serializer | `JdkSerializationRedisSerializer` |
| Entry TTL | None |
| Cache nulls | Yes |

TTL is **time-to-live on write/update**, not “expire after last read,” unless you opt into time-to-idle (`enableTimeToIdle()`, Redis **6.2+** / `GETEX`). Cache clear historically used `KEYS`+`DEL`; prefer a `SCAN` batch strategy for large keyspaces.

> [!warning] Default JDK value serialization
> Out of the box, cache values use **`JdkSerializationRedisSerializer`**. Prefer JSON (or another safe format) for values and never cache Hibernate proxies / lazy entity graphs — serialize DTOs. See [[Why should you avoid JdkSerializationRedisSerializer]] and [[What serialization problems happen with Redis Spring Cache]].

> [!warning] Local vs shared cache
> `ConcurrentMapCacheManager` is per-JVM. Only a shared backend such as **`RedisCacheManager`** makes `@CacheEvict` on one node visible to the others — see [[How do you invalidate Spring Cache in a cluster]].

> [!tip] Interview answer
> I add `@EnableCaching` and a `RedisCacheManager` from `RedisConnectionFactory`, usually via `RedisCacheManager.builder` with `RedisCacheConfiguration` for TTL and serializers. Redis becomes the shared cache store so every instance sees the same keys. I avoid default JDK serialization and do not put lazy JPA entities in the cache.

See [[How do you invalidate Spring Cache in a cluster]], [[What serialization problems happen with Redis Spring Cache]], and [[How do you store a Redis value with a TTL]].
