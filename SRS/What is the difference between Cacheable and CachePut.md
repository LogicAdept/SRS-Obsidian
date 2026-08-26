<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is the difference between `Cacheable` and `CachePut`?

> [!abstract] Short answer
> **`@Cacheable` is a cache-aside read: on a hit the method is skipped.** **`@CachePut` always runs the method, then writes the return value** into the cache. Same names, keys, and SpEL knobs; opposite control of **whether the method executes**.

## Skip versus always invoke

| | `@Cacheable` | `@CachePut` |
| --- | --- | --- |
| Method on cache **hit** | **Skipped** | **Always invoked** |
| On **miss** | Invoke, then put | Invoke, then put |
| Typical use | Expensive **reads** | **Create/update** that must run |
| Goal | Avoid work | Keep the cache **current** |

Spring: `@Cacheable` **triggers cache population** (lookup first). `@CachePut` updates the cache **without interfering with method execution** — used for **cache population**, not flow optimization.

```java
@Cacheable(cacheNames = "books", key = "#isbn")
public Book findBook(ISBN isbn) {
    return catalog.load(isbn); // skipped on hit
}

@CachePut(cacheNames = "books", key = "#isbn")
public Book updateBook(ISBN isbn, BookDescriptor descriptor) {
    return catalog.update(isbn, descriptor); // always runs
}
```

**Listing 1.** Conceptual pairing — same cache and key so a later `findBook` sees the update. Details: [[What is the Spring Cacheable annotation]], [[What is the CachePut annotation]].

```d2
direction: right
r: "@Cacheable\nhit → skip method" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
w: "@CachePut\nalways invoke → put" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}

r -> w: "do not combine on one method"
```

**Fig. 1.** Spring **strongly discourages** both annotations on the **same** method: skip vs force-invoke. Exclusive `condition`s are the documented exception, and those conditions **must not** use `#result`.

Both still need **`@EnableCaching`** and a **`CacheManager`**. `condition` / `unless` exist on both, but **`@CachePut`’s `condition` runs after the method** (can use `#result`); **`@Cacheable`’s `condition` runs before** (no `#result`) — [[What is the difference between condition and unless on Cacheable]].

This is **not** JPA write-through. `@CachePut` is still `Cache.put` after your method; the database write is your code.

> [!warning] `@Cacheable` on a write skips the write
> A hit returns the **old** cached book and **never** calls `updateBook`. That is the classic interview trap. Use `@CachePut` (or `@CacheEvict`) for mutating methods.

> [!warning] Same key space
> If `findBook` and `updateBook` disagree on `key` or cache name, the put does not refresh the read path.

> [!tip] Interview answer
> **`@Cacheable` may skip the method; `@CachePut` never does.** Use Cacheable for reads, CachePut when the method must run and the return value should replace the cache entry. Do not put both on one method.
