<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

TTL can be set at class, field, or method level on a @RedisHash entity.

Class-level: @RedisHash(value = "sessions", timeToLive = 1800) — 30 minutes for all instances.

Field-level: @TimeToLive private Long expiration; dynamic per entity (dump: seconds remaining; -1 means no expiry). This overrides the class-level TTL.

Method-level: @TimeToLive on a getter, e.g. return isPremiumUser ? 7200L : 3600L.
> [!warning] Unverified traps from the dump
> - Field-level @TimeToLive overrides the annotation on @RedisHash.
> - Secondary @Indexed sets may outlive a TTL'd hash.
