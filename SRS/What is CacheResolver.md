<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is `CacheResolver`?

> [!abstract] Short answer
> **`CacheResolver` (since 4.1) decides which `Cache` instance(s) an advised method uses.** Default **`SimpleCacheResolver`** maps annotation **`cacheNames`** through the configured **`CacheManager`**. A custom resolver can pick caches from **runtime arguments**. **`cacheManager` and `cacheResolver` on the same operation are mutually exclusive.**

## Names vs runtime resolution

`CacheResolver` javadoc: thread-safe functional interface — `Collection<? extends Cache> resolveCaches(CacheOperationInvocationContext<?> context)` (never `null`; failure → `IllegalStateException`).

Spring *Default Cache Resolution*: one manager, names on the annotation → simple resolver. *Custom Cache Resolution*: several managers → per-operation `cacheManager="..."`, **or** replace resolution entirely:

```java
@Cacheable(cacheNames = "books", cacheManager = "anotherCacheManager")
public Book findBook(ISBN isbn) { /* ... */ }

@Cacheable(cacheResolver = "runtimeCacheResolver")
public Book findBook(ISBN isbn) { /* names optional since 4.1 */ }
```

**Listing 1.** Official patterns. Custom bean implements `CacheResolver` (often extends `AbstractCacheResolver`). Known types: `SimpleCacheResolver`, `NamedCacheResolver`, `SimpleExceptionCacheResolver`.

Since **4.1**, `value`/`cacheNames` is **not mandatory** if the resolver supplies the caches. Same exclusivity rule as `key`/`keyGenerator`: specifying **both** `cacheManager` and `cacheResolver` **throws** — the custom resolver **ignores** the manager attribute.

```d2
direction: right
op: "@Cacheable cacheNames\nor no names" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
res: "CacheResolver.resolveCaches" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
c: "Cache / CacheManager" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}

op -> res -> c
```

**Fig. 1.** `CacheInterceptor` asks the resolver on **every** operation. Class defaults: [[What is the CacheConfig annotation]]. Global default: [[What is CachingConfigurer]]. SPI: [[What is CacheManager]].

Boot looks for a `CacheResolver` bean named **`cacheResolver`** as an alternative to auto-configuring a `CacheManager`.

> [!warning] Do not set both `cacheManager` and `cacheResolver`
> The operation fails fast. Pick one: named manager + `cacheNames`, or a resolver that returns `Cache`s itself.

> [!warning] Must return a non-null collection
> Empty might mean “no cache” depending on caller; **`null` is forbidden**. Resolution errors surface as `IllegalStateException`.

> [!tip] Interview answer
> **`CacheResolver` maps a cache operation to one or more `Cache` instances.** The default uses `cacheNames` plus `CacheManager`. Write your own when the cache depends on runtime data, or when `cacheNames` is empty. Do not combine `cacheManager` and `cacheResolver` on the same annotation.
