<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@EnableCaching` activates Spring caching. Place it on a `@Configuration` class, often the `@SpringBootApplication` class. It starts a post-processor that looks for cache annotations on public methods and builds a proxy.

Without it, `@Cacheable` does nothing. Boot still auto-configures a simple in-memory `CacheManager` (`ConcurrentMapCacheManager`) if you do not define another.

> [!warning] Unverified traps from the dump
> - The annotation enables processing; it is not itself a cache store.
> - `@CacheConfig` on a class does not turn caching on.

