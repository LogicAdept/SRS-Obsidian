<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS

# What is the difference between RedisTemplate and StringRedisTemplate?

> [!abstract] Short answer
> **`RedisTemplate<K,V>`** is the general Spring Data Redis API with **configurable serializers** (default JDK serialization for many operations). **`StringRedisTemplate`** is a **`RedisTemplate<String, String>`** specialization preconfigured with **`StringRedisSerializer`**, so keys and values stay human-readable UTF-8 strings with less setup.

## Same ops, different serialization defaults

Both expose the same `opsForValue` / `opsForHash` / … views and implement `RedisOperations`. The difference is how Java types become Redis bytes.

| | `RedisTemplate` | `StringRedisTemplate` |
| --- | --- | --- |
| Type params | Any `K`, `V` | Fixed `String`, `String` |
| Default serializers | Often JDK for values | `StringRedisSerializer` throughout |
| Typical use | Objects / JSON / custom codecs | Counters, tokens, plain string payloads |
| Callbacks | `RedisConnection` | `StringRedisConnection` |

```java
@Bean
StringRedisTemplate stringRedisTemplate(RedisConnectionFactory factory) {
  return new StringRedisTemplate(factory);
}

@Bean
RedisTemplate<String, User> userRedisTemplate(RedisConnectionFactory factory) {
  RedisTemplate<String, User> template = new RedisTemplate<>();
  template.setConnectionFactory(factory);
  template.setKeySerializer(RedisSerializer.string());
  template.setValueSerializer(RedisSerializer.json());
  return template;
}
```

**Listing 1.** String convenience template vs typed template with explicit serializers (Spring Data Redis template docs / `StringRedisTemplate` Javadoc).

```d2
direction: right
generic: "RedisTemplate<K,V>\nconfigurable serializers" {
  style.fill: "#e3f2fd"
}
string: "StringRedisTemplate\nStringRedisSerializer" {
  style.fill: "#e8f5e9"
}
bytes: "Redis bytes" {
  style.fill: "#f3e5f5"
}

generic -> bytes
string -> bytes
```

**Fig. 1.** Both write bytes to Redis; mismatched serializers look like missing or garbled keys.

## Choosing

Prefer **`StringRedisTemplate`** for intensive string work (cache keys, feature flags, simple lists of strings). Prefer a configured **`RedisTemplate`** (or JSON serializers) when values are domain objects. Jedis/Lettuce are **connection drivers**, not alternate template types — see [[What is the difference between Lettuce and Jedis in Spring Data Redis]].

> [!warning] Serializer mismatch ≠ “owned by one template”
> Redis stores opaque bytes. A key written with JDK serialization will not decode correctly with `StringRedisTemplate` (and vice versa). Align serializers across every client of the same keyspace — there is no separate Redis namespace per Java template class.

> [!warning] Default `RedisTemplate` JDK serialization
> Unconfigured `RedisTemplate` often uses **`JdkSerializationRedisSerializer`**, which is unsafe for untrusted data and produces non-readable values. See [[Why should you avoid JdkSerializationRedisSerializer]].

> [!tip] Interview answer
> `StringRedisTemplate` is a `RedisTemplate<String,String>` already wired with `StringRedisSerializer` for readable string keys/values. Generic `RedisTemplate` needs serializers configured for your value types and defaults toward JDK serialization. Same Redis commands; different encoding of what you put on the wire.

See [[What is RedisTemplate]], [[How do you use opsForValue with RedisTemplate]], and [[What serialization strategy should you use with RedisTemplate]].
