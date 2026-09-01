<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #Java/Collections/Sorting #SRS

# What does sorted mean for a `SortedMap` besides iteration order?

> [!abstract] Short answer
> **A total order on keys that the map uses for every key comparison, not only for walking views.** `get` / `put` / `containsKey` treat `compareTo` / `compare == 0` as the same key. You also get **range views** (`subMap`, `headMap`, `tailMap`), **endpoints** (`firstKey`, `lastKey`), and `comparator()`. Encounter order **is** that order: `putFirst` / `putLast` throw. Iteration is a consequence, not the definition.

## Order is the lookup, not a paint job

`SortedMap` (Java 1.2) is a `Map` with a total ordering: natural order of the keys, or a `Comparator` given at creation. All inserted keys must be mutually comparable (`ClassCastException` otherwise). The analogue of `SortedSet`. [[What is the Map interface in Java]]

The javadoc’s reason this is more than iterator order: **`Map` is specified with `equals`, but a sorted map performs all key comparisons with `compareTo` / `compare`.** Two keys that compare equal are one mapping. For a correct `Map`, that ordering must be **consistent with `equals`**. If it is not, the tree is still well-defined; it just fails the `Map` contract. [[Can keys be duplicated in a Java Map]]

```d2
direction: down
ord: "Total order on keys\nComparable or Comparator" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
loc: "Locate\ncompare == 0 is the key" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
rng: "Range views\nsubMap / headMap / tailMap" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
ends: "firstKey / lastKey\ncomparator()" {
  width: 260
  height: 70
  style.fill: "#ffe0b2"
}
iter: "Views iterate in that order" {
  width: 280
  height: 60
  style.fill: "#f3e5f5"
}

ord -> loc
ord -> rng
ord -> ends
ord -> iter
```

**Fig. 1.** Iteration is one use of the same relation. `LinkedHashMap` encounter order is not this.

```java
sorted.subMap(from, to);   // [from, to)  live view
sorted.headMap(to);        // keys < to
sorted.tailMap(from);      // keys >= from
sorted.firstKey();         // lowest; NoSuchElementException if empty
sorted.lastKey();
sorted.comparator();       // null ⇒ natural order
```

**Listing 1.** Extra operations (Java SE 21). Ranges are **half-open** where both ends apply: low inclusive, high exclusive. `from.equals(to)` yields an empty `subMap`. The view is backed by the map; inserting a key outside the range throws `IllegalArgumentException`.

`values()` is **not** sorted by value: it follows **ascending keys**. `reversed()` (Java 21) is a reverse-ordered `SortedMap` view. `putFirst` / `putLast` always throw: position is induced by comparison, so you cannot pin a mapping at an end. [[What is the difference between HashMap, TreeMap, and LinkedHashMap]]

`NavigableMap` (1.6) is the usual subtype (`TreeMap`, `ConcurrentSkipListMap`): inclusive/exclusive `subMap` overloads plus `floorKey` / `ceilingKey` / `lowerKey` / `higherKey` and snapshot `firstEntry` / `pollFirstEntry`. Those still rest on the same total order. Structure: [[What data structure backs TreeMap in Java]]. Why pick it: [[Compare HashMap and TreeMap tradeoffs]].

> [!warning] Sorted ≠ insertion order
> Copying `new TreeMap<>(hashMap)` **re-sorts** by key. It does not keep `HashMap` iteration. A `subMap` is not a copy: `clear()` on the view clears that range in the original. Do not use `TreeMap` when you wanted `LinkedHashMap`.

> [!tip] Interview answer
> **Sorted means a total order on keys used for lookup (`compare == 0`), range views, and first/last — not merely that `keySet()` comes out sorted. That order must be consistent with `equals` for a correct `Map`. `subMap` is a live half-open window. `NavigableMap` adds floor/ceiling. `TreeMap` is the usual implementation.**
