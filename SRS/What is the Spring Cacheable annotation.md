<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is the Spring `Cacheable` annotation?

> [!abstract] Short answer
> **`@Cacheable`** marks a method whose **return value** is stored in a named cache. Next call with the **same key** returns the cached value and **skips** the method. It is **AOP**: **`CacheInterceptor`** on a Spring proxy (default) after **`@EnableCaching`**. You also need a **`CacheManager` bean**.

## Check cache, then maybe invoke

Spring *Declarative Annotation-based Caching*: `@Cacheable` **triggers cache population**. Simplest form names the cache:

```java
@Cacheable("books")
public Book findBook(ISBN isbn) { /* ... */ }
```

**Listing 1.** Official example. Multiple names (`{"books", "isbns"}`): each cache is checked; a hit returns that value and **still puts** into the caches that missed.

Default key (`SimpleKeyGenerator`): no args → `SimpleKey.EMPTY`; one arg → that instance; several → `SimpleKey` of all (need proper `equals`/`hashCode`). Override with SpEL **`key`** (`key="#isbn"`) or a **`keyGenerator`** bean — not both. **`condition`** (before invoke) skips caching if false. **`unless`** (after invoke, may use `#result`) vetoes the put. **`Optional`** is unwrapped; empty Optional stores **`null`**.

Enablement registers **`CacheInterceptor`** and proxy/AspectJ advice (`EnableCaching` javadoc). XML: `<cache:annotation-driven/>`. Failure modes: [[Why might the Cacheable annotation not work]]. Internals: [[How does Cacheable work internally]].

```d2
direction: down
in: "External call via proxy" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
get: "Cache.get(key)" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
hit: "return cached value" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}
miss: "invoke method, Cache.put" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}

in -> get
get -> hit: "hit"
get -> miss: "miss"
```

**Fig. 1.** Only calls that enter the caching advice participate. `@CachePut` on the **same** method as `@Cacheable` is strongly discouraged.

`sync=true` (4.3+): one thread loads a key while others wait — a stampede hint, provider-dependent. Then **`unless` is unsupported**, **only one cache name**, no combined cache ops.

> [!warning] Self-invocation and `@PostConstruct`
> Default **proxy** mode: `this.findBook(...)` **does not cache**. The proxy must be **fully initialized** — do **not** call `@Cacheable` methods from **`@PostConstruct`**. Use another bean after startup, or `mode = ASPECTJ` with weaving. Same AOP hole: [[Why does a self-invocation skip Spring AOP advice]].

> [!warning] No default `CacheManager`
> `@EnableCaching` searches for a **`CacheManager` by type**. There is **no** convention bean the framework invents. Missing it, caching annotations do not magically use a map.

> [!tip] Interview answer
> **`@Cacheable` is Spring’s AOP cache-aside: look up by key, skip the method on hit, put on miss.** Enable with `@EnableCaching` and a `CacheManager`. Keys default to parameters; `condition`/`unless` are SpEL. `this` and `@PostConstruct` never hit the interceptor in proxy mode.
