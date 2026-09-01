<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/TreeMap #Java/HashCodeEquals #SRS

# Compare `HashMap` and `TreeMap` tradeoffs

> [!abstract] Short answer
> **`HashMap` is the default: expected constant-time `get`/`put` if hashes spread, no iteration order, keys by `equals`/`hashCode`.** **`TreeMap` is the ordered map: guaranteed log(n) for those operations, keys sorted by `compareTo` or a `Comparator`, no hashing in the lookup path.** Pick `HashMap` for speed and a plain `Map`. Pick `TreeMap` when you need sorted keys or range views. Neither is synchronized.

## What you pay for

```text
                 HashMap                         TreeMap
structure        array of bins                   red-black tree
get / put        expected O(1) if hashes spread  guaranteed log(n)
order            unspecified, may change         sorted by key
key identity     equals + hashCode               compare / compareTo
null key         yes                             NPE unless comparator allows
null values      yes                             yes
iteration        capacity + size, any order      n mappings, key order
```

**Listing 1.** Class javadocs (Java SE 21) plus the two backing structures. “Expected O(1)” is not a worst-case guarantee. [[Does HashMap guarantee its documented lookup time complexity]] and [[What is the time complexity of lookup by key in a TreeMap]] are those sentences.

```d2
direction: down
need: "Need a Map?" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
ord: "Sorted keys or\nrange queries?" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
hm: "HashMap" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
tm: "TreeMap" {
  width: 180
  height: 60
  style.fill: "#ffe0b2"
}

need -> ord
ord -> tm: yes
ord -> hm: no
```

**Fig. 1.** Order is the usual reason to accept log(n). Insertion-order or access-order is `LinkedHashMap`, not `TreeMap`. [[What is the difference between HashMap, TreeMap, and LinkedHashMap]] is the three-way split.

## Keys and extra API

`HashMap` keys must obey the `equals`/`hashCode` contract. A bad or mutating hash turns one bin into a list (or a conditional Java 8+ tree). [[What requirements apply to keys used in a HashMap]] and [[What is the internal structure of HashMap]] are that side.

`TreeMap` keys must be mutually comparable. The ordering must be **consistent with `equals`** for the map to implement `Map` correctly: the tree treats `compare == 0` as the same key. [[What data structure backs TreeMap in Java]] is the red-black `Entry`. You also get `NavigableMap` operations (`floorKey`, `ceilingKey`, `subMap`, …) that `HashMap` does not offer.

Both are unsynchronized. The documented wrappers differ: `Collections.synchronizedMap` versus `synchronizedSortedMap`.

> [!warning] Do not “sort a HashMap” by switching types blindly
> `TreeMap` will not preserve `HashMap` iteration order. It will also reject a `null` key under natural ordering, and it will merge keys that `compare` equal even if `equals` does not. Copying into a `TreeMap` is n log(n), not a free view.

> [!tip] Interview answer
> **Use `HashMap` unless you need keys in sorted order or range queries: expected constant-time lookup if `hashCode` spreads, unspecified iteration order. Use `TreeMap` for a red-black `NavigableMap`: guaranteed log(n) `get`/`put`/`remove`, ordered by `Comparable`/`Comparator`, no hash table. Speed versus order is the tradeoff; `LinkedHashMap` is the third option if the order you want is insertion or access.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Почему B-tree, а не Hash?**

Hash: O(1) только =. B-tree: O(log n) но поддерживает <, >, BETWEEN, ORDER BY, LIKE 'abc%'. Поэтому B-tree — default.
