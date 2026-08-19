<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

In-memory `CacheManager` backed by concurrent maps. Dumps use `new ConcurrentMapCacheManager("myCache")` in `@EnableCaching` Java config and call it the lightweight default for standalone or test apps.

> [!warning] Unverified traps from the dump
> - Entries live in the JVM heap of one process; they vanish on restart and are not shared across instances.

