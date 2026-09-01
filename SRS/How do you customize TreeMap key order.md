<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Sorting #SRS

# How do you customize `TreeMap` key order?

> [!abstract] Short answer
> Pass a `Comparator` into the `TreeMap` constructor. With no comparator, or a `null` one, keys use **natural order** (`Comparable.compareTo`). `Collections.reverseOrder()` (or `Comparator.reverseOrder()`) reverses that. `Comparator.comparingInt` / `thenComparing` build a custom total order. `new TreeMap<>(sortedMap)` copies the source map's ordering.

## Ordering is chosen when the map is created

A `TreeMap` is a red-black tree. Every `put`, `get`, `containsKey`, and range view compares keys with that tree's ordering — never with `equals` or `hashCode`. The class offers two empty constructors:

- `new TreeMap<>()` — natural order. Every key must implement `Comparable`, and `k1.compareTo(k2)` must not throw `ClassCastException`.
- `new TreeMap<>(comparator)` — `comparator.compare(k1, k2)` is the order. If `comparator` is `null`, this is the same as natural order.

Two copy constructors: `new TreeMap<>(map)` always uses **natural** order of the keys (it does not keep a `HashMap`'s iteration order). `new TreeMap<>(sortedMap)` copies mappings **and** the source `SortedMap`'s comparator in linear time.

`comparator()` returns that comparator, or `null` for natural order. There is no setter. A reverse **view** (`descendingMap()`, and `reversed()` since 21) has ordering equivalent to `Collections.reverseOrder(comparator())`; the backing map's comparator does not change. `putFirst` / `putLast` throw `UnsupportedOperationException` because position is the comparison method, not an insert-at-end API.

Natural order for `Integer` is signed numeric (smaller first). For `String` it is lexicographic Unicode `compareTo`. `Collections.reverseOrder()` is the reverse of that `compareTo`.

```d2
direction: down
empty: "new TreeMap<>()" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
nat: "natural order\ncompareTo" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
cmp: "new TreeMap<>(c)" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
ord: "c.compare\n(null c → natural)" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
copy: "new TreeMap<>(sortedMap)" {
  width: 260
  height: 50
  style.fill: "#f3e5f5"
}
same: "same comparator\nas the source" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
empty -> nat
cmp -> ord
copy -> same
```

**Fig. 1.** Key order is fixed by the constructor. See [[What types can you use as TreeMap keys]] and [[How does TreeMap decide whether two keys are the same]].

```java
import java.util.Collections;
import java.util.Comparator;
import java.util.TreeMap;

class Demo {
    static void reverseNatural() {
        var m = new TreeMap<Integer, String>(Collections.reverseOrder());
        m.put(1, "a");
        m.put(3, "c");
        m.put(2, "b");
        m.firstKey(); // 3
    }

    static void byLengthThenNatural() {
        var m = new TreeMap<String, Integer>(
                Comparator.comparingInt(String::length)
                        .thenComparing(Comparator.naturalOrder()));
        m.put("bb", 1);
        m.put("a", 2);
        m.put("ccc", 3);
        m.put("aa", 4);
        m.firstKey(); // "a"  — length, then lexicographic
    }

    static void lengthOnlyCollides() {
        var m = new TreeMap<String, Integer>(
                Comparator.comparing(String::length));
        m.put("One", 1);
        m.put("Two", 2);
        m.size();      // 1 — compare returns 0
        m.get("One");  // 2
        m.get("Two");  // 2
    }
}
```

**Listing 1.** Reverse natural order; a length-then-lexicographic comparator that stays consistent with `equals` for `String`; a length-only comparator that collapses `"One"` and `"Two"`. `comparing` / `comparingInt` / `thenComparing` are Java 8.

> [!warning] `compare == 0` means the same key
> The map treats two keys as equal when `compare` (or `compareTo`) returns `0`, even if `equals` is false. A length-only comparator does that for `"One"` and `"Two"`: the second `put` replaces the value, `size` stays 1, and both `get` calls hit that one mapping. Tie-break with `thenComparing` (or do not use a key extractor that is not unique). The `Map` contract also requires the ordering to be consistent with `equals` — see [[Why must TreeMap ordering be consistent with equals]].

> [!warning] Mutually comparable, or `ClassCastException`
> A later `put` whose key cannot be compared with keys already in the tree throws `ClassCastException`. Mixing incomparable types, or a comparator that cannot handle a key (including `null` unless it is `nullsFirst` / `nullsLast`), fails at insertion, not at construction. Null keys under natural order: [[Can TreeMap have null keys or null values]].

> [!tip] Interview answer
> **Default `TreeMap` sorts keys by natural order (`compareTo`). Custom order is a `Comparator` passed to the constructor — `Collections.reverseOrder()`, or `comparingInt` plus `thenComparing` for a composite key. That comparator is fixed at creation; `compare == 0` is uniqueness, so a length-only order will merge unequal strings. Copying from a `SortedMap` keeps its comparator; copying from a plain `Map` does not.**
