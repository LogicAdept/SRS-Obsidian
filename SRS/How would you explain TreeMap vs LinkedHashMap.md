<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Map/LinkedHashMap #Java/Collections/Map/HashMap #SRS

# How would you explain `TreeMap` vs `LinkedHashMap`?

> [!abstract] Short answer
> **`TreeMap` sorts keys; `LinkedHashMap` remembers encounter order.** `TreeMap` is a red-black `NavigableMap`: `O(log n)` `get`/`put`/`remove`, `Comparable` or `Comparator`, `firstKey` / `floorKey`. `LinkedHashMap` is a `HashMap` plus a doubly-linked list: default **insertion-order**, `accessOrder=true` for LRU, `removeEldestEntry` to cap size, hash-table time. Sorted ≠ inserted.

## Sorted tree vs hashed list

`TreeMap`: red-black tree `NavigableMap`. Order is natural ordering of keys or a constructor `Comparator`. That order must be consistent with `equals` if the map is to obey the `Map` contract. Guaranteed `log(n)` for `containsKey`, `get`, `put`, `remove`. Navigable extras: `firstKey`, `lastKey`, `floorKey`, `ceilingKey`, … Null key throws `NullPointerException` under natural ordering (or if the comparator forbids nulls). `putFirst` / `putLast` throw `UnsupportedOperationException` — comparison, not positioning, sets encounter order. [[What data structure backs TreeMap in Java]] [[What is the time complexity of lookup by key in a TreeMap]] [[Why must TreeMap ordering be consistent with equals]] [[Can TreeMap have null keys or null values]]

`LinkedHashMap` extends `HashMap`. A doubly-linked list defines encounter order, normally **insertion-order** (eldest = least recently inserted). Re-`put` of a live key does **not** move the node. The `accessOrder` constructor orders by last access (LRU); `put`/`get`/… are accesses. `removeEldestEntry` after a **new** insert is the size-cap hook. Permits null elements. Constant-time basic ops like `HashMap`, plus list cost; iteration is `O(size)`, not capacity. Not synchronized; access-order `get` is a structural modification. [[What are LinkedHashMap ordering guarantees]] [[Can LinkedHashMap fully implement an LRU cache]] [[How do you build a cache with invalidation using LinkedHashMap]] [[Does putting an existing key change LinkedHashMap iteration order]]

```d2
direction: down
need: "need a Map with a defined order" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
tree: "TreeMap\nkey comparison\nlog n, NavigableMap" {
  width: 280
  height: 80
  style.fill: "#c8e6c9"
}
link: "LinkedHashMap\nput/get history\nhash + list" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}

need -> tree: sort by key
need -> link: insertion or LRU
```

**Fig. 1.** Same “ordered map” interview word. Sorted keys vs hashed encounter order.

```java
TreeMap<String, Integer> sorted = new TreeMap<>();
sorted.put("b", 1);
sorted.put("a", 1);
// iteration: a, b — key order, not put order
sorted.floorKey("m");

LinkedHashMap<String, Integer> inserted = new LinkedHashMap<>();
inserted.put("b", 1);
inserted.put("a", 1);
// iteration: b, a — insertion-order

LinkedHashMap<String, Integer> lru = new LinkedHashMap<>(16, 0.75f, true);
```

**Listing 1.** Conceptual: `put("b")` then `put("a")` is `a,b` in a tree and `b,a` in a linked hash map. [[What is the difference between HashMap, TreeMap, and LinkedHashMap]] [[Is LinkedHashMap synchronized]]

`HashMap` is the unordered hash table both are measured against: `LinkedHashMap` is slightly slower than `HashMap` because of the list; `TreeMap` is `log n` and not a hash table.

> [!warning] “Both are ordered HashMaps”
> `LinkedHashMap` *is* a `HashMap` plus a list. `TreeMap` is not: it compares keys, forbids a null key under natural order, and offers range queries `TreeMap`’s hash-based cousin cannot. Access-order is LRU, not sort. Default `LinkedHashMap` is insertion-order, not LRU, until `accessOrder=true` and `removeEldestEntry`.

> [!tip] Interview answer
> **`TreeMap` keeps keys sorted in a red-black tree (`O(log n)`, `NavigableMap`). `LinkedHashMap` is a `HashMap` with a linked list: insertion-order by default, or access-order LRU with `removeEldestEntry`.** Use the tree when you query by key order; use the linked hash map when you care about put/get history.
