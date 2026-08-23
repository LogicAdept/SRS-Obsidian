<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS

# What is the difference between RedisHash and RedisTemplate?

> [!abstract] Short answer
> **`@RedisHash`** marks a domain type for **Spring Data Redis repositories**: the object is stored as a Redis **hash** (`keyspace:id`) with optional TTL and `@Indexed` helper sets. **`RedisTemplate`** is the **general command API** (`opsForValue`, `opsForHash`, lists, ZSets, pub/sub, streams) where you choose keys, structures, and serializers yourself.

## Repository mapping vs template commands

| | `@RedisHash` + repository | `RedisTemplate` |
| --- | --- | --- |
| Abstraction | Entity CRUD like other Spring Data modules | Explicit Redis operations |
| Storage shape | Flattened hash + index/keyspace SETs | Whatever structure you call |
| Setup | `@EnableRedisRepositories` | `RedisConnectionFactory` + serializers |
| Best for | Simple domain objects, indexed finders | ZSET boards, streams, pub/sub, ad-hoc keys |

```java
@RedisHash("people")
class Person {
  @Id String id;
  @Indexed String firstname;
}

interface PersonRepository extends CrudRepository<Person, String> {}

// Template — any structure
redis.opsForZSet().add("leaderboard", "alice", 42);
redis.convertAndSend("channel", payload);
```

**Listing 1.** Hash-mapped entity vs free-form template commands (Spring Data Redis repositories + template docs).

Repositories still need a `RedisTemplate` (often `byte[]` keys/values) in configuration for the mapping infrastructure — but **application code** usually talks to `PersonRepository` for entities and to a typed `RedisTemplate` for everything else.

```d2
direction: right
hash: "@RedisHash entity\nCrudRepository" {
  style.fill: "#e3f2fd"
}
store: "Redis Hash\npeople:id + indexes" {
  style.fill: "#e8f5e9"
}
tmpl: "RedisTemplate\nopsFor*" {
  style.fill: "#fff3e0"
}
other: "Strings Lists ZSets\nPub/Sub Streams" {
  style.fill: "#f3e5f5"
}

hash -> store
tmpl -> other
```

**Fig. 1.** Repositories own the hash-mapping model; the template reaches every Redis data type.

## When each wins

Use **`@RedisHash`** for CRUD aggregates that fit the hash + secondary-index model ([[How does Spring Data Redis store a RedisHash entity]], [[How do Indexed fields work in a Spring Data Redis repository]]). Use **`RedisTemplate`** for sorted sets, streams, pub/sub, pipelines, and custom key designs — see [[What is RedisTemplate]].

> [!warning] `@Indexed` is not a SQL index
> Secondary indexes are **extra Redis SET keys** maintained on save/delete. They cost memory and write amplification; they do not turn Redis into a relational query engine.

> [!warning] Repositories do not replace Streams or ZSET APIs
> There is no repository method that magically becomes a Redis Stream consumer group or a leaderboard ZSET. Those stay on `RedisTemplate` / connection APIs.

> [!tip] Interview answer
> `@RedisHash` is the entity annotation for Redis repositories — Spring maps the object to a hash and optional index sets. `RedisTemplate` is the low-level client for any Redis structure. I use repositories for simple domain CRUD and the template for streams, pub/sub, sorted sets, and custom keys.

See [[How does Spring Data Redis store a RedisHash entity]], [[What is RedisTemplate]], and [[How do you use opsForValue with RedisTemplate]].
