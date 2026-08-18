<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `TreeMap` is **not thread-safe**. Wrap at **creation** so nothing else keeps the raw map:

```java
SortedMap<Integer, String> sorted =
    Collections.synchronizedSortedMap(new TreeMap<>());
```

Use `Collections.synchronizedMap` for `HashMap` / `LinkedHashMap`, and **`synchronizedSortedMap` for `TreeMap`**. Concurrent alternative named in the same dump: `ConcurrentHashMap` (for hashing maps, not as a drop-in sorted tree).

> [!warning] Unverified traps from the dump
> - Wrap at construction to avoid accidental unsynchronized access.
> - Fail-fast iterators on the collection views throw `ConcurrentModificationException` on a best-effort basis; do not use that as a lock.
