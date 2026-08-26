<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is `CachingConfigurer`?

> [!abstract] Short answer
> **`CachingConfigurer` is the `@EnableCaching` callback for global cache infrastructure:** which **`CacheManager`**, **`CacheResolver`**, **`KeyGenerator`**, and **`CacheErrorHandler`** annotation-driven caching uses. Implement it on a **`@Configuration`** class. **`@Bean` on `cacheManager()` / `cacheResolver()` is required** so the instance is a context bean. Use it to pick among **several** managers.

## Explicit global wiring

`EnableCaching` javadoc: by type lookup is enough for a **single** `CacheManager`. `CachingConfigurer` makes the relationship **explicit** (two managers, custom keys, custom errors).

Methods (all **default**, nullable):

| Method | Default if unused |
| --- | --- |
| `cacheManager()` | —; builds a default `CacheResolver` behind the scenes |
| `cacheResolver()` | `SimpleCacheResolver` on that manager |
| `keyGenerator()` | `SimpleKeyGenerator` |
| `errorHandler()` | `SimpleCacheErrorHandler` (rethrows to the caller) |

If **both** `cacheManager()` and `cacheResolver()` are set, the **manager is ignored**.

```java
@Configuration
@EnableCaching
class AppConfig implements CachingConfigurer {

    @Bean
    @Override
    public CacheManager cacheManager() {
        SimpleCacheManager manager = new SimpleCacheManager();
        manager.setCaches(Set.of(new ConcurrentMapCache("default")));
        return manager;
    }

    @Override
    public KeyGenerator keyGenerator() {
        return new MyKeyGenerator();
    }
}
```

**Listing 1.** Conceptual pattern from `EnableCaching` / `CachingConfigurer` javadoc. The `@Bean` on `cacheManager()` is **mandatory** for lifecycle. Resolver details: [[What is CacheResolver]]. Enablement: [[What is the EnableCaching annotation]].

```d2
direction: down
en: "@EnableCaching +\nCachingConfigurer" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
g: "cacheManager / cacheResolver\nkeyGenerator / errorHandler" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
aop: "CacheInterceptor uses them" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

en -> g -> aop
```

**Fig. 1.** Global layer under `@CacheConfig` and method attributes. JCache uses **`JCacheConfigurer`**.

**Early initialization:** do **not** `@Autowired` common fields on the config class; use a lazy **`ObjectProvider`**. Operation-level `cacheManager`/`keyGenerator` still override these defaults.

> [!warning] Missing `@Bean` on `cacheManager()`
> The method runs as a config callback but the manager may **not** be a managed bean (lifecycle, injection). Javadoc marks `@Bean` as **important**.

> [!warning] Two resolvers
> Setting `cacheResolver()` discards `cacheManager()` for annotation-driven resolution. Do not expect both to apply.

> [!tip] Interview answer
> **`CachingConfigurer` is how `@EnableCaching` config supplies the global `CacheManager`, resolver, key generator, and error handler.** Put `@Bean` on `cacheManager()`. Use it when more than one manager exists or you need a custom `KeyGenerator`. Method annotations can still override per operation.
