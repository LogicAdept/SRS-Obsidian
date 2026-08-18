<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Sorting #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: default is **natural order** (`Comparable` / `compareTo`). Custom order: pass a **`Comparator` at construction**.

```java
SortedMap<Integer, String> sortedCache = new TreeMap<>(Collections.reverseOrder());
sortedCache.putAll(cache);
```

Another dump sorts strings by length: `new TreeMap<>(Comparator.comparing(String::length))`.

Natural order examples: `Integer` ascending, `String` lexicographic.

> [!warning] Unverified traps from the dump
> - The comparator is fixed at creation; dumps do not show changing order later.
> - A length comparator can return `0` for unequal strings (`"One"` vs `"Two"`); that collides with uniqueness. Dumps still print both — verify in fill.
