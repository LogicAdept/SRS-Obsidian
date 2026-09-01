<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Versions #SRS

# When was `NavigableMap` introduced for `TreeMap`?

> [!abstract] Short answer
> **Java 6** — interface and methods are `Since: 1.6`. `TreeMap` itself is **`Since: 1.2`** (`SortedMap`). Java 5’s `TreeMap` implements `SortedMap`, not `NavigableMap`. Floor/ceiling/poll, descending views, and inclusive range overloads are the 1.6 surface.

## The class is 1.2; navigation is 1.6

`NavigableMap` extends `SortedMap` and is documented `Since: 1.6`. `TreeMap` is a red-black `NavigableMap` today, but the **class** arrived with the Collections Framework (`Since: 1.2`). On Java 5 the type line is `implements SortedMap, Cloneable, Serializable` — no `NavigableMap` yet ([[In which Java version was TreeMap introduced]], [[What interfaces does TreeMap implement]]).

What 1.6 added on that same tree:

- Closest-match lookup: `lower*` / `floor*` / `ceiling*` / `higher*` (key and entry)
- Ends that return `null` when empty: `firstEntry` / `lastEntry` / `pollFirstEntry` / `pollLastEntry`
- `descendingMap` / `navigableKeySet` / `descendingKeySet`
- Inclusive `subMap` / `headMap` / `tailMap` overloads; two-arg `subMap(from, to)` stays the old half-open `SortedMap` shape

`NavigableMap` still declares the two-arg range methods as returning `SortedMap` so older `SortedMap` implementations could be **retrofitted**. `TreeMap` overrides them as navigable views ([[How do you get a range or neighbor key from a TreeMap]]). Order is still `Comparable` or a constructor `Comparator` — that part is not new in 6.

Java 21 later adds `SequencedMap` (`putFirst` / `putLast` throw on `TreeMap`). That is not when navigation arrived.

```d2
direction: right
v12: "1.2\nTreeMap\nSortedMap" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}
v5: "5.0\nstill SortedMap\nonly" {
  width: 180
  height: 80
  style.fill: "#fff3e0"
}
v16: "1.6\nNavigableMap\nfloor / poll / …" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
v12 -> v5 -> v16
```

**Fig. 1.** Do not date the **class** from the **interface**. Concurrent skip lists are also 1.6 ([[What is the difference between TreeMap and ConcurrentSkipListMap]]).

```java
import java.util.NavigableMap;
import java.util.TreeMap;

class Demo {
    static void layer16() {
        NavigableMap<Integer, String> m = new TreeMap<>();
        m.put(1, "a");
        m.put(3, "c");
        m.subMap(1, 3);   // SortedMap API, 1.2
        m.floorKey(2);    // NavigableMap, 1.6
        m.ceilingKey(2);  // 1.6
        m.pollFirstEntry(); // 1.6 — removes
    }
}
```

**Listing 1.** Same `TreeMap` object. Half-open `subMap` is the old layer; `floorKey` / `pollFirstEntry` exist only from 1.6.

> [!warning] “TreeMap came in Java 6” is the dump collapse
> The red-black tree and `SortedMap` methods (`firstKey`, two-arg `subMap`) are 1.2. **JDK 6 / 1.6** is `NavigableMap` on that class. Javadoc writes **1.6**, not “JDK 6.0.”

> [!warning] `floorKey` is not `firstKey`
> `firstKey` throws on an empty 1.2 map. `floorKey` / `ceilingKey` return `null` when there is no neighbor. Mixing those APIs is mixing two generations.

> [!tip] Interview answer
> **`NavigableMap` is Java 6 (`Since: 1.6`) — floor, ceiling, poll, descending, inclusive ranges. `TreeMap` is Java 1.2 as a `SortedMap`. Java 5 still has no `NavigableMap`. Do not say the class was introduced in 6.**
