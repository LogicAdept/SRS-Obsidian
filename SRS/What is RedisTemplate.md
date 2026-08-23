<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS

# What is RedisTemplate?

> [!abstract] Short answer
> **`RedisTemplate<K, V>`** is the central Spring Data Redis API for high-level Redis access. It implements **`RedisOperations`**, handles **connection management and serialization**, and exposes typed operational views (`opsForValue`, `opsForHash`, `opsForList`, `opsForSet`, `opsForZSet`, geo, HyperLogLog, …). Prefer injecting **`RedisOperations`**.

## Role and configuration

`RedisConnection` works in raw `byte[]`. The template sits above that: you pass domain keys/values, and configured **`RedisSerializer`s** convert to bytes. Once configured, the bean is **thread-safe** and reusable.

```java
@Bean
RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
  RedisTemplate<String, Object> template = new RedisTemplate<>();
  template.setConnectionFactory(factory);
  template.setKeySerializer(RedisSerializer.string());
  template.setHashKeySerializer(RedisSerializer.string());
  template.setValueSerializer(RedisSerializer.json());
  template.setHashValueSerializer(RedisSerializer.json());
  return template;
}
```

**Listing 1.** Template wired to a connection factory with explicit key/value serializers (Spring Data Redis template docs).

Operational views match Redis structures — for example `opsForValue()` for strings — see [[How do you use opsForValue with RedisTemplate]]. You can also inject a view bean (`ListOperations`, …) so callers skip `opsFor*`. For string-only workloads, use **`StringRedisTemplate`**.

```d2
direction: right
app: "Application code" {
  style.fill: "#e3f2fd"
}
ops: "RedisOperations\nRedisTemplate" {
  style.fill: "#e8f5e9"
}
ser: "RedisSerializer\nK / V / hash" {
  style.fill: "#fff3e0"
}
conn: "RedisConnectionFactory\n→ Redis" {
  style.fill: "#f3e5f5"
}

app -> ops -> ser -> conn
```

**Fig. 1.** Template serializes keys/values then talks to Redis through the connection factory.

## Serialization defaults

By default, **`RedisTemplate`** (and **`RedisCache`**) use **`JdkSerializationRedisSerializer`** for most operations. Keys must be **non-null**; values may be null only if the serializer allows it. Prefer JSON (or another non-JDK format) in production — see [[Why should you avoid JdkSerializationRedisSerializer]] and [[What serialization strategy should you use with RedisTemplate]].

Repositories (`@RedisHash`) and **`RedisTemplate`** solve different jobs: entity CRUD vs ad-hoc Redis commands — see [[What is the difference between RedisHash and RedisTemplate]].

> [!warning] Default JDK serialization is a security footgun
> Official docs warn that Java native serialization can run untrusted bytecode on deserialize. Do not leave the default serializer in untrusted environments; prefer JSON or another format.

> [!warning] Serializer mismatch looks like “missing keys”
> Writing with one serializer and reading with another yields opaque bytes or failed deserialization. Align key/value/hash serializers across every client of the same keyspace (apps, cache, session).

> [!tip] Interview answer
> `RedisTemplate` is Spring Data Redis’s main high-level client: it implements `RedisOperations`, serializes keys/values, and exposes `opsFor*` views per Redis data type. Configure a `RedisConnectionFactory` and replace the default JDK serializer. For plain strings, `StringRedisTemplate` is the convenient specialization.

See [[How do you use opsForValue with RedisTemplate]], [[What is the difference between RedisTemplate and StringRedisTemplate]], and [[Why should you avoid JdkSerializationRedisSerializer]].
