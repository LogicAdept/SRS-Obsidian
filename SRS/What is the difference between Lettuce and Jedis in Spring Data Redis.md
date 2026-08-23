<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS

# What is the difference between Lettuce and Jedis in Spring Data Redis?

> [!abstract] Short answer
> **Lettuce** and **Jedis** are Redis **client drivers**. Spring Data Redis talks to both through **`RedisConnectionFactory`** (`LettuceConnectionFactory` / `JedisConnectionFactory`) so `RedisTemplate` code stays the same. **Lettuce** (Netty) is Spring Boot’s **default**, supports a **reactive** API, and shares a thread-safe **native** connection for non-blocking commands. **Jedis** is a sync client; switch by excluding Lettuce and adding Jedis.

## Drivers under one Spring API

```java
@Bean
LettuceConnectionFactory lettuceFactory() {
  return new LettuceConnectionFactory(new RedisStandaloneConfiguration("localhost", 6379));
}

@Bean
JedisConnectionFactory jedisFactory() {
  return new JedisConnectionFactory(new RedisStandaloneConfiguration("localhost", 6379));
}
```

**Listing 1.** Either factory plugs into `RedisTemplate` (Spring Data Redis Drivers reference).

| Feature (docs overview) | Lettuce | Jedis |
| --- | --- | --- |
| Reactive API | Yes | No |
| Shared native connection (non-blocking) | Default | — |
| Connection pooling | Optional (`commons-pool2`) | Typical / driver-managed |
| Master/replica config | Yes | No (per feature table) |
| Transport | TCP, native epoll/kqueue, Unix sockets | TCP |

```d2
direction: right
app: "RedisTemplate\nRedisOperations" {
  style.fill: "#e3f2fd"
}
factory: "RedisConnectionFactory" {
  style.fill: "#fff3e0"
}
lettuce: "Lettuce\n(Netty, reactive)" {
  style.fill: "#e8f5e9"
}
jedis: "Jedis\n(sync)" {
  style.fill: "#f3e5f5"
}

app -> factory
factory -> lettuce
factory -> jedis
```

**Fig. 1.** Application code depends on Spring Data abstractions; the factory selects the driver.

## Boot default and switching

`spring-boot-starter-data-redis` uses **Lettuce** by default. To use Jedis, exclude `lettuce-core` and add `redis.clients:jedis` (Spring Boot NoSQL how-to).

> [!warning] Do not share `RedisConnection` across threads
> Spring Data’s `RedisConnection` (Lettuce or Jedis wrappers) is **not** thread-safe — especially for transactions, pipelining, and blocking commands. Use **`RedisTemplate`**, which acquires/manages connections safely. Lettuce’s **native** shared connection is a separate story from sharing Spring’s `LettuceConnection` instances.

> [!warning] “Lettuce needs no pool” is incomplete
> Default shared-connection mode covers **non-blocking, non-transactional** work. Blocking/tx paths can use a pool; set `shareNativeConnection` to `false` to dedicate connections. Jedis historically relied more on pooling for concurrency.

> [!tip] Interview answer
> Lettuce and Jedis are Redis clients behind `RedisConnectionFactory`. Boot defaults to Lettuce: Netty-based, reactive-capable, shared native connection for ordinary commands. Jedis is the alternate sync client you opt into by swapping dependencies. I still use `RedisTemplate` so I do not share raw connections across threads.

See [[What is RedisTemplate]], [[How do you handle Redis connection failures in Spring]], and [[What is the difference between RedisTemplate and StringRedisTemplate]].
