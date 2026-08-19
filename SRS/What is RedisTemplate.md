<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

RedisTemplate is the central class for Redis in Spring Data Redis. It implements RedisOperations and exposes type-safe views per data structure: opsForValue, opsForHash, opsForList, opsForSet, opsForZSet (dumps also mention geo, stream, hyperloglog, cluster).

Configure it with a RedisConnectionFactory and serializers. A typical dump bean:

```java
RedisTemplate<String, Object> template = new RedisTemplate<>();
template.setConnectionFactory(factory);
template.setKeySerializer(new StringRedisSerializer());
template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
template.setHashKeySerializer(new StringRedisSerializer());
template.setHashValueSerializer(new GenericJackson2JsonRedisSerializer());
template.afterPropertiesSet();
```

Default serialization is Java serialization for most operations.
> [!warning] Unverified traps from the dump
> - The default JDK serializer is called out as something to replace in production.
> - Keys must be non-null; values may be null only if the serializer allows it.
