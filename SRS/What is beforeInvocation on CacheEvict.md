<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is `beforeInvocation` on `CacheEvict`?

> [!abstract] Short answer
> **`beforeInvocation` chooses when eviction runs.** **`false` (default):** evict **after** the method **succeeds** — an exception means **no** evict. **`true`:** evict **before** the method, **even if it throws**. Use `true` when the cache must drop regardless of the outcome.

## After success vs always first

Spring *The @CacheEvict Annotation* and `CacheEvict` javadoc:

* Default **`false`**: same as other cache annotations — the action runs when the method **completes successfully**. If the method is **not invoked** (another cache skip) or **throws**, eviction **does not** occur.
* **`true`:** eviction **always** happens **before** invoke, **irrespective of the method outcome**.

```java
@CacheEvict(cacheNames = "books", key = "#isbn")
public void deleteBook(String isbn) {
    catalog.delete(isbn); // evict only if this succeeds
}

@CacheEvict(cacheNames = "books", key = "#isbn", beforeInvocation = true)
public void deleteBookAlwaysDropCache(String isbn) {
    catalog.delete(isbn); // cache already cleared; DB may still fail
}
```

**Listing 1.** Conceptual contrast. Parent: [[What is the CacheEvict annotation]]. Region wipe still honors this flag: [[What is allEntries on CacheEvict]].

`#result` is **not** available when eviction is **before** invoke (SpEL table: `#result` on evict only if `beforeInvocation` is **false**).

```d2
direction: down
def: "beforeInvocation=false" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
ok: "invoke OK → evict" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
fail: "throw → keep cache entry" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}

def -> ok
def -> fail
```

**Fig. 1.** After-success keeps cache aligned with a rolled-back write; before-invoke can leave a **miss** while the row **still exists**.

As of **6.1**, **after-invocation** evict on `CompletableFuture` / reactive types waits until processing **completes**. Before-invocation still fires immediately before the call.

> [!warning] Evict-first + failed delete
> Cache miss, database row **still there**. The next `@Cacheable` reloads from DB (often fine) — or you served a gap if something else read the cache as source of truth. Do not assume “evict first” means the delete committed.

> [!warning] Default does **not** evict on exception
> A failed `update` leaves the **old** cached value. That can be **stale relative to a partial write**, or **correct** if the TX rolled back. Match the flag to whether you trust the method outcome.

> [!tip] Interview answer
> **Default `beforeInvocation = false` evicts only after a successful method.** **`true` evicts first, even if the method throws** — useful when you must not keep a cached value tied to a write that might fail. The trade-off is an empty cache while the database is unchanged.
