<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The abstraction itself does not define TTL; the provider does. Redis dump: `RedisCacheConfiguration.defaultCacheConfig().entryTtl(Duration.ofHours(1))`. Caffeine dumps use expire-after-write in the cache spec. Concurrent map default has no TTL.

> [!warning] Unverified traps from the dump
> - `@Cacheable` has no `ttl` attribute in these dumps.

