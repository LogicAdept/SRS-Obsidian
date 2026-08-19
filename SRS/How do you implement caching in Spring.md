<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Add `@EnableCaching` and a `CacheManager` bean if you are not using Boot auto-config. Example dumps: `@Bean CacheManager` returning `new ConcurrentMapCacheManager("myCache")`, then `@Cacheable("myCache")` on a service method.

Boot path: `spring-boot-starter-cache`, `@EnableCaching`, then `@Cacheable` / `@CachePut` / `@CacheEvict` on the service. Override `CacheManager` to plug Redis, Caffeine, or EhCache.

> [!warning] Unverified traps from the dump
> - Only public methods on a Spring bean are intercepted; private methods and `this.` calls skip the proxy.

