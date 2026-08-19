<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

On RedisTemplate values: opsForValue().set(key, value, Duration.ofMinutes(30)).

On @RedisHash entities: class-level timeToLive on @RedisHash, or per-instance @TimeToLive.

On Spring Cache with Redis: RedisCacheConfiguration.defaultCacheConfig().entryTtl(...) and a per-cache map on RedisCacheManager.

Hot-key dump: jitter TTLs or refresh before expiry to avoid a stampede when many keys expire together.
> [!warning] Unverified traps from the dump
> - @Cacheable has no ttl attribute in these dumps; TTL lives on the cache config.
> - Repository TTL and template SET EX are different APIs for the same Redis expire idea.
