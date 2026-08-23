<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Data/Redis #SRS

# How do you invalidate Spring Cache in a cluster?

> [!abstract] Short answer
> With a **shared Redis** `CacheManager`, `@CacheEvict` or `Cache.evict` removes keys in Redis and every node stops hitting stale entries. With **local** caches (`ConcurrentMapCacheManager` or Caffeine per JVM), eviction on one instance does not reach others — broadcast invalidation or use a shared store.

## Shared Redis vs local JVM caches

Spring’s `@Cacheable` / `@CacheEvict` delegate to the configured `CacheManager`. Behavior in a cluster depends on whether all nodes read the same backing store.

```java
@CacheEvict(cacheNames = "products", key = "#id")
public void updateProduct(Long id, ProductDto dto) {
  productRepository.save(toEntity(dto));
}
```

**Listing 1.** Declarative eviction after a write (Spring Framework `@CacheEvict`).

| Setup | Cluster behavior |
|-------|------------------|
| `RedisCacheManager` (shared Redis) | One node’s `@CacheEvict` deletes the Redis key; all nodes miss on next read |
| `ConcurrentMapCacheManager` / local Caffeine | Eviction is JVM-local; other pods keep stale entries |

For programmatic clears, `Cache.evict(key)` removes one entry; `RedisCache.clear()` / pattern `invalidate` wipe a cache namespace. Prefer **`invalidate`** when you need immediate visibility — `evict` may be deferred (transactional decorators, lock-free writer).

```d2
direction: down
nodeA: "Pod A @CacheEvict" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
redis: "RedisCacheManager\n(shared keys)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
nodeB: "Pod B next @Cacheable\n→ cache miss" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
local: "Local CacheManager\n(other JVMs untouched)" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}

nodeA -> redis -> nodeB
nodeA -> local: "no shared store"
```

**Fig. 1.** Shared Redis centralizes entries; local managers need an explicit broadcast path.

## When you must broadcast

If some layers keep **local** caches (HTTP client cache, second-level in-memory layer, or hybrid), publish an invalidation event after writes: Redis Pub/Sub, messaging (Kafka/Rabbit), or Spring Cloud Bus. Subscribers call `cacheManager.getCache("products").evict(id)` on their JVM. Short TTL alone is eventual consistency, not explicit invalidation.

With **Redis Cluster**, treat Redis as the shared cache backend normally — but do not rely on **keyspace notifications** for cross-node invalidation signals; cluster docs warn keyspace events are not replicated across shards.

> [!warning] `@CacheEvict` is not cross-JVM magic
> It only touches caches your `CacheManager` controls on **this** application context. Local maps need a message or a shared Redis backend. Even with Redis, configure one `RedisCacheManager` bean cluster-wide and align key serializers ([[What serialization problems happen with Redis Spring Cache]]).

See [[How do you use Redis as a Spring CacheManager]] and [[How do you implement Redis Pub Sub with Spring Data Redis]].

> [!tip] Interview answer
> In a cluster I use a shared `RedisCacheManager` so `@CacheEvict` drops keys in Redis and every pod sees the miss. If caches are local per JVM, I broadcast invalidation events and evict on each node, or I accept TTL-based staleness. Local `ConcurrentMapCacheManager` never propagates evicts to other instances.
