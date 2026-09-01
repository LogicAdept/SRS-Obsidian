<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Map/EnumMap #Java/Collections/Map/HashMap #Java/Collections/Map/Hashtable #Java/Collections/Map/IdentityHashMap #Java/Collections/Map/LinkedHashMap #Java/Collections/Map/TreeMap #Java/Collections/Map/WeakHashMap #SRS

# What are the main Java `Map` implementations?

> [!abstract] Short answer
> **Three general-purpose maps: `HashMap` (speed, unspecified order), `LinkedHashMap` (near-`HashMap` speed, encounter order), `TreeMap` (`SortedMap` / key order, guaranteed log(n)).** Special-purpose: `EnumMap`, `WeakHashMap`, `IdentityHashMap`. Concurrent: `ConcurrentHashMap` (and `ConcurrentSkipListMap` when you need a concurrent sorted map). `Hashtable` is the legacy synchronized table, not the default. [[What is the difference between HashMap, TreeMap, and LinkedHashMap]]

## General-purpose (the usual choice)

Oracle’s implementations lesson names exactly three. They support the optional `Map` operations and are **unsynchronized**. The Collections Framework overview: tune by switching implementations of the same interface.

```text
need sorted keys / ranges     → TreeMap
need insertion or access order → LinkedHashMap
need a hash table, no order    → HashMap   (default)
```

**Listing 1.** Decision from the Map implementations tutorial. `LinkedHashMap` also documents access-order and `removeEldestEntry` for a bounded cache. [[What is a HashMap]]

```d2
direction: down
q: "Which Map?" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
gp: "general-purpose\nHashMap / LinkedHashMap / TreeMap" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
sp: "special\nEnumMap WeakHashMap IdentityHashMap" {
  width: 340
  height: 70
  style.fill: "#fff3e0"
}
cc: "concurrent\nConcurrentHashMap\nConcurrentSkipListMap" {
  width: 280
  height: 80
  style.fill: "#ffe0b2"
}
q -> gp
q -> sp
q -> cc
```

**Fig. 1.** “Main” is the general-purpose trio. The others are named jobs, not faster `HashMap`s.

## Special-purpose

`EnumMap`: all keys from one enum type; internally an array; natural enum-declaration order; no null keys, null values allowed. Prefer it over `HashMap` when the key is an enum.

`WeakHashMap`: **weak keys**; the mapping does not keep the key alive. Registry-style tables, not an LRU cache. [[What is WeakHashMap used for]]

`IdentityHashMap`: keys (and values) compared with `==`. Not a general-purpose `Map`; it intentionally violates the `equals` contract. Node tables, proxies. [[What is IdentityHashMap for]]

## Concurrent and legacy

`ConcurrentHashMap`: full concurrency of retrievals, high expected concurrency for updates; retrievals generally do not lock. Drop-in for `Hashtable` **thread safety**, not for its locking details. Like `Hashtable` and unlike `HashMap`, **no null key or value**. Iterators do not throw `ConcurrentModificationException`. [[Is java.util.HashMap thread safe]]

`ConcurrentSkipListMap`: concurrent `ConcurrentNavigableMap`, sorted, expected average log(n).

`Hashtable`: legacy (overview: retrofitted `Map`). Synchronized, no nulls. Prefer `ConcurrentHashMap` or a `HashMap` plus an external lock. [[What is the difference between HashMap and Hashtable]]

`Map.of` / `copyOf` are unmodifiable factories, not a fourth general-purpose class. `Collections.synchronizedMap` is a wrapper, not a table type.

> [!warning] “Hashtable because I have threads”
> A lock around the whole table is not the concurrent map. `ConcurrentHashMap` is the usual replacement. Do not pick `IdentityHashMap` for speed.

> [!tip] Interview answer
> **Name the three general-purpose maps: `HashMap`, `LinkedHashMap`, `TreeMap`. Then `ConcurrentHashMap` for shared updates, `EnumMap` for enum keys, `WeakHashMap` / `IdentityHashMap` for their documented jobs. `Hashtable` is legacy.**
