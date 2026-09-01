<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/LinkedHashMap #Java/Collections/Map/TreeMap #Java/HashCodeEquals #SRS

# What is the difference between `HashMap`, `TreeMap`, and `LinkedHashMap`?

> [!abstract] Short answer
> **Lookup machine and encounter order.** `HashMap` hashes into bins; iteration order is unspecified. `LinkedHashMap` is that hash table plus a doubly-linked list, so encounter order is insertion-order (default) or access-order. `TreeMap` is a red-black tree: keys sorted by `compareTo` / `Comparator`, guaranteed log(n), no hashing on the search path.

## Side by side (Java SE 21)

```text
                 HashMap              LinkedHashMap              TreeMap
extends          AbstractMap          HashMap                    AbstractMap
also             Map                  SequencedMap               NavigableMap, SortedMap, SequencedMap
structure        bin array            bins + before/after list   red-black tree
get / put        expected O(1)*       expected O(1)*, slightly   guaranteed log(n)
                                      slower than HashMap
iteration        capacity + size      size (walk the list)       n, in key order
order            unspecified          insertion or access        sorted by key
key test         equals + hashCode    same as HashMap            compare / compareTo
null key         yes                  yes                        NPE unless comparator allows
null values      yes                  yes                        yes
sync             no                   no                         no
```

**Listing 1.** Class javadocs. `*` constant-time only if hashes disperse among buckets. `LinkedHashMap` says it avoids `HashMap`’s chaotic order without `TreeMap`’s extra cost. Internals of the three machines: [[How do HashMap, TreeMap, and LinkedHashMap work at a high level]].

```d2
direction: down
need: "Need which order?" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
none: "HashMap\nnone promised" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
enc: "LinkedHashMap\ninsertion / access" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
sort: "TreeMap\ncompare keys" {
  width: 220
  height: 70
  style.fill: "#ffe0b2"
}

need -> none
need -> enc
need -> sort
```

**Fig. 1.** Three different “order” answers. Do not pick `TreeMap` to keep insertion order.

## What actually differs in use

`LinkedHashMap` **extends** `HashMap`: same capacity/load-factor knobs, same `null` key, same hash lookup ([[What is the internal structure of HashMap]]). The list is encounter order. Re-`put` of an existing key does **not** move it in insertion-order. Access-order is the three-arg constructor; then `get` is a structural modification ([[What are LinkedHashMap ordering guarantees]], [[How do you build a cache with invalidation using LinkedHashMap]]).

`TreeMap` does not hash. Keys must be mutually comparable. Ordering must be **consistent with `equals`** for a correct `Map`. `putFirst` / `putLast` throw `UnsupportedOperationException`: encounter order **is** sort order. Range views (`subMap`, `floorKey`, …) exist only here among the three. Pairwise speed vs sort: [[Compare HashMap and TreeMap tradeoffs]]. Backing tree: [[What data structure backs TreeMap in Java]].

All three are unsynchronized and fail-fast on their views. Wrap with `synchronizedMap` or, for `TreeMap`, `synchronizedSortedMap`.

> [!warning] “Ordered HashMap” is two types
> Encounter order → `LinkedHashMap`. Sorted keys → `TreeMap`. Copying `new TreeMap<>(hashMap)` sorts; it does not preserve hash iteration. Copying `new LinkedHashMap<>(m)` snapshots **that** map’s current iteration order, which for a `HashMap` is not insertion order.

> [!warning] Access-order `get` mutates the list
> On an access-order `LinkedHashMap`, `get` is a structural modification. Insertion-order `get` is not. Do not confuse that with `TreeMap`, where `get` never reorders.

> [!tip] Interview answer
> **`HashMap`: hash table, no order, expected O(1) if hashes spread. `LinkedHashMap`: same table plus a list — insertion-order by default, optional LRU access-order, iteration O(size). `TreeMap`: red-black `NavigableMap`, sorted keys, guaranteed log(n). Choose by unspecified vs encounter vs sorted.**
