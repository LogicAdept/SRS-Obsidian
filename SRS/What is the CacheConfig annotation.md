<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Class-level defaults: shared cache names, `KeyGenerator`, `CacheManager`, or `CacheResolver`. Methods can omit repeating `cacheNames`. It does not enable caching by itself.

> [!warning] Unverified traps from the dump
> - You still need `@EnableCaching` and a method-level `@Cacheable` / `@CachePut` / `@CacheEvict`.

