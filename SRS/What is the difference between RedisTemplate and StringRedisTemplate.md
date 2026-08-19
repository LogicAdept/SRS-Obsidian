<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump comparison:

StringRedisTemplate can only manage data stored through StringRedisTemplate. RedisTemplate can only manage data stored through RedisTemplate. Jedis is listed separately as a way to connect to Redis.

Spring wraps RedisTemplate so you can work with String, List, Set, Hash, and ZSet. Because keys and values are often java.lang.String, dumps also describe StringRedisTemplate as the string-focused template that uses StringRedisSerializer so stored keys and values stay human-readable.
> [!warning] Unverified traps from the dump
> - Mixed serializers mean a key written with one template may not read with the other.
> - Jedis in this dump is the client, not a third template type.
