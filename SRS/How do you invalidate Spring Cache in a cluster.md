<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump approaches: short TTLs; domain events (Kafka/Rabbit) so consumers evict; Redis pub/sub; Spring Cloud Bus broadcast. Pick from consistency needs vs ops complexity.

Local `ConcurrentMapCacheManager` cannot see another node’s evict.

> [!warning] Unverified traps from the dump
> - `@CacheEvict` on one instance does not clear other JVMs unless the store is shared (Redis) or you broadcast.

