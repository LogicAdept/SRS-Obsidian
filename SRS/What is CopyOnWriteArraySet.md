<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Set #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: a `Set` **backed by `CopyOnWriteArrayList`**, same snapshot story: lock-free reads, copy-on-write mutations, iterators that never throw. Stores in an **array**; add / `contains` check duplicates with **`equals`**, so add and `contains` are **O(n)** — **no hashing**.

```java
Set<String> tags = new CopyOnWriteArraySet<>();
tags.add("a"); // scans for duplicate, then copies array
```

Dump: tiny, read-mostly sets (a handful of subscribers). For larger or write-heavy sets, prefer **`ConcurrentHashMap.newKeySet()`**.

> [!warning] Unverified traps from the dump
> - O(n) `contains` is easy to miss if you treat it as `HashSet`.
> - `ConcurrentSkipListSet` is the dump’s sorted concurrent set, not this class.
