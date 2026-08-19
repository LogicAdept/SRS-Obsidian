<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Custom `CacheManager` wrapping Caffeine (L1, local) and Redis (L2, distributed). Get: L1, then L2, then compute and write both. Put/evict both. Short L1 TTL. Optional Redis pub/sub to drop L1 on other nodes.

> [!warning] Unverified traps from the dump
> - Not a built-in Boot annotation; dumps describe a custom `CacheManager`.

