<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Bean RedisCacheManager cacheManager(RedisConnectionFactory factory)` via `RedisCacheManager.builder(factory).build()`. Cluster dumps: Redis (or Hazelcast/Geode) as a shared cache so all instances see the same entries.

TTL example: `RedisCacheConfiguration.defaultCacheConfig().entryTtl(Duration.ofHours(1))`.

> [!warning] Unverified traps from the dump
> - Do not cache Hibernate lazy entities; dumps say serialize DTOs. Jackson/`LocalDateTime` and missing no-arg constructors are listed Redis hazards.

