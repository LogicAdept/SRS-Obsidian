<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: rarely changing, frequently read data → simple cache-aside; changing data → TTL or event eviction. Multi-instance → Redis; huge data → EhCache disk; production single JVM → Caffeine; otherwise concurrent map.

Do not cache data that changes constantly; watch size and TTL so you do not OOM or serve stale rows.

> [!warning] Unverified traps from the dump
> - Hibernate L1 is a different cache, not a `CacheManager` choice.

