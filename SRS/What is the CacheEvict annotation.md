<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is the `CacheEvict` annotation?

> [!abstract] Short answer
> **`@CacheEvict` marks a method that removes cache entries** so later `@Cacheable` calls do not keep stale data. Default: evict **one key after a successful** invoke. **`allEntries = true`** clears the whole named cache(s). **`beforeInvocation = true`** evicts **before** the method, even if it throws.

## Evict as a trigger

Spring *The @CacheEvict Annotation*: unlike `@Cacheable`, these methods **act as eviction triggers**. `void` is fine — the return value is ignored. Options include cache names, key / `keyGenerator`, `condition`, plus **`allEntries`** and **`beforeInvocation`**.

```java
@CacheEvict(cacheNames = "books", key = "#isbn")
public void deleteBook(String isbn) {
    catalog.delete(isbn);
}

@CacheEvict(cacheNames = "books", allEntries = true)
public void loadBooks(InputStream batch) {
    catalog.replaceAll(batch);
}
```

**Listing 1.** Key eviction vs region wipe — second snippet follows the Framework `allEntries` example. Default key is all parameters if `key` is omitted.

**`allEntries = true`:** one operation clears the region; per-key evict would be slow. `CacheEvict` javadoc: combining **`allEntries = true` with `key`** is **not allowed**. The reference also notes a specified key is irrelevant for a full clear.

**`beforeInvocation`:** default **`false`** — evict **after success** only (exception → **no** evict). **`true`** — evict **always before** invoke, **regardless of outcome**. Use when eviction must not depend on the method succeeding.

As of **6.1**, after-invocation evict waits for `CompletableFuture` / reactive completion.

```d2
direction: down
call: "Advised call" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
when: "beforeInvocation?" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
before: "evict, then invoke" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}
after: "invoke; evict only if success" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

call -> when
when -> before: "true"
when -> after: "false (default)"
```

**Fig. 1.** Default ties eviction to a successful method. Several evicts: [[What is the Caching annotation]]. Related knobs: [[What is allEntries on CacheEvict]], [[What is beforeInvocation on CacheEvict]].

> [!warning] Failed method + default timing keeps the old entry
> If `update` throws and `beforeInvocation` is false, the cache is **not** cleared — it may still hold a value that no longer matches the DB. That is the opposite of “evict after failure.” Use **`beforeInvocation = true`** only when you **want** a miss even if the write fails (cache empty, DB unchanged).

> [!warning] `allEntries` is a coarse flush
> On a **local** `ConcurrentMapCacheManager`, it clears **this JVM only**. Other nodes keep stale maps. A shared store (Redis) sees one region clear. Prefer keyed evict when you can.

> [!warning] Still proxy-bound
> `this.deleteBook(...)` never evicts in default proxy mode — [[Why might the Cacheable annotation not work]].

> [!tip] Interview answer
> **`@CacheEvict` drops a key or a whole cache so reads do not stay stale.** Default is after a successful call. `allEntries = true` wipes the region (do not also set `key`). `beforeInvocation = true` evicts first, even if the method throws.
