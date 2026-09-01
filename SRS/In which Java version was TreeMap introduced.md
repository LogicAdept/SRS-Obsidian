<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Versions #SRS

# In which Java version was `TreeMap` introduced?

> [!abstract] Short answer
> **Java 1.2** — the Collections Framework release. The class javadoc is `Since: 1.2`. `NavigableMap` (floor/ceiling/poll, inclusive ranges) is **1.6**. `ConcurrentSkipListMap` is also **1.6**, not a 1.2 twin of `TreeMap`.

## `Since: 1.2`, then a 1.6 navigable layer

`TreeMap` shipped with `SortedMap`, `Map`, and the four constructors still on the type: natural order, `Comparator`, copy-from-`Map` (natural order), copy-from-`SortedMap` (keep that order). It is documented as a member of the Java Collections Framework.

Java 6 added `NavigableMap`. `TreeMap` then gained `floorKey` / `ceilingKey` / `lowerKey` / `higherKey`, `pollFirstEntry` / `pollLastEntry`, `descendingMap`, and the inclusive `subMap` / `headMap` / `tailMap` overloads (`Since: 1.6` on those methods). The two-argument `subMap(from, to)` half-open view is the older `SortedMap` shape. Details: [[When was NavigableMap introduced for TreeMap]], [[What interfaces does TreeMap implement]].

The concurrent ordered map is not a 1.2 `TreeMap` variant: `ConcurrentSkipListMap` is `Since: 1.6` ([[What is the difference between TreeMap and ConcurrentSkipListMap]]). `putFirst` / `putLast` on `TreeMap` throw and are `Since: 21` (`SequencedMap`).

```d2
direction: right
v12: "1.2\nTreeMap\nSortedMap" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}
v16: "1.6\nNavigableMap\nConcurrentSkipListMap" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
v21: "21\nputFirst / putLast\nUOE" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
v12 -> v16
v16 -> v21
```

**Fig. 1.** Class vs later interfaces. Neighbor APIs: [[How do you get a range or neighbor key from a TreeMap]].

```java
import java.util.NavigableMap;
import java.util.TreeMap;

class Demo {
    static void since12Vs16() {
        var m = new TreeMap<Integer, String>(); // type exists since 1.2
        m.put(1, "a");
        m.subMap(1, 2);     // SortedMap range, 1.2
        m.floorKey(1);      // NavigableMap, 1.6
        NavigableMap<Integer, String> n = m;
        n.ceilingKey(1);
    }
}
```

**Listing 1.** Same class, two layers: the tree is 1.2; `floorKey` / `ceilingKey` are 1.6.

> [!warning] Do not answer “Java 6” for `TreeMap` itself
> Interview tables mix **when the class appeared** with **when `NavigableMap` methods appeared**. `TreeMap` is 1.2. Floor/ceiling/poll are 1.6. Javadoc writes **1.2** / **1.6**, not “JDK 2.0” / “JDK 6.0”.

> [!warning] “Java 2” is a brand, not `Since: 2.0`
> 1.2 is the Collections Framework version number on the class. Saying “JDK 2.0” as if it were a `Since` tag is dump shorthand. Pair the number with the fact: Collections Framework, red-black `SortedMap`.

> [!tip] Interview answer
> **`TreeMap` is Java 1.2, with the Collections Framework — `Since: 1.2` on the class. `NavigableMap` methods on that same type are Java 6. `ConcurrentSkipListMap` is also Java 6. Do not collapse those three dates.**
