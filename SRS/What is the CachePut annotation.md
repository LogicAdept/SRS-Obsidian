<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is the `CachePut` annotation?

> [!abstract] Short answer
> **`@CachePut` always invokes the method**, then **puts the return value** into the named cache(s) when `condition` / `unless` allow it. Unlike **`@Cacheable`**, a cache hit **does not skip** the method. Use it to **populate or refresh** an entry (create/update), not to avoid work.

## Always run, then put

Spring *The @CachePut Annotation*: update the cache **without interfering with method execution**. Same option set as `@Cacheable`: `cacheNames`/`value`, `key`, `keyGenerator`, `cacheManager`/`cacheResolver`, `condition`, `unless`. Official example:

```java
@CachePut(cacheNames = "book", key = "#isbn")
public Book updateBook(ISBN isbn, BookDescriptor descriptor) {
    return catalog.update(isbn, descriptor);
}
```

**Listing 1.** From the Framework reference — the method runs; the returned `Book` is stored under `#isbn`. Contrast skip-on-hit: [[What is the Spring Cacheable annotation]].

`CachePut` javadoc: **`Optional`** is unwrapped; present content is stored. **`condition`** is evaluated **after** the invoke (put nature) and **may use `#result`**. **`unless`** vetoes the put if true (`#result` allowed). `key` and `keyGenerator` are mutually exclusive; `cacheManager` and `cacheResolver` likewise. Default key is all parameters (`SimpleKeyGenerator`) unless `key` is set.

As of **6.1**, `CompletableFuture` and reactive return types put when the produced object is available.

```d2
direction: down
call: "Advised call" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
run: "Always invoke method" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
put: "Cache.put(key, result)\nif condition/unless allow" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

call -> run -> put
```

**Fig. 1.** `@Cacheable` would branch to “return cached” before invoke. Side-by-side: [[What is the difference between Cacheable and CachePut]].

This is still Spring’s **method cache-aside** SPI (`Cache.put`), not JPA write-through to the database. Pair with `@CacheEvict` on delete, or several puts/evicts via `@Caching` — [[What is the Caching annotation]].

> [!warning] Do not stack `@Cacheable` and `@CachePut` on one method
> Spring **strongly discourages** it: skip vs always-invoke conflict. Exclusive `condition`s are the documented corner case, and those conditions **must not** use `#result` (checked up front).

> [!warning] Side-effect methods belong on `@CachePut` (or no cache skip)
> `@Cacheable` on `updateBook` would skip the update on a hit and return a **stale** cached book. `@CachePut` keeps the write.

> [!warning] Exception → no put
> If the method throws, there is no successful result to store. Evict-on-failure is a separate `@CacheEvict(beforeInvocation = true)` concern.

> [!tip] Interview answer
> **`@CachePut` always runs the method and then writes the return value into the cache.** Use it on create/update so the cache stays current. `@Cacheable` is for reads that may skip the method. Do not put both on the same method.
