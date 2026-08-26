<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Framework/AOP #Java/Annotations #SRS

# How does `Cacheable` work internally?

> [!abstract] Short answer
> **`@EnableCaching`** registers **`CacheInterceptor`** (`MethodInterceptor`) on an AOP proxy (or weaves an AspectJ aspect). On an advised call, **`CacheAspectSupport`** reads **`CacheOperation`s**, builds a **key**, **`CacheResolver`** picks **`Cache`** instances from a **`CacheManager`**, then **`Cache.get`**. Hit: unwrap **`ValueWrapper`**, skip the method. Miss: **`invokeOperation`**, then **`Cache.put`**.

## Interceptor, then `Cache` SPI

Enablement javadoc: `@EnableCaching` / `<cache:annotation-driven/>` register **`CacheInterceptor`** and the proxy- or AspectJ advice that weaves it in. `CacheInterceptor` is a thread-safe AOP Alliance interceptor; the algorithm lives in **`CacheAspectSupport`**: **`CacheOperationSource`** (what to do), **`KeyGenerator`** (key), **`CacheResolver`** (which `Cache`s). `AbstractCacheInvoker` talks to the store via **`doGet` / `doPut`**, routing failures to **`CacheErrorHandler`** (`doGet` error → treated as miss if the handler does not throw).

Spring *Understanding the Cache Abstraction*: this is **not** a cache product. Storage is **`org.springframework.cache.Cache`** + **`CacheManager`**. JDK path is often **`ConcurrentMapCache`** (`ConcurrentHashMap`). Annotation meaning: [[What is the Spring Cacheable annotation]].

```java
// Cache SPI — miss vs cached null
Cache.ValueWrapper wrap = cache.get(key);
if (wrap != null) {
    return wrap.get(); // may be null (cached null / empty Optional)
}
Object value = method.invoke(); // invokeOperation on miss
cache.put(key, value);
```

**Listing 1.** Conceptual `get`/`put` (see `Cache` javadoc). A bare **`null` from `get`** means **no mapping**; a wrapper that holds `null` is a cached empty. `sync=true` uses **`Cache.get(key, Callable)`** so the loader runs once per key (provider-dependent).

```d2
direction: down
proxy: "CacheInterceptor.invoke" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
meta: "CacheOperationSource\nKeyGenerator · CacheResolver" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
store: "Cache.get / Cache.put\n(CacheManager)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

proxy -> meta -> store
```

**Fig. 1.** The interceptor never runs for `this.cached()` or `@PostConstruct` in default **proxy** mode — [[Why might the Cacheable annotation not work]], [[Why does a self-invocation skip Spring AOP advice]].

`condition` is evaluated **before** the method (no cache use if false). `unless` **after** a miss invoke (can see `#result`) and can skip **put**. Multi-cache `@Cacheable({"a","b"})`: check in order; on hit still **put** into the caches that missed.

Proxy kind is the usual Spring AOP choice (JDK vs CGLIB / Boot default). Private methods are not advised in proxy mode. AspectJ `mode` rewrites bytecode so local calls participate (`spring-aspects` + weaving).

> [!warning] Errors can look like misses
> If `Cache.get` throws and `CacheErrorHandler` swallows it, **`doGet` returns null** — the method runs and a **put** may still happen (`sync=false`). `sync=true` is a **combined** get-or-load; a failed initial access has **no** separate put.

> [!warning] TTL is not in the interceptor
> Eviction, TTL, and clustering are **provider** settings. The abstraction only **get/put/evict** through `Cache`.

> [!tip] Interview answer
> **`CacheInterceptor` sits on the Spring AOP proxy, computes a key, and calls `Cache.get`.** Hit returns the wrapper value and skips the method; miss invokes then `put`. It is cache-aside over a `CacheManager`, not an inlined `ConcurrentHashMap` in your service.
