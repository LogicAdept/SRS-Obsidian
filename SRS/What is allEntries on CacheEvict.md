<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is `allEntries` on `CacheEvict`?

> [!abstract] Short answer
> **`allEntries = true` clears every entry in the named cache(s)** in one operation, instead of removing a single key. Default is **`false`**: only the computed **key** is evicted. Do **not** also set **`key`** — `CacheEvict` javadoc forbids that combination.

## Region wipe vs one key

Spring *The @CacheEvict Annotation*: `allEntries` means **cache-wide** eviction. Useful when a batch reload invalidates **all** keys and per-key evict would be slow. Official example:

```java
@CacheEvict(cacheNames = "books", allEntries = true)
public void loadBooks(InputStream batch) {
    catalog.replaceAll(batch);
}

@CacheEvict(cacheNames = "books", key = "#isbn")
public void deleteBook(String isbn) {
    catalog.delete(isbn);
}
```

**Listing 1.** Full-region clear vs keyed delete. Parent: [[What is the CacheEvict annotation]]. Timing still follows **`beforeInvocation`** ([[What is beforeInvocation on CacheEvict]]) — default after **successful** invoke.

The Framework **ignores** a key for a full clear (it does not apply). The annotation contract is stricter: **`allEntries = true` + `key()` is not allowed**.

```d2
direction: right
keyed: "allEntries=false\nCache.evict(key)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
all: "allEntries=true\nCache.clear()" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
```

**Fig. 1.** One named region is emptied; other cache names on the annotation are each cleared.

A method used **only** to wipe (`clearBooksCache()`) is valid: `@CacheEvict` allows **`void`** because the return is ignored.

> [!warning] Coarse and local unless the store is shared
> On **`ConcurrentMapCacheManager`**, `clear()` is **this JVM**. Other nodes keep stale maps. Redis/`JCache` shared regions drop **everyone’s** view of that name — still a blunt hammer on a huge keyspace.

> [!warning] Cost
> Clearing a large Redis hash/region is a **broad invalidation**. Prefer keyed `@CacheEvict` when you know the id. Interviewers still expect `allEntries` as “wipe the cache.”

> [!warning] Do not pair with `key`
> Specifying both is **not allowed**. Drop `key` when you mean a full clear.

> [!tip] Interview answer
> **`allEntries = true` empties the whole named cache in one go**, instead of one key. Use it after a bulk reload. Default is keyed evict; do not set `key` at the same time. On an in-memory map it only clears that process.
