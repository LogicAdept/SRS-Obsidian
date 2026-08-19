<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Standard `@Cacheable` caches the `Mono`/`Flux` publisher object, not the emitted values, which dumps say breaks. Alternatives listed: `CacheMono`/`CacheFlux` from reactor-extra; `ReactiveRedisTemplate` by hand; `Mono.cache()` for a single in-memory publisher.

> [!warning] Unverified traps from the dump
> - Do not assume servlet `@Cacheable` recipes work on a Netty controller returning `Mono`.

