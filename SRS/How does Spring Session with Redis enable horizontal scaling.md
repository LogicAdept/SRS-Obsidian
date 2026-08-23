<!--
reps: 0
priority: 0
-->
#Java/Spring/Session #Java/Spring/Data/Redis #SRS

# How does Spring Session with Redis enable horizontal scaling?

> [!abstract] Short answer
> Spring Session stores the servlet **`HttpSession`** in a **shared Redis** store instead of JVM memory. Any app instance that can reach Redis can load the same session by id, so you can scale out and roll instances **without sticky sessions** or container-specific clustering.

## The scaling problem

With the container’s in-memory `HttpSession`, each node keeps its own sessions. A load balancer must pin a user to one instance (sticky sessions), and a rolling restart or failover can drop session state that lived only on that JVM.

Spring Session’s goal, per the reference docs, is **clustered sessions without tying you to an application-container solution**: put session data in shared storage (here Redis) so every node reads and updates the same session.

```d2
direction: right
lb: "Load balancer\n(no sticky required)" {
  style.fill: "#e3f2fd"
}
a1: "App instance A" {
  style.fill: "#fff3e0"
}
a2: "App instance B" {
  style.fill: "#fff3e0"
}
redis: "Redis\nshared sessions" {
  style.fill: "#e8f5e9"
}

lb -> a1
lb -> a2
a1 -> redis
a2 -> redis
```

**Fig. 1.** Shared Redis session storage: any instance can serve any request that carries the session id.

## How Redis-backed HttpSession works

1. Add **`spring-session-data-redis`** (Boot: **`spring-boot-starter-session-data-redis`**) and a **`RedisConnectionFactory`**.
2. Enable Redis sessions with **`@EnableRedisHttpSession`**, or rely on Boot auto-configuration (which replaces the need for that annotation when the Redis session starter is on the classpath).
3. That setup registers a servlet filter bean named **`springSessionRepositoryFilter`**. The filter swaps the container `HttpSession` for a Spring Session implementation backed by Redis.
4. The browser still sends a **session-id cookie**; each request loads/saves that session from Redis.

New instances during a deploy see existing sessions as soon as they connect to the same Redis namespace — there is nothing sticky left in app memory.

```java
@Configuration(proxyBeanMethods = false)
@EnableRedisHttpSession
public class SessionConfig {

  @Bean
  LettuceConnectionFactory connectionFactory() {
    return new LettuceConnectionFactory();
  }
}
```

**Listing 1.** Minimal Java config from the Spring Session Redis HttpSession guide (`@EnableRedisHttpSession` + `RedisConnectionFactory`).

## Serialization, flush mode, cookies

By default Spring Session uses **Java serialization** for session attributes. Prefer a JSON `RedisSerializer` bean named **`springSessionDefaultRedisSerializer`** when apps or class versions share Redis — same class of risk as default JDK serializers elsewhere.

**`FlushMode`** (annotation `flushMode`, Boot `spring.session.redis.flush-mode`):

- **`ON_SAVE`** (default) — write Redis when `SessionRepository.save` runs (typically just before the HTTP response commits).
- **`IMMEDIATE`** — write on create / attribute changes as soon as they happen.

Customize the session cookie (name, path, domain, Secure, SameSite, …) by exposing a **`CookieSerializer`** / **`DefaultCookieSerializer`** bean.

> [!warning] Sticky sessions are optional, Redis is not free
> Shared Redis removes the need for affinity, but Redis becomes critical path: availability, latency, namespace collisions (`spring.session.redis.namespace`), and serializer compatibility across instances all matter.

> [!tip] Interview answer
> Put `HttpSession` in Redis via Spring Session’s `springSessionRepositoryFilter`. Every node loads the session by cookie id from the same store, so you scale horizontally and roll deploys without sticky sessions or container clustering.

See [[What is RedisTemplate]], [[What serialization strategy should you use with RedisTemplate]], and [[Why should you avoid JdkSerializationRedisSerializer]].
