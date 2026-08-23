<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS

# How do you handle Redis connection failures in Spring?

> [!abstract] Short answer
> Configure **timeouts** on `LettuceClientConfiguration`, rely on Lettuce’s **automatic reconnect** for transient outages, and design the **application layer** to degrade (cache miss → database, circuit breaker, session fallback). Spring Data Redis does not silently substitute another store when Redis is down.

## Client timeouts and reconnect

Spring Boot auto-configures `LettuceConnectionFactory` (Lettuce is the default client). Tune connect and command timeouts so threads fail fast instead of hanging when Redis is unreachable.

```java
@Bean
LettuceConnectionFactory redisConnectionFactory() {
  LettuceClientConfiguration clientConfig = LettuceClientConfiguration.builder()
      .commandTimeout(Duration.ofSeconds(2))
      .shutdownTimeout(Duration.ZERO)
      .build();

  return new LettuceConnectionFactory(
      new RedisStandaloneConfiguration("localhost", 6379), clientConfig);
}
```

**Listing 1.** `commandTimeout` bounds how long each Redis command waits (Spring Data Redis “Drivers” guide).

Default `LettuceClientConfiguration` already enables Lettuce `TimeoutOptions` and a **60s connect timeout**. Official `LettuceConnectionFactory` docs: **Lettuce automatically reconnects** until the native connection is closed. `setValidateConnection(true)` only helps when something closes the shared native connection — it adds a server round-trip on each `getConnection()` and defaults to **false**.

Boot properties (when not overriding the factory manually): `spring.data.redis.timeout` (command timeout), `spring.data.redis.connect-timeout`, and Lettuce pool settings under `spring.data.redis.lettuce.pool.*` for blocking/transactional work.

```d2
direction: down
fail: "Redis unreachable\nor slow" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
timeout: "commandTimeout\nfail fast" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
reconnect: "Lettuce auto-reconnect\n(transient)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
app: "App degradation\n(cache miss, breaker)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}

fail -> timeout
fail -> reconnect
timeout -> app
```

**Fig. 1.** Infrastructure handles timeouts/reconnect; business code decides fallback when errors propagate.

## Application degradation (your code)

Spring Cache with `RedisCacheManager` **throws** on Redis errors — it does not auto-read the database. For cache-aside, catch failures (or use a circuit breaker such as Resilience4j around Redis calls) and **load from the source of truth** on miss/error. That is a deliberate degradation path, not a built-in Spring Data Redis feature.

Same pattern for [[How do you use Redis as a Spring CacheManager]] reads, session storage, and pub/sub: decide whether outage means fail the request, serve stale data, or fall back (for example in-memory sessions only in non-prod). Monitor Lettuce/Redis via Boot **Micrometer** metrics (`spring.data.redis` timers/spans when observability is enabled) and connection pool stats.

> [!warning] Reconnect ≠ business continuity
> Lettuce may restore the TCP connection while in-flight commands still failed. Auto-reconnect does not replay lost cache writes or missed Pub/Sub messages. Treat Redis as optional only where you explicitly code a fallback — fixing the cluster is still the real fix.

See [[What is the difference between Lettuce and Jedis in Spring Data Redis]] and [[What is RedisTemplate]].

> [!tip] Interview answer
> I set Lettuce command and connect timeouts, know that Lettuce reconnects automatically for transient blips, and handle sustained failure in application code: cache-aside falls back to the database, optional circuit breakers fail fast, and I monitor `spring.data.redis` metrics. Spring Data Redis itself does not transparently replace Redis with another backend.
