<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Cache is a provider-agnostic abstraction: you annotate methods; a `CacheManager` stores and retrieves values. Dumps say you do not talk to EhCache, Caffeine, or Redis directly from business code. `@EnableCaching` turns the infrastructure on; `@Cacheable`, `@CachePut`, and `@CacheEvict` drive the operations.

Boot auto-configures a `CacheManager` from the classpath. Common providers listed: `ConcurrentMapCacheManager` (default in-memory), EhCache, Caffeine, Redis, JCache/Hazelcast.

> [!warning] Unverified traps from the dump
> - This is not Hibernate first-level cache or JPA `@Cacheable` on an entity (second-level cache).
> - Without `@EnableCaching`, method annotations are ignored.

