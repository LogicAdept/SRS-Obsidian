<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Caching #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When a hot key expires, many threads miss at once and stampede the DB. Prevention dumps: `@Cacheable(sync = true)` so one thread computes and others wait; distributed lock (`SETNX`); Caffeine `refreshAfterWrite`; jittered TTLs; never-expire plus background refresh for hot keys.

> [!warning] Unverified traps from the dump
> - `sync = true` is local to one JVM; it does not stop a stampede across nodes.

