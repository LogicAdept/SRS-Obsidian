<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`RedisTemplate` is the low-level API: `opsForValue`, `opsForHash`, `opsForList`, `opsForSet`, `opsForZSet`, pub/sub, streams. You control keys, serializers, and data structures.

`@RedisHash` plus a `CrudRepository` maps a Java type onto Redis hashes: id generation, optional `@TimeToLive`, secondary indexes via `@Indexed` (stored as Redis sets). Use it for simple CRUD. Use `RedisTemplate` for sorted sets, streams, pub/sub, or custom commands.

> [!warning] Unverified traps from the dump
> - `@Indexed` is not a SQL index — it is extra Redis sets to maintain.
> - Repository abstraction will not replace Streams or ZSET leaderboards.
