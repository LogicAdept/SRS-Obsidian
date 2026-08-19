<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Abstraction is provider-agnostic. Boot picks from the classpath. Lists include ConcurrentMap (default), EhCache, Caffeine, Redis, JCache (e.g. Hazelcast). Add `spring-boot-starter-cache` plus the provider (Caffeine or `spring-data-redis`).

Decision-style dump: multiple instances → Redis; data bigger than heap → EhCache with disk; production single node → Caffeine; otherwise concurrent map is fine.

> [!warning] Unverified traps from the dump
> - Hibernate L2 and CDN/Varnish are other caching layers, not this `CacheManager` list.

