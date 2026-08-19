<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`CacheManager` is the SPI that creates, looks up, and manages `Cache` instances. Spring Boot picks one from the classpath; you can declare your own `@Bean` for TTL, names, or a specific provider.

Dumps name `ConcurrentMapCacheManager` for local/dev, `EhCacheCacheManager` or `RedisCacheManager` for disk or distributed setups. Choice is framed as performance vs scalability vs persistence.

> [!warning] Unverified traps from the dump
> - Defining a `CacheManager` bean typically replaces Boot auto-config for that type.
> - A named `Cache` must match `cacheNames` / `value` on the annotations.

