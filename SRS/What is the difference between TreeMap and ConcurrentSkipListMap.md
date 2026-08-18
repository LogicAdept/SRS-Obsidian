<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview dumps: when many threads share a sorted map, prefer **`ConcurrentSkipListMap`** over a **synchronized `TreeMap`** (same idea as `ConcurrentHashMap` vs synchronized `HashMap`).

A comparison dump:

- `TreeMap`: `java.util`, **not synchronized**, **fail-fast** view iterators (`ConcurrentModificationException` on structural change). Introduced **JDK 2**. Implements `Map` / `SortedMap` / `NavigableMap`.
- `ConcurrentSkipListMap`: `java.util.concurrent`, described as **synchronized**, **fail-safe** iterators. Introduced **JDK 6**. Also `ConcurrentNavigableMap`.
- Both: sorted by natural key order (or a constructor `Comparator`); **no null key** (`NullPointerException`); dump also says **many null values**; `put`/`get` **O(log n)**.

Dumps say unsynchronized `TreeMap` is **faster**; the concurrent map is **slower** because it is “synchronized.”

> [!warning] Unverified traps from the dump
> - “Synchronized” for `ConcurrentSkipListMap` is dump wording (two threads “cannot access at the same time”). Other concurrency dumps call it a concurrent / lock-free skip list, not a single monitor.
> - Same dump claims both maps allow many null **values**; other concurrent-map dumps forbid nulls on skip-list maps. Verify in fill.
> - `synchronizedSortedMap(new TreeMap<>())` is the wrapper dumps contrast with `ConcurrentSkipListMap`.
