<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #Java/Annotations #SRS

# How do you store a Redis value with a TTL?

> [!abstract] Short answer
> With **`RedisTemplate`**, use `opsForValue().set(key, value, Duration)` (or `Expiration`) so Redis sets **`EX`** on write. With **`@RedisHash`**, use `@RedisHash(timeToLive = …)` or `@TimeToLive` on a field/method. With **Spring Cache**, configure **`entryTtl`** on `RedisCacheConfiguration` — not on `@Cacheable`.

## `RedisTemplate` string/hash values

`ValueOperations.set` can attach expiry in one command. Spring Data Redis 4.1+ prefers **`Duration`** / **`Expiration`** over `long` + `TimeUnit`.

```java
redisTemplate.opsForValue().set(
    "session:" + id, session, Duration.ofMinutes(30));

// Or set then expire separately:
redisTemplate.opsForValue().set("token:" + id, token);
redisTemplate.expire("token:" + id, Duration.ofHours(1));
```

**Listing 1.** Atomic set-with-TTL vs separate `expire` (Spring Data Redis `ValueOperations` / `RedisTemplate`).

## Repository entities and Spring Cache

For **`@RedisHash`** entities, TTL can be fixed on the type or computed per instance:

```java
@RedisHash(value = "sessions", timeToLive = 1800)
class Session { /* seconds for every instance */ }

@RedisHash("sessions")
class DynamicSession {
  @TimeToLive
  private Long ttlSeconds; // per-entity seconds; do not also @TimeToLive a method
}
```

**Listing 2.** Class-level `timeToLive` or property/method `@TimeToLive` (Spring Data Redis expirations reference).

For **`@Cacheable`**, TTL belongs in cache manager setup:

```java
RedisCacheConfiguration defaults = RedisCacheConfiguration
    .defaultCacheConfig()
    .entryTtl(Duration.ofMinutes(10));
```

**Listing 3.** Default entry TTL for Redis-backed Spring Cache — there is no `ttl` attribute on `@Cacheable`.

```d2
direction: down
tmpl: "RedisTemplate.set\n+ Duration" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
hash: "@RedisHash / @TimeToLive" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
cache: "RedisCacheConfiguration\n.entryTtl(...)" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

tmpl -> hash
cache
```

**Fig. 1.** Three layers — imperative template, Redis repositories, and cache abstraction — each with its own TTL API.

> [!warning] Same Redis `EXPIRE`, different entry points
> Template `SET` with TTL, repository `@TimeToLive`, and cache `entryTtl` all map to Redis expiry but are configured separately. Hot keys with identical TTL can expire together and cause a **cache stampede** — add jitter or proactive refresh in application code. TTL on a hash does not automatically clean secondary `@Indexed` sets unless keyspace handling is enabled.

See [[What is the TimeToLive annotation in Spring Data Redis]], [[How do you use opsForValue with RedisTemplate]], and [[How do you use Redis as a Spring CacheManager]].

> [!tip] Interview answer
> For plain keys I use `redisTemplate.opsForValue().set(key, value, Duration.ofMinutes(30))`. For `@RedisHash` I set `@RedisHash(timeToLive=…)` or `@TimeToLive` on a numeric field. For Spring Cache I configure `RedisCacheConfiguration.entryTtl`, not the annotation. All of them end up as Redis key expiry, but the configuration surface differs.
