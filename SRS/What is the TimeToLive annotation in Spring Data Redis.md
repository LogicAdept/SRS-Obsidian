<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #Java/Annotations #SRS

# What is the TimeToLive annotation in Spring Data Redis?

> [!abstract] Short answer
> **`@TimeToLive`** marks a **numeric property or method** on a **`@RedisHash`** aggregate whose value becomes the Redis key **expiration**. It **supersedes** `@RedisHash(timeToLive=…)` / keyspace defaults. Default unit is **seconds** (`unit` optional). Do not put `@TimeToLive` on both a field and a method in the same class.

## Fixed vs per-entity TTL

Class-level fixed expiry (seconds):

```java
@RedisHash(value = "sessions", timeToLive = 1800) // 30 minutes for every instance
class Session { /* … */ }
```

Per-instance / computed expiry with `@TimeToLive`:

```java
@RedisHash("sessions")
class Session {
  @Id String id;

  @TimeToLive // optional: unit = TimeUnit.SECONDS
  private Long expiration; // positive → EXPIRE; property reads back TTL/PTTL (−1 = no expiry)
}

@RedisHash("sessions")
class DynamicSession {
  @Id String id;

  @TimeToLive
  public long getTimeToLive() {
    return premium ? 7200L : 3600L;
  }
}
```

**Listing 1.** Class `timeToLive` vs property/method `@TimeToLive` (Spring Data Redis expirations reference / `TimeToLive` Javadoc).

```d2
direction: right
entity: "@RedisHash save" {
  style.fill: "#e3f2fd"
}
ttl: "@TimeToLive value\nor @RedisHash.timeToLive" {
  style.fill: "#fff3e0"
}
exp: "EXPIRE on hash key" {
  style.fill: "#e8f5e9"
}
ev: "Optional keyspace\nexpiry events" {
  style.fill: "#f3e5f5"
}

entity -> ttl -> exp -> ev
```

**Fig. 1.** Repository save applies expiration; Spring can listen for Redis keyspace notifications to publish `RedisKeyExpiredEvent`.

## Events and indexes

Positive TTL runs `EXPIRE`. Repository support may keep a short-lived **phantom** copy so apps can receive **`RedisKeyExpiredEvent`** after the original key is gone (configurable via `@EnableRedisRepositories` / keyspace events). Enabling the listener may alter Redis `notify-keyspace-events` (problematic on some managed Redis offerings).

> [!warning] One `@TimeToLive` source only
> Annotate **either** a numeric property **or** a method — not both. The annotated property **overrides** other timeout configuration (`@RedisHash.timeToLive` included).

> [!warning] Secondary indexes can outlive the hash
> Redis Pub/Sub expiry messages are not durable. If a key expires while the app is down, **`@Indexed` sets may keep stale ids**. Redis cannot expire individual set members used as indexes — residual cleanup relies on those events.

> [!tip] Interview answer
> `@TimeToLive` on a `@RedisHash` entity supplies a per-object Redis TTL in seconds by default and beats the class-level `timeToLive` attribute. I use a Long field for dynamic expiry or a method for computed TTL, never both. Class-level `timeToLive` is enough when every instance shares the same lifetime.

See [[How do you store a Redis value with a TTL]], [[How does Spring Data Redis store a RedisHash entity]], and [[How do Indexed fields work in a Spring Data Redis repository]].
