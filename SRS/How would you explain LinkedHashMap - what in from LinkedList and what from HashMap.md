<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Java/Collections/Map/HashMap #Java/Collections/List/LinkedList #SRS

# What does `LinkedHashMap` take from `HashMap`, and what from a linked list?

> [!abstract] Short answer
> **The hash table is `HashMap`; the encounter order is a doubly-linked list of entries.** `LinkedHashMap` **extends** `HashMap`, so `get`/`put`, buckets, nulls, load factor, and fail-fast iterators are the hash map. It is **not** a `java.util.LinkedList` and does not store entries in one. The extra list is the same *kind* of structure as `LinkedList` (doubly-linked nodes) and is what makes iteration well-defined.

## From `HashMap`

Class signature (Java SE 21): `LinkedHashMap<K,V> extends HashMap<K,V> implements SequencedMap<K,V>`. Same optional `Map` operations, null key and values, expected constant-time `get`/`put` if hashes spread, unsynchronized, fail-fast views. Capacity and load factor are defined as for `HashMap`. [[Does LinkedHashMap extend HashMap]] [[What is the difference between HashMap and LinkedHashMap]]

`HashMap` itself does **not** define iteration order. That is the gap the list fills. [[What is a HashMap]]

## From a linked list — not from `LinkedList`

`LinkedHashMap` javadoc: it differs from `HashMap` by a **doubly-linked list running through all of its entries**. That list is encounter order: eldest first, youngest last. `LinkedList` javadoc: a doubly-linked list implementation of `List`/`Deque`. Same node shape (prev/next), different type: map entries vs list elements. There is no `LinkedList` field inside the map. [[What are LinkedHashMap ordering guarantees]]

```d2
direction: down
lhm: "LinkedHashMap" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}
hm: "extends HashMap\nbuckets, hash, equals" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
list: "doubly-linked entries\nencounter order\n(not java.util.LinkedList)" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}

lhm -> hm
lhm -> list
```

**Fig. 1.** Two structures, one class. Lookup hashes. Iteration walks the list.

Default constructors are **insertion-order**. `put` of a key that is **already** present does **not** move it in that mode. `new LinkedHashMap<>(int, float, true)` is **access-order** (least- to most-recently accessed). Then `put`, `get`, `getOrDefault`, `compute*`, `merge` (and `putIfAbsent`) count as accesses and move the entry **last** on this map (`replace` only if it actually replaces). View iteration is not an access. [[Does putting an existing key change LinkedHashMap iteration order]]

```java
LinkedHashMap<String, Integer> ins = new LinkedHashMap<>();
ins.put("a", 1);
ins.put("b", 2);
ins.put("a", 9); // still encounter order a, b — HashMap replace, list unmoved

LinkedHashMap<String, Integer> lru = new LinkedHashMap<>(16, 0.75f, true);
lru.put("a", 1);
lru.put("b", 2);
lru.get("a");    // list: b, then a
```

**Listing 1.** HashMap part: same-key `put` replaces the value. List part: insertion-order keeps position; access-order moves on `get`/`put`.

Iteration over `LinkedHashMap` views is **O(size)** (walk the list). `HashMap` iteration is capacity + size (empty buckets). That is the list’s payoff, plus LRU via `removeEldestEntry`. Java 21 `putFirst`/`putLast`/`reversed` are sequenced-map operations on that same list. [[How do you build a cache with invalidation using LinkedHashMap]]

> [!warning] It does not contain a `LinkedList`, and re-`put` is not always order-stable
> Dumps say “from LinkedList.” The JDK never wraps `java.util.LinkedList`; it threads its own links through `HashMap` nodes. Dumps also say re-inserting an existing key never changes order. That is **insertion-order `put` only**. In access-order, that `put` is an access and the entry goes last. `get` in access-order is a structural modification (fail-fast).

> [!tip] Interview answer
> **`LinkedHashMap` is a `HashMap` plus a doubly-linked list of entries. Hashing, buckets, and `equals` come from `HashMap`. Predictable iteration — insertion-order by default, access-order if you pass `true` — comes from the list, the same idea as `LinkedList` but not that class. Re-putting an existing key keeps position only in insertion-order.**
