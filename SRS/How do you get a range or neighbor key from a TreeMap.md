<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list `NavigableMap` / `SortedMap` methods as the reason to pick `TreeMap`:

- Range: `headMap()`, `tailMap()`, `subMap()`
- Ends: `firstKey()`, `lastKey()`, `pollFirstEntry()`, `pollLastEntry()`
- Neighbors: `floorKey()`, `ceilingKey()`

Example from a dump:

```java
treeMap.subMap(1, 3);      // {1=Banana, 2=Orange}
treeMap.floorKey(2);       // 2
treeMap.ceilingKey(2);     // 2
```

> [!warning] Unverified traps from the dump
> - `subMap` bounds in that example are keys `1` inclusive to `3` exclusive (result has 1 and 2, not 3).
> - These methods are why dumps call TreeMap “richer” than HashMap’s `get`/`put`/`keySet`.
