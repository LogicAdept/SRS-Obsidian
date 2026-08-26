<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is the `CacheConfig` annotation?

> [!abstract] Short answer
> **`@CacheConfig` (since 4.1) is a class-level default** for cache **names**, **`KeyGenerator`**, **`CacheManager`**, and **`CacheResolver`**. Method-level `@Cacheable` / `@CachePut` / `@CacheEvict` can omit repeating `cacheNames`. It **does not enable** caching and **does not** mark methods as cached by itself.

## Shared defaults, three override layers

Spring *The @CacheConfig Annotation*: repeating the same cache name on every method is tedious. Put the name (and optional generator / manager / resolver) on the class:

```java
@CacheConfig("books")
public class BookRepositoryImpl implements BookRepository {

    @Cacheable
    public Book findBook(ISBN isbn) {
        return catalog.load(isbn);
    }

    @CacheEvict(key = "#isbn")
    public void deleteBook(String isbn) {
        catalog.delete(isbn);
    }
}
```

**Listing 1.** Official-style example: `@Cacheable` with no `cacheNames` inherits `"books"`. `value` is an alias for `cacheNames` (javadoc since 6.2.9).

**Override order** (most specific wins):

1. **Global** — `CachingConfigurer` / `@EnableCaching` setup
2. **Class** — `@CacheConfig`
3. **Operation** — attributes on `@Cacheable`, `@CachePut`, `@CacheEvict`

An operation-level `cacheNames`, `keyGenerator`, `cacheManager`, or `cacheResolver` **replaces** the class default for that method. Provider TTL/size still live on the **`CacheManager` bean** (for example `CaffeineCacheManager`), not on `@CacheConfig`.

```d2
direction: down
g: "CachingConfigurer / EnableCaching" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
c: "@CacheConfig on the class" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
m: "@Cacheable / @CachePut / @CacheEvict" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}

g -> c -> m
```

**Fig. 1.** Class defaults fill in what the method leaves blank. Enablement is separate: [[What is the EnableCaching annotation]]. Global hooks: [[What is CachingConfigurer]].

`cacheManager` is used to build a default `CacheResolver` when none is set on the operation or via `cacheResolver()`. `cacheNames` are resolved through that resolver (`CacheManager.getCache`).

> [!warning] Not an on-switch
> `@CacheConfig` alone does **nothing** at runtime. You still need **`@EnableCaching`** (or XML) **and** a method-level cache operation. A class with only `@CacheConfig` is not cached.

> [!warning] Not a substitute for `@Cacheable`
> Inheriting the name does not imply `@Cacheable` on every method. Unannotated methods are ordinary calls.

> [!warning] Interface vs class
> Defaults apply to cache operations **defined in that class**. Prefer the annotation on the **concrete** type that carries the operations (same AOP visibility rules as other cache annotations).

> [!tip] Interview answer
> **`@CacheConfig` shares cache names and key/manager/resolver defaults across a class** so methods can say just `@Cacheable`. Method attributes override it; `CachingConfigurer` is the global layer. It does not turn caching on — `@EnableCaching` does.
