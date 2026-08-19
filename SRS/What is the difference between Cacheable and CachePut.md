<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Cacheable`: on a hit, skip the method and return the cached value (read / lazy load). `@CachePut`: always execute, then update the cache (write-through). Use `@Cacheable` for expensive reads; `@CachePut` when an update must run and the cache must stay current.

> [!warning] Unverified traps from the dump
> - Both still need `@EnableCaching` and a matching cache name.

