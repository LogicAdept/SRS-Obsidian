<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Framework/AOP #Java/Annotations #SRS

# Why might the Cacheable annotation not work?

> [!abstract] Short answer
> **`@Cacheable` is AOP-driven** — it runs only when caching is **enabled**, the call goes **through the Spring proxy**, the method is **public** (in default proxy mode), returns a **cacheable result**, and any **`condition` / `unless`** SpEL passes. Violating any of these makes caching appear “silent”: the method runs every time with no error.

## Activation and proxy rules

1. **`@EnableCaching` missing** — annotation processing is off until you add **`@EnableCaching`** on a **`@Configuration`** class (or **`cache:annotation-driven`** in XML).

2. **Self-invocation** — in default **`mode = proxy`**, only **external** calls through the proxy are intercepted. **`this.cachedMethod()`** inside the same bean **does not cache**, even if the target method carries **`@Cacheable`**. Use **`aspectj`** weaving or refactor to another bean. See [[Why does a self-invocation skip Spring AOP advice]].

3. **Non-public methods** — with proxies, annotate **public** methods on **concrete classes**. **`protected` / private / package-private`** methods compile fine but **ignore caching settings** (no error).

```java
@Service
public class BookService {

    @Cacheable("books")
    public Book findByIsbn(String isbn) { /* cached via proxy */ }

    @Cacheable("books")
    private Book internalLookup(String isbn) { /* never cached in proxy mode */ }
}
```

**Listing 1.** Conceptual split — external calls hit the cache aspect; self-calls and non-public methods do not (proxy mode).

## Return type and SpEL conditions

4. **`void` return on `@Cacheable`** — **`@Cacheable` requires a result** to store. **`void` methods** suit **`@CacheEvict`** (trigger semantics); they do not populate a cache entry.

5. **`condition` evaluates to `false`** — caching is skipped and the method runs every time, as if uncached.

6. **`unless` vetoes after invocation** — even when the method runs, the return value may be **not stored** (for example **`unless="#result.hardback"`**).

7. **Failed invocation** — cache population happens on **successful completion** with a result. If the method **throws**, no value is added (same post-success semantics as other cache annotations).

```d2
direction: right
call: "External call\nvia proxy" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
self: "this.method()\nself-invocation" {
  width: 180
  height: 60
  style.fill: "#fce4ec"
}
cache: "@Cacheable\ninterceptor" {
  width: 160
  height: 60
  style.fill: "#e3f2fd"
}

call -> cache
self -> cache: "bypasses\n(proxy mode)"
```

**Fig. 1.** Proxy-mode caching applies to inbound calls through the Spring proxy.

> [!warning] Different failure modes
> **Cache stampede**, **Redis connection errors**, and **serializer mismatches** can break caching at runtime but are **infrastructure problems**, not the “annotation silently does nothing” checklist above. Those throw or log via the configured **`CacheErrorHandler`**. See [[What is the difference between Cacheable and CachePut]].

> [!tip] Interview answer
> @Cacheable fails silently when @EnableCaching is off, when you self-invoke or use a non-public method in proxy mode, when the method is void, when condition/unless SpEL skips caching, or when the method throws before a result exists. External calls through the proxy on public methods with a return value are the baseline that works.
