<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is the difference between `condition` and `unless` on `Cacheable`?

> [!abstract] Short answer
> **`condition` is evaluated before the method: if it is false, Spring ignores the cache entirely** (always invoke, never get/put). **`unless` is evaluated after a miss invoke: if it is true, the return value is not stored.** Only **`unless`** (and puts/evicts after invoke) can use **`#result`**.

## Before vs after

Spring *Conditional Caching* and `Cacheable` javadoc:

| | `condition` | `unless` |
| --- | --- | --- |
| When | **Before** invoke | **After** invoke (on the miss path) |
| Meaning | Cache this call if **true** (empty string → always) | **Veto the put** if **true** (empty → never veto) |
| `#result` | **No** | **Yes** (`Optional` unwrapped) |
| If it “fails” | No cache lookup, no store | Method still ran; result not put |

```java
@Cacheable(
    cacheNames = "book",
    condition = "#name.length() < 32",
    unless = "#result.hardback")
public Book findBook(String name) {
    return catalog.find(name);
}

@Cacheable(cacheNames = "book", unless = "#result == null")
public Book findBookOrNull(String isbn) { /* ... */ }
```

**Listing 1.** Official-style `condition` on the argument; `unless` on the entity (`#result.hardback`). For `Optional<Book>`, `#result` is still `Book` — use `#result?.hardback`. Sibling: [[What is the Spring Cacheable annotation]].

```d2
direction: down
cond: "condition SpEL" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
get: "Cache.get" {
  width: 160
  height: 50
  style.fill: "#fff3e0"
}
invoke: "invoke method" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
un: "unless SpEL" {
  width: 180
  height: 50
  style.fill: "#fce4ec"
}
put: "Cache.put" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}

cond -> get: "true"
cond -> invoke: "false: skip cache"
get -> invoke: "miss"
invoke -> un
un -> put: "false"
```

**Fig. 1.** `condition == false` never reaches `get`. A **hit** never evaluates `unless` because the method is skipped. `sync = true` **does not support `unless`**.

On `@CachePut`, **`condition` runs after** the method (put nature) and **may** use `#result` — do not copy the Cacheable timing blindly ([[What is the difference between Cacheable and CachePut]]).

> [!warning] `#result` in `condition` is not defined
> The SpEL table lists `#result` only for **`unless`**, cache **put** key/condition, and **evict** when `beforeInvocation` is false. Putting `#result == null` in `condition` on `@Cacheable` is the usual swap mistake.

> [!warning] `unless` does not skip the method
> The expensive call still happens on a miss; you only skip **storing** (for example nulls or hardbacks). To skip both lookup and invoke based on **inputs**, use `condition`.

> [!tip] Interview answer
> **`condition` is a before-gate on arguments: false means no cache at all.** **`unless` is an after-gate on the return value: true means do not put.** Only `unless` sees `#result`. They are not interchangeable.
