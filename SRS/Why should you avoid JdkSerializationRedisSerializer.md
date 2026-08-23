<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS

# Why should you avoid JdkSerializationRedisSerializer?

> [!abstract] Short answer
> **`JdkSerializationRedisSerializer`** is the **default** for **`RedisTemplate`** / **`RedisCache`** and stores values with **Java native serialization**. That format is **Java-only**, opaque in `redis-cli`, **brittle** across class changes, and — per Spring Data Redis — a **known deserialization attack surface**. Prefer **JSON** (or another explicit format) and typically **`StringRedisSerializer`** for keys.

## What the default does

Spring Data Redis documents that **`RedisTemplate`** serializes objects with a Java-based serializer by default, and lists **`JdkSerializationRedisSerializer`** as the default for **`RedisCache`** and **`RedisTemplate`**.

Effects in practice:

- Values are **binary Java serialization** — not human-readable in Redis tooling
- Only Java consumers that share compatible classes can decode them
- Changing a domain type (or **`serialVersionUID`**) can make existing keys **unreadable**
- Payload size is often larger than a compact JSON encoding

```java
RedisTemplate<String, Object> template = new RedisTemplate<>();
template.setKeySerializer(RedisSerializer.string());
template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
template.setConnectionFactory(connectionFactory);
template.afterPropertiesSet();
```

**Listing 1.** Conceptual safer setup — string keys and Jackson JSON values instead of JDK serialization (type names vary slightly by Spring Data Redis version).

## Security warning from the reference

The serializers section states that Java native serialization is known for allowing **remote code execution** via payloads that exploit vulnerable libraries during deserialization. Spring’s guidance:

- **Do not use** Java serialization in **untrusted** environments
- **Strongly recommend** another message format such as **JSON**
- If you must keep Java serialization, consider JVM **serialization filters** (JEP 290)

```d2
direction: right
jdk: "JdkSerializationRedisSerializer\n(default)" {
  width: 260
  height: 80
  style.fill: "#fce4ec"
}
json: "JSON serializer\n(+ String keys)" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}

jdk -> json: "prefer for\nnew apps"
```

**Fig. 1.** Move off the JDK default unless you consciously accept its limits.

> [!warning] Silent breakage and gadgets
> Redeploying a changed entity class can leave **stale JDK-serialized cache entries** that fail on read. Separately, **deserializing untrusted Redis content** with the JDK serializer is a classic gadget risk — treat Redis as part of your trust boundary. See [[What serialization strategy should you use with RedisTemplate]] and [[What is the difference between RedisTemplate and StringRedisTemplate]].

> [!tip] Interview answer
> JdkSerializationRedisSerializer is the historical RedisTemplate default: opaque Java bytes, fragile across class changes, and flagged by Spring for deserialization attacks. Prefer String keys and a JSON value serializer unless you have a deliberate reason to keep Java serialization.
