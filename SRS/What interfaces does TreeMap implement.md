<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Map/HashMap #SRS

# What interfaces does `TreeMap` implement?

> [!abstract] Short answer
> Directly: **`NavigableMap`**, **`Cloneable`**, **`Serializable`**. That pulls in **`SortedMap`**, **`SequencedMap`** (Java 21), and **`Map`**. It **extends `AbstractMap`**. It does **not** implement `Collection` or `Iterable`. `HashMap` is `Map` + `Cloneable` + `Serializable` only — no sorted/navigable types.

## The `implements` line vs the full type

```text
public class TreeMap<K,V> extends AbstractMap<K,V>
    implements NavigableMap<K,V>, Cloneable, Serializable
```

`NavigableMap` extends `SortedMap`, which since 21 extends `SequencedMap`, which extends `Map`. The “All Implemented Interfaces” list is therefore `NavigableMap`, `SortedMap`, `SequencedMap`, `Map`, plus the two markers. `Cloneable` / `Serializable` are extra; `AbstractMap` is a **class**.

| Type | Role on `TreeMap` |
| --- | --- |
| `Map` | `get` / `put` / views; identity of keys is still **compare**, not `equals` ([[How does TreeMap decide whether two keys are the same]]) |
| `SortedMap` (1.2) | Total key order, `subMap`/`headMap`/`tailMap`, `firstKey`/`lastKey` |
| `NavigableMap` (1.6) | Closest-match keys/entries, `poll*`, inclusive ranges, `descendingMap` ([[When was NavigableMap introduced for TreeMap]], [[How do you get a range or neighbor key from a TreeMap]]) |
| `SequencedMap` (21) | Encounter order; `TreeMap.putFirst` / `putLast` throw — position is the comparator, not insert-at-end |
| `Cloneable`, `Serializable` | `clone()`; the map (and a serializable comparator) can be serialized |

`HashMap` implements `Map`, `Cloneable`, `Serializable` and is a hash table, not a `NavigableMap` ([[Compare HashMap and TreeMap tradeoffs]]). `TreeMap` was 1.2 with the Collections Framework ([[In which Java version was TreeMap introduced]]).

```d2
direction: down
map: "Map" {
  width: 140
  height: 40
  style.fill: "#e3f2fd"
}
seq: "SequencedMap\n(21)" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
sorted: "SortedMap\n(1.2)" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}
nav: "NavigableMap\n(1.6)" {
  width: 180
  height: 50
  style.fill: "#f3e5f5"
}
tm: "TreeMap\n+ Cloneable + Serializable" {
  width: 260
  height: 60
  style.fill: "#ffe0b2"
}
map -> seq -> sorted -> nav -> tm
```

**Fig. 1.** Interface chain. `Collection` / `Iterable` are not on this path. Iterate `entrySet()` / `keySet()` / `values()`.

```java
import java.util.Map;
import java.util.NavigableMap;
import java.util.SequencedMap;
import java.util.SortedMap;
import java.util.TreeMap;

class Demo {
    static void assignments() {
        var t = new TreeMap<Integer, String>();
        NavigableMap<Integer, String> n = t;
        SortedMap<Integer, String> s = n;
        SequencedMap<Integer, String> q = s;
        Map<Integer, String> m = q;
        t.putFirst(1, "a"); // UnsupportedOperationException
    }
}
```

**Listing 1.** Widening works down the chain. `putFirst` is on `SequencedMap` / `SortedMap` and is specified to throw on a sorted map.

> [!warning] `Map` is not a `Collection`
> Interview lists that say `TreeMap` “indirectly implements `Collection` and `Iterable`” are wrong. `Map` is a separate root (`Dictionary`’s successor). The **views** are collections: `keySet()` is a `Set`, `values()` is a `Collection`. The map itself is not for-each-able.

> [!warning] Not hashing plus a sort
> `TreeMap` is a red-black `NavigableMap`. Lookup is `compare`/`compareTo`, log(n), no `hashCode` in the search. Do not describe it as `HashMap` with extra sorting.

> [!tip] Interview answer
> **`TreeMap` implements `NavigableMap` (hence `SortedMap`, `SequencedMap` since 21, and `Map`), plus `Cloneable` and `Serializable`. It is not a `Collection`. `HashMap` stops at `Map`. NavigableMap is the floor/ceiling/poll/range API; `putFirst`/`putLast` throw because order is the comparator.**
