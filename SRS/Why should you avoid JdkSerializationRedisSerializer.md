<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`JdkSerializationRedisSerializer` is the historical default. It stores Java serialized bytes: unreadable in `redis-cli`, Java-only, brittle when the class changes (`serialVersionUID`), larger than JSON, and a deserialization-gadget risk.

Prefer `StringRedisSerializer` for keys and `GenericJackson2JsonRedisSerializer` (or a typed `Jackson2JsonRedisSerializer`) for values.

> [!warning] Unverified traps from the dump
> - Changing a domain class silently breaks JDK-serialized cache entries.
> - JSON with `@class` (`GenericJackson2JsonRedisSerializer`) is polyglot-hostile if other languages must read the key; still better than JDK serialization for Java services.
