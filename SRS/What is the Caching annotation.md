<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Caching` groups several cache operations on one method — dumps say when you need `@CachePut` and `@CacheEvict` together, or multiple `@CacheEvict`/`@CachePut` with different keys or caches.

> [!warning] Unverified traps from the dump
> - It does not replace `@EnableCaching`.

