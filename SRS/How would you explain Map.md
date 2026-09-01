<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #SRS

# How would you explain `Map`?

> [!abstract] Short answer
> **A `Map` associates keys to values; each key maps to at most one value.** It replaced the obsolete `Dictionary` class. You look at it as three views — `keySet`, `values`, `entrySet` — plus `get`/`put`. Default choice is `HashMap`. Need encounter order or LRU → `LinkedHashMap`. Need sorted keys → `TreeMap`. Need concurrency → `ConcurrentHashMap`. Do not start with `Hashtable`.

## Interface first, then which class

`Map`: no duplicate keys. The Collections Framework’s hash/list/tree maps implement this interface. `Dictionary` was a 1.0 abstract class; `Map` takes its place. Mutable keys that change `equals` while in the map are unspecified. Some implementations ban nulls. Optional mutators may throw `UnsupportedOperationException`. [[What is the Map interface in Java]] [[What is the main purpose of the Map interface]] [[What is java.util.Dictionary and how does Hashtable relate to it]]

General-purpose (tutorial): `HashMap` if you want speed and do not care about order; `TreeMap` if you need `SortedMap`/`NavigableMap`; `LinkedHashMap` if you want near-HashMap speed plus insertion-order (or access-order). Special-purpose: `EnumMap`, `WeakHashMap`, `IdentityHashMap`. Concurrent: `ConcurrentHashMap`. [[What are the main Java Map implementations]]

```d2
direction: down
iface: "Map\nkey → at most one value" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
hm: "HashMap\nunsync, no order, nulls" {
  width: 280
  height: 70
  style.fill: "#c8e6c9"
}
lhm: "LinkedHashMap\ninsert or access-order" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
tm: "TreeMap\nNavigableMap, sorted keys" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
chm: "ConcurrentHashMap\nno whole-table lock" {
  width: 280
  height: 70
  style.fill: "#bbdefb"
}

iface -> hm
iface -> lhm
iface -> tm
iface -> chm
```

**Fig. 1.** Interview four plus the concurrent replacement. `Hashtable` is a synchronized 1.0 `Map`; skip it for new code.

`HashMap`: hash table, unsynchronized, no encounter-order guarantee, permits the null key and null values. Default capacity 16, load factor 0.75. Since 1.2. [[Is java.util.HashMap thread safe]] [[Does LinkedHashMap allow null keys or values]]

`LinkedHashMap` extends `HashMap` and adds a doubly-linked list. Default is insertion-order (re-`put` does not move). `accessOrder=true` is documented for LRU caches with `removeEldestEntry`. Access-order `get` is a structural modification. [[Can LinkedHashMap fully implement an LRU cache]] [[What are LinkedHashMap ordering guarantees]]

`TreeMap`: red-black `NavigableMap`, sorted by natural order or a `Comparator`. `firstKey` / `lastKey` / `floorKey` (and the rest of the navigable API) live here. Null key NPEs under natural ordering. `putFirst`/`putLast` throw `UnsupportedOperationException`. [[Can TreeMap have null keys or null values]]

`Hashtable`: synchronized, no null keys or values, `Since: 1.0`, became a `Map` in 1.2. Not `@Deprecated`; javadoc says use `HashMap` or `ConcurrentHashMap`. [[Is Hashtable deprecated]] [[Can you unsynchronize a Hashtable]] [[Why is ConcurrentHashMap faster than Hashtable]]

Specials in one line: `IdentityHashMap` is `==` keys and pins; `WeakHashMap` is weak keys; `EnumMap` is an array of one enum type in declaration order.

```java
Map<String, Integer> counts = new HashMap<>();
counts.put("a", 1);
counts.get("a");           // 1
counts.keySet();           // set view of keys

Map<String, Integer> lru = new LinkedHashMap<>(16, 0.75f, true);
NavigableMap<String, Integer> sorted = new TreeMap<>();
sorted.floorKey("m");
```

**Listing 1.** Conceptual: program to `Map` (or `NavigableMap` when you need it). Pick the class for order, nulls, and threads.

> [!warning] “Hashtable is the thread-safe HashMap, so use it”
> It is a whole-table lock and a 1.0 leftover. Concurrent maps do not lock the entire table on `get`. `TreeMap` is not “HashMap with sort” for null keys. `LinkedHashMap` default is **not** LRU until `accessOrder` is true.

> [!tip] Interview answer
> **A `Map` is a key-to-value table with unique keys, replacing `Dictionary`.** I default to `HashMap`. I use `LinkedHashMap` for insertion or LRU order, `TreeMap` when I need sorted/navigable keys, and `ConcurrentHashMap` when the map is shared. `Hashtable` is legacy synchronized — I do not pick it for new code.
