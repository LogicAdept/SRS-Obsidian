<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Caching #SRS

# What is the difference between cache-aside and write-through in Spring?

> [!abstract] Short answer
> Spring’s `@Cacheable` path **is cache-aside**: get-if-absent, then invoke, then put. A **write-through-shaped** update is **`@CachePut`**: the method **always runs** (your DB write) and the **return value is stored**. **`@CacheEvict` after a write** is cache-aside **invalidation** — the next read reloads. Spring does **not** implement a separate write-through cache product.

## Two write strategies on the same SPI

*Understanding the Cache Abstraction*: method caching is the usual **get-if-not-found-then-put** block. That is **cache-aside** (lazy load). The app owns the database; the cache is an optional shortcut.

| | Cache-aside (typical Spring) | Write-through-shaped |
| --- | --- | --- |
| Read | `@Cacheable` — skip method on hit | Same, or always go to DB |
| Write | DB commit, then **`@CacheEvict`** | DB write **and** **`@CachePut`** of the new value |
| After write | Brief miss, then reload | Cache already has the new object |
| Cost | Extra read after evict | Write always pays put; may store unread keys |

```java
@Cacheable("books")
public Book find(ISBN isbn) { return catalog.load(isbn); }

@CacheEvict(cacheNames = "books", key = "#isbn")
public void delete(ISBN isbn) { catalog.delete(isbn); }

@CachePut(cacheNames = "books", key = "#isbn")
public Book update(ISBN isbn, BookDescriptor descriptor) {
    return catalog.update(isbn, descriptor);
}
```

**Listing 1.** Aside reads + evict-on-delete + put-on-update. Contrast: [[What is the difference between Cacheable and CachePut]].

Spring never calls this “write-through” in the reference. `@CachePut` is **cache population without skipping the method** — your code still writes the DB; the interceptor only **`Cache.put`s** the return value.

```d2
direction: right
aside: "write DB → @CacheEvict\nnext @Cacheable reloads" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
wt: "write DB in method\n@CachePut stores result" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
```

**Fig. 1.** Both are AOP around **your** method, not a DB engine that writes cache and SQL atomically.

> [!warning] `@Cacheable` on a write is not write-through
> A hit **skips** the update. Use `@CachePut` or `@CacheEvict`, not Cacheable, on mutating methods.

> [!warning] Evict vs put
> Evict is simpler and avoids caching unread data; readers pay a miss. Put keeps read-your-writes on that key if the **same key** is used. Annotations do not pick a strategy for you.

> [!warning] Not JPA second-level write-through
> Hibernate/JPA cache modes are a **different** stack (`jakarta.persistence.Cacheable`). This card is Spring **method** cache.

> [!tip] Interview answer
> **`@Cacheable` is cache-aside: miss, load, put.** After a write, either **evict** (aside) or **`@CachePut`** (keep the new value in cache). Spring has no separate write-through cache — `@CachePut` just always runs the method and puts the result.
