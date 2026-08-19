<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

opsForValue() is the string/value view on RedisTemplate.

Dump operations:

- set with TTL: redisTemplate.opsForValue().set("user:1001", user, Duration.ofMinutes(30));
- get: User user = (User) redisTemplate.opsForValue().get("user:1001");
- set if absent (flag/lock): setIfAbsent("lock:order:123", "locked", Duration.ofSeconds(10));
- increment: redisTemplate.opsForValue().increment("page:views:home");

Sibling views in the same dump: opsForHash, opsForList, opsForSet, opsForZSet.
> [!warning] Unverified traps from the dump
> - get returns Object when the template is RedisTemplate<String, Object>; you cast.
> - setIfAbsent with a TTL is the dump's distributed flag pattern, not a full Redisson lock.
