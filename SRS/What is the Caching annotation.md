<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is the `Caching` annotation?

> [!abstract] Short answer
> **`@Caching` groups several cache operations on one method** — nested **`@Cacheable`**, **`@CachePut`**, and **`@CacheEvict`** arrays (`cacheable`, `put`, `evict`). Java forbids repeating the same annotation twice, so two `@CacheEvict`s with different keys or cache names go inside `@Caching`. It does **not** enable the infrastructure; you still need **`@EnableCaching`**.

## Multiple operations, one method

Spring *Declarative Annotation-based Caching*: `@Caching` **regroups** cache operations when you need several of the **same** type, typically because **condition** or **key** differs per cache. The official example evicts two regions with different key rules:

```java
@Caching(evict = {
    @CacheEvict("primary"),
    @CacheEvict(cacheNames = "secondary", key = "#p0")
})
public Book importBooks(String deposit, Date date) {
    // ...
}
```

**Listing 1.** Conceptual pattern from the Spring Framework reference. First eviction uses the default key; the second uses the first method argument.

You can mix types on the same method: `cacheable = {…}`, `put = {…}`, `evict = {…}`. Each nested annotation keeps its own cache names, key, condition, and (for evict) `allEntries` / `beforeInvocation`. Javadoc (since 3.1): `@Caching` may also be a **meta-annotation** for a composed custom annotation.

```d2
direction: down
call: "Advised method call" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
group: "@Caching\ncacheable / put / evict arrays" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ops: "Each nested annotation\n→ its own CacheOperation" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

call -> group -> ops
```

**Fig. 1.** `CacheInterceptor` still runs once; it executes every nested operation. Enabling: [[What is the EnableCaching annotation]]. Evict semantics: [[What is the CacheEvict annotation]].

A common interview pair is “update then drop another view”: `@CachePut` on the entity cache plus `@CacheEvict` on a list cache, both nested in `@Caching`.

> [!warning] `@Caching` is not `@EnableCaching`
> Without annotation processing, nested `@Cacheable` / `@CachePut` / `@CacheEvict` are inert metadata. `@CacheConfig` on the class also does **not** turn caching on.

> [!warning] Do not nest `@Cacheable` and `@CachePut` as a clever combo
> Spring **strongly discourages** `@Cacheable` and `@CachePut` on the **same** method: one wants to **skip** the call, the other **always** invokes. `@Caching` does not make that pairing safe unless the nested `condition`s **exclude** each other up front (and those conditions **must not** use `#result`). Prefer a put-only method or split methods. Contrast: [[What is the difference between Cacheable and CachePut]].

> [!warning] Still a proxy
> Default **proxy** mode: `this.importBooks(...)` never applies the nested operations. Same hole as a lone `@Cacheable` — [[Why might the Cacheable annotation not work]].

> [!tip] Interview answer
> **`@Caching` is the wrapper for several cache annotations on one method** — usually two `@CacheEvict`s or a put plus an evict with different keys. Java cannot repeat `@CacheEvict` twice, so you nest them. It does not start caching; `@EnableCaching` and a `CacheManager` still do. Do not use it to combine `@Cacheable` and `@CachePut` on the same method.
