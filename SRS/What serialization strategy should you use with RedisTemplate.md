<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS

# What serialization strategy should you use with RedisTemplate?

> [!abstract] Short answer
> Prefer **readable string keys** (`StringRedisSerializer`) and **JSON (or another non-JDK format) for values**. Avoid the default **`JdkSerializationRedisSerializer`**. Configure key, value, hash key, and hash value serializers explicitly and keep them identical across every client of the same keyspace.

## Recommended pairing

| Slot | Typical choice | Why |
| --- | --- | --- |
| Key | `StringRedisSerializer` | Readable in `redis-cli`, stable across languages |
| Hash key | `StringRedisSerializer` | Same |
| Value | JSON serializer (`GenericJacksonJsonRedisSerializer` / typed Jackson JSON) | Debuggable, evolvable, Spring-recommended over JDK |
| Hash value | Same JSON strategy as values | Consistency |

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

**Listing 1.** Explicit serializers — do not rely on JDK defaults (Spring Data Redis template / serializers docs).

For string-only workloads, use **`StringRedisTemplate`** (all `StringRedisSerializer`). Typed `JacksonJsonRedisSerializer` binds one target class; **generic** Jackson variants embed type metadata (e.g. `@class`) so polymorphic/`Object` values can round-trip — at the cost of larger payloads and type-whitelist concerns.

```d2
direction: right
app: "Java object / String" {
  style.fill: "#e3f2fd"
}
ser: "RedisSerializer\n(key + value)" {
  style.fill: "#fff3e0"
}
bytes: "Redis bytes" {
  style.fill: "#e8f5e9"
}

app -> ser -> bytes
```

**Fig. 1.** Everything in Redis is bytes; serializers define the contract between apps.

## What to avoid

Official docs warn that default **Java native serialization** enables remote-code risk on deserialize and recommend **other formats such as JSON**. See [[Why should you avoid JdkSerializationRedisSerializer]].

> [!warning] Mismatched serializers look like data loss
> Writing with JSON and reading with JDK (or different key serializers) yields garbage or empty-looking keys. Align serializers for cache, session, and every microservice touching the same Redis DB.

> [!warning] Generic JSON type metadata is not free
> Type hints help deserialization but enlarge values and can widen gadget surfaces if untrusted JSON is accepted. Prefer trusted writers, typed serializers, or a constrained `ObjectMapper` / polymorphic type handling.

> [!tip] Interview answer
> I set string serializers for keys and JSON for values on `RedisTemplate`, and I never leave the JDK default in production. `StringRedisTemplate` is enough when everything is text. The important part is one consistent strategy per keyspace so every node can read what every node writes.

See [[What is RedisTemplate]], [[Why should you avoid JdkSerializationRedisSerializer]], and [[What is the difference between RedisTemplate and StringRedisTemplate]].
