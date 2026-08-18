<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Set #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: there is **no `ConcurrentHashSet` class**. Use **`ConcurrentHashMap.newKeySet()`** — a `Set` backed by `ConcurrentHashMap` (dummy values). O(1), concurrent, lock-free reads like the map.

```java
Set<String> seen = ConcurrentHashMap.newKeySet();
seen.add("a");
boolean isNew = seen.add("b"); // false if already present
```

Dump: large write-heavy concurrent set. `CopyOnWriteArraySet` only for **tiny read-mostly**. `ConcurrentSkipListSet` when you need **sorted** order.

> [!warning] Unverified traps from the dump
> - Wrapping `Collections.synchronizedSet(new HashSet<>())` is the older one-lock story, not this API.
