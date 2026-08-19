<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A @RedisHash type is stored as a Redis Hash plus optional index sets and a TTL.

Dump layout for @RedisHash(value = "sessions") id abc-123-def:

- Hash sessions:abc-123-def with fields including _class, userId, email, createdAt
- Index set sessions:userId:user:1001 containing the entity id (from @Indexed)
- TTL on the hash (from timeToLive / @TimeToLive)

The repository extends CrudRepository. Use @RedisHash for simple CRUD; RedisTemplate for sorted sets, streams, and pub/sub.
> [!warning] Unverified traps from the dump
> - _class is stored on the hash for type information.
> - Index sets are extra keys, not fields inside the hash.
