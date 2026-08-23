<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Data/Redis #SRS

# What serialization problems happen with Redis Spring Cache?

> [!abstract] Short answer
> **`RedisCacheConfiguration` defaults to `StringRedisSerializer` keys and `JdkSerializationRedisSerializer` values.** That JDK default is opaque, Java-only, brittle across class changes, and a documented deserialization security risk. Switching to JSON fixes many of those issues but introduces Jackson constraints (dates, constructors, polymorphism) and forbids caching Hibernate lazy proxies — cache **DTOs**.

## Default Redis cache serializers

| Setting | Default (docs) |
| --- | --- |
| Key serializer | `StringRedisSerializer` |
| Value serializer | `JdkSerializationRedisSerializer` |

```java
RedisCacheConfiguration defaults = RedisCacheConfiguration.defaultCacheConfig()
    .serializeValuesWith(
        RedisSerializationContext.SerializationPair.fromSerializer(RedisSerializer.json()))
    .entryTtl(Duration.ofMinutes(10));
```

**Listing 1.** Override value serialization on `RedisCacheConfiguration` (Spring Data Redis Cache reference).

Configure this on `RedisCacheManager.builder(…).cacheDefaults(…)`. Keys already default to strings; keep them consistent with any manual `RedisTemplate` key format you share.

```d2
direction: right
cacheable: "@Cacheable return value" {
  style.fill: "#e3f2fd"
}
ser: "Value RedisSerializer\n(JDK default / JSON)" {
  style.fill: "#fff3e0"
}
redis: "Redis bytes" {
  style.fill: "#e8f5e9"
}
read: "Deserialization\non cache hit" {
  style.fill: "#f3e5f5"
}

cacheable -> ser -> redis -> read
```

**Fig. 1.** Cache hits fail when the stored bytes cannot be deserialized by the current serializer and type model.

## Failure modes you hit in practice

**JDK value serializer:** class evolution / `serialVersionUID` breaks old entries; unreadable in `redis-cli`; Spring warns about gadget attacks on deserialize — see [[Why should you avoid JdkSerializationRedisSerializer]].

**JSON value serializer:** `LocalDateTime` and other Java Time types need a time module on the `ObjectMapper`; types without a suitable constructor (e.g. some builder-only beans) fail mapping; polymorphism needs explicit typing; **Hibernate lazy proxies / open sessions** do not serialize as plain domain objects — return **DTOs** from `@Cacheable` methods.

**Cross-app mismatch:** one node on JDK, another on JSON, or different Jackson configs → mysterious misses and exceptions on hit.

> [!warning] Caching entities is a trap
> A `@Cacheable` service that returns a managed JPA entity (especially with lazy associations) often stores a proxy or graph that cannot be safely reconstituted later. Cache a DTO or a dedicated cache model.

> [!warning] Serializer change does not migrate old keys
> Flipping from JDK to JSON leaves previous values undecodable until TTL expires or you flush the cache names. Plan a flush or dual-read window when changing formats.

> [!tip] Interview answer
> Redis Spring Cache defaults to string keys and JDK-serialized values — I replace the value serializer with JSON and never cache Hibernate proxies. Common JSON pain points are Java Time modules, constructors, and polymorphism. Keep serializers aligned across every instance, and flush or TTL-out old entries after a format change.

See [[How do you use Redis as a Spring CacheManager]], [[What serialization strategy should you use with RedisTemplate]], and [[Why should you avoid JdkSerializationRedisSerializer]].
