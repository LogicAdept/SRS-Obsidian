<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/LinkedHashMap #SRS

# What is the difference between `HashMap` and `LinkedHashMap`?

> [!abstract] Short answer
> **Same hash table, different encounter order.** `HashMap` does not define iteration order. `LinkedHashMap` **extends** `HashMap` and adds a doubly-linked list of entries so iteration has a well-defined **encounter order** — insertion-order by default, or access-order (`accessOrder == true`) for LRU-style maps. Lookup is still hashing. It is not `Hashtable`, and insertion-order is not `TreeMap` sort order.

## Order is the difference that matters

`LinkedHashMap` javadoc (Java SE 21): hash table **and** linked list, with well-defined encounter order. The list runs through every entry. Eldest is first, youngest last. A key **re-inserted** with `put` does **not** move in insertion-order (`put` when `containsKey` is already true). `HashMap` makes no such promise: order is unspecified and may change over time. [[What are LinkedHashMap ordering guarantees]] [[Does LinkedHashMap extend HashMap]]

Both: `Map` (`get`/`put`), one `null` key and `null` values, expected constant-time hashing if hashes spread, unsynchronized, fail-fast iterators. `LinkedHashMap` is a `HashMap` subclass and, since 21, a `SequencedMap` (`putFirst` / `putLast` / `reversed`).

```text
                 HashMap                         LinkedHashMap
type             HashMap                         extends HashMap, SequencedMap (21)
order            unspecified                     encounter order (list)
default order    n/a                             insertion-order
access-order     n/a                             constructor flag accessOrder
re-put existing  may reshuffle iteration         insertion-order: stays put
iteration cost   capacity + size                 size only
basic ops        expected O(1)*                  expected O(1)*; slightly more work
nulls            one null key; null values       same
sync             no                              no
```

**Listing 1.** Java SE 21 class javadocs. `*` hashes disperse. Extra list work is why basic ops are *likely* a bit slower than `HashMap`; walking the map is often cheaper because it does not scan empty buckets.

```d2
direction: down
api: "Need defined iteration order?" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
hm: "HashMap\nhash → buckets" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
lhm: "LinkedHashMap\nbuckets + doubly-linked list" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}

api -> hm: no
api -> lhm: yes
```

**Fig. 1.** `LinkedHashMap` is not a second hash algorithm. It is `HashMap` plus a list that records encounter order.

## Insertion-order vs access-order

Default constructors and `LinkedHashMap(Map)` are **insertion-ordered**. Copying any map with `new LinkedHashMap<>(m)` keeps that copy’s encounter order as the source iterator presented it — the usual way to freeze a `HashMap`’s chaotic view into a stable sequence.

```java
LinkedHashMap<String, Integer> ins = new LinkedHashMap<>();
ins.put("b", 2);
ins.put("a", 1);
ins.put("b", 3); // still encounter order b, then a

LinkedHashMap<String, Integer> lru = new LinkedHashMap<>(16, 0.75f, true);
lru.put("b", 2);
lru.put("a", 1);
lru.get("b");    // access-order: a, then b (b moved last)
```

**Listing 2.** Third constructor argument `accessOrder`: `false` (default) insertion-order; `true` least-recently to most-recently accessed. In access-order, `put`, `putIfAbsent`, `get`, `getOrDefault`, `compute*`, and `merge` count as accesses (entry must still exist afterward). `replace` accesses only if it actually replaces. `putAll` accesses each copied mapping. View iteration does **not** count as access. [[Does putting an existing key change LinkedHashMap iteration order]]

Access-order plus `removeEldestEntry` is the documented LRU-cache hook: after `put`/`putAll`, return `true` to drop the eldest (first in encounter order). [[How do you build a cache with invalidation using LinkedHashMap]] [[Can LinkedHashMap fully implement an LRU cache]]

Java 21 `putFirst` / `putLast` relocate a key without treating that as an “access.” On the reversed view, an access moves the entry **first**, not last.

> [!warning] Hash table, not `Hashtable` — and not sorted
> Dumps say “Hashtable and linked list.” The implementation is a **hash table** plus a doubly-linked list. `java.util.Hashtable` is a different, synchronized map; the LinkedHashMap javadoc cites `HashMap` **and** `Hashtable` as the chaotic-order maps this class spares you from. Insertion-order is also **not** key sort order: `TreeMap` orders by `compareTo` / `Comparator`. Use `LinkedHashMap` when you care about encounter order, `TreeMap` when you care about sorted keys. [[What is the difference between HashMap, TreeMap, and LinkedHashMap]]
>
> In an **access-ordered** map, `get` is a structural modification. A fail-fast iterator can throw `ConcurrentModificationException` if another thread — or the same thread — `get`s during iteration. Insertion-ordered `get` is not structural.

> [!tip] Interview answer
> **`HashMap` hashes and does not define iteration order. `LinkedHashMap` extends it and threads a doubly-linked list through the entries so iteration is insertion-order by default, or access-order if you pass `true` as the third constructor argument. Re-putting an existing key does not reshuffle insertion-order. It is slightly more work per update than `HashMap`, but iteration is proportional to size, not capacity. It is not `Hashtable` and not a sorted map.**
