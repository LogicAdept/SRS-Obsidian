<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Set/TreeSet #SRS

# What internal structures back `HashSet` and `TreeSet`?

> [!abstract] Short answer
> **`HashSet` is a `HashMap`. `TreeSet` is a `TreeMap`.** Set elements are the map’s **keys**. `HashSet` values are one dummy object; `TreeSet` values are the same dummy idea on a red-black tree. There is no second table beside those maps.

## `HashSet` → hash table (`HashMap`)

The class is “backed by a hash table (actually a `HashMap` instance).” OpenJDK keeps `transient HashMap<E,Object> map` and `static final Object PRESENT`. `add` is `map.put(e, PRESENT)` ([[How is HashSet implemented in terms of HashMap]]).

That map is itself an array of bins (`Node<K,V>[] table` in OpenJDK). A bin is a list, or a tree of nodes once it is busy enough (`TREEIFY_THRESHOLD` is 8). Null element is the null **key** ([[Does HashSet allow a null element]]). Iteration walks keys; cost is set size **plus** table capacity ([[What is the internal structure of HashMap]]).

```java
transient HashMap<E, Object> map;
static final Object PRESENT = new Object();

public boolean add(E e) {
    return map.put(e, PRESENT) == null;
}
```

**Listing 1.** OpenJDK 21 `HashSet`. The set *is* the key set of that map.

## `TreeSet` → red-black tree (`TreeMap`)

`TreeSet` is “a `NavigableSet` implementation based on a `TreeMap`.” `TreeMap` is “a Red-Black tree based `NavigableMap`,” sorted by natural order or a constructor `Comparator`, with guaranteed `log(n)` for `containsKey` / `get` / `put` / `remove` — which become `contains` / `add` / `remove` on the set ([[Is TreeSet implemented using TreeMap]], [[Which tree data structure backs Java TreeSet]]).

```d2
direction: down
hs: "HashSet" {
  width: 160
  height: 50
  style.fill: "#fff3e0"
}
hm: "HashMap\narray of bins\n(+ tree bins)" {
  width: 220
  height: 80
  style.fill: "#ffe0b2"
}
ts: "TreeSet" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}
tm: "TreeMap\nred-black tree" {
  width: 220
  height: 80
  style.fill: "#c8e6c9"
}

hs -> hm
ts -> tm
```

**Fig. 1.** Two `Set` types, two maps. Uniqueness follows the map: hash/`equals` vs `compare` ([[How do HashSet and TreeSet decide whether two elements are duplicates]]).

`LinkedHashSet` is a `HashSet` whose map is a `LinkedHashMap` (list through entries). That is not `TreeSet`. `TreeSet` does not hash.

Neither set is synchronized. Fail-fast iterators come from the backing map’s `modCount`. `TreeSet` range views (`headSet`, `subSet`, …) are views on the same tree, not copies ([[What NavigableSet operations does TreeSet provide]]).

> [!warning] “TreeSet is a HashSet plus sort” is the wrong picture
> Sorting does not sit on top of buckets. You pay a red-black tree and a comparison order. A `HashSet` never becomes a `TreeSet` by iterating it in order.

> [!warning] You never get the map back
> There is no `HashSet.asMap()`. Values are not user data. Do not design as if you could `get` a payload from the dummy.

> [!tip] Interview answer
> **`HashSet` wraps a `HashMap` (hash table, dummy values). `TreeSet` wraps a `TreeMap` (red-black tree).** Elements are keys in both. That is why null, uniqueness, and big-O follow the map, not a separate set engine.
