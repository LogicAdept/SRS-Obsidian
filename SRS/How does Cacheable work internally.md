<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring wraps the bean in an AOP proxy. On an external call, `CacheInterceptor` builds the key (`KeyGenerator` or SpEL), then `Cache.get(key)`. Hit: return cached value, skip the method. Miss: invoke, `Cache.put`, return. Proxy is CGLIB (class) or JDK (interface).

Self-invocation, `@PostConstruct`, and private methods never hit that interceptor.

> [!warning] Unverified traps from the dump
> - Same proxy story as `@Transactional`: `this.cached()` does not cache.
> - Cache advice is not available during `@PostConstruct` the way dumps describe for other AOP annotations.

