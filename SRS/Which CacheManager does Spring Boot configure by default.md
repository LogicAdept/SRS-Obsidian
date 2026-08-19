<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Boot/AutoConfiguration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

If no other `CacheManager` is defined, Boot uses a simple in-memory `ConcurrentMapCacheManager`. Dumps also say Spring’s default is a concurrent hashmap you can replace by registering another `CacheManager`.

> [!warning] Unverified traps from the dump
> - That default has no TTL, no size cap, and no clustering — dumps treat it as development/testing, not production multi-node.
> - Adding Caffeine or Redis on the classpath changes what Boot auto-configures.

