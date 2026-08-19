<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Data Redis talks to Redis through a client library.

**Lettuce** (Boot default since 2.0): Netty-based, thread-safe, one shared connection, async and reactive (`ReactiveRedisTemplate`). Pooling is optional.

**Jedis:** synchronous, not thread-safe, needs a connection pool (one connection per thread). Choose it for legacy or specific pipeline-heavy workloads; you typically exclude Lettuce and add Jedis.

> [!warning] Unverified traps from the dump
> - Sharing one Jedis instance across threads is unsafe.
> - “Lettuce needs no pool” is about the default non-blocking connection; blocking commands can still use a pool.
