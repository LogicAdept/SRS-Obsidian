<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Iteration/FailFast #SRS

# Are `ConcurrentHashMap` iterators fail-fast?

> [!abstract] Short answer
> **No.** Iterators (and spliterators) from `ConcurrentHashMap` views are **weakly consistent**: they **never** throw `ConcurrentModificationException`. They reflect the table state at some point at or after the iterator was created and may (but need not) observe later updates. That is the opposite of fail-fast maps such as [[Are IdentityHashMap iterators fail-fast]].

## Fail-fast vs weakly consistent

```d2
direction: right
ff: "Fail-fast\nHashMap / IdentityHashMap\nmodCount → CME" {
  width: 260
  height: 100
  style.fill: "#ffebee"
}
wc: "Weakly consistent\nConcurrentHashMap\nno CME" {
  width: 260
  height: 100
  style.fill: "#e8f5e9"
}
ff -> wc: "not this"
```

**Fig. 1.** Fail-fast iterators detect structural races with `ConcurrentModificationException`. Concurrent map iterators skip that check on purpose.

`java.util.concurrent` documents weakly consistent traversal for most concurrent collections:

* may run while other threads update the map;
* will never throw `ConcurrentModificationException`;
* traverse each element that existed at construction **exactly once**, and **may** reflect later modifications.

`ConcurrentHashMap` class docs say the same for iterators, spliterators, and enumerations: they do not throw `ConcurrentModificationException`. View APIs (`keySet`, `values`, `entrySet`) state that their iterators and spliterators are weakly consistent. Iterators are still meant for **one thread at a time**.

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("a", 1);

Iterator<String> it = map.keySet().iterator();
map.put("b", 2); // concurrent structural change
while (it.hasNext()) {
    System.out.println(it.next()); // no ConcurrentModificationException
}
```

**Listing 1.** A put while iterating does not abort the iterator; you may or may not see `"b"` depending on timing and table state.

## Not a CopyOnWrite snapshot

Interview dumps often say “fail-safe = clone.” That describes **`CopyOnWriteArrayList` / `CopyOnWriteArraySet`**: mutative ops copy the array; iterators walk an immutable snapshot. `ConcurrentHashMap` does **not** clone the whole map for each iterator — it walks the live table with weakly consistent rules. Prefer [[What is the difference between HashMap and ConcurrentHashMap]] for the concurrency model, not CopyOnWrite.

> [!warning] “Fail-safe” is not a JDK term here
> Official wording is **weakly consistent**. “Fail-safe” in interviews usually only means “no CME.” It does **not** mean you see a frozen full-map snapshot or a deterministic mix of updates.

> [!warning] Do not rely on which updates appear
> The iterator may miss a mapping inserted after creation, or may observe it. Aggregate helpers like `size()` / `isEmpty()` are also only rough under concurrent updates — fine for monitoring, not for control decisions.

> [!tip] Interview answer
> **`ConcurrentHashMap` iterators are not fail-fast.** They are weakly consistent: no `ConcurrentModificationException`, one pass over entries that existed at construction, and optional visibility of later puts/removes. That is different from `HashMap`’s fail-fast `modCount` check and different from CopyOnWrite’s array snapshot.
