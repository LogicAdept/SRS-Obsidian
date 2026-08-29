<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Collections/Map/HashMap #Java/Collections/Map/ConcurrentHashMap #Java/Collections/Concurrency #SRS

# How would you explain drawbacks of the legacy `Hashtable` class?

> [!abstract] Short answer
> **It is a 1.0 hash table that the JDK itself tells you not to pick for new code.** Every public lookup and update locks the whole table. Null keys and values throw. It still extends obsolete `Dictionary`. `keys()` / `elements()` enumerations are not fail-fast. Crowded buckets stay linked lists. Use `HashMap` if you do not need a monitor; use `ConcurrentHashMap` if you do.

## The class page already names the replacements

As of Java 2, `Hashtable` was retrofitted as a `Map`. Unlike the new collections, it stays synchronized. The same javadoc: if you do not need thread safety, use `HashMap`; if you want a highly concurrent map, use `ConcurrentHashMap`. [[What need did HashMap address compared to older maps]] is why `HashMap` exists. Pairwise contract: [[What is the difference between HashMap and Hashtable]].

```text
Hashtable
  since 1.0, Map since 1.2
  extends Dictionary (obsolete parent)
  synchronized on this
  no null key, no null value  → NPE
  default capacity 11
  keys()/elements() Enumeration: not fail-fast
  view iterators: fail-fast
```

**Listing 1.** Drawbacks that are in the Java SE 21 class contract, not folklore.

```d2
direction: down
ht: "Hashtable" {
  width: 200
  height: 55
  style.fill: "#ffe0b2"
}
lock: "one monitor\non every get/put" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
nulls: "null → NPE" {
  width: 180
  height: 55
  style.fill: "#ffebee"
}
enum: "Enumeration not fail-fast" {
  width: 260
  height: 60
  style.fill: "#ffebee"
}
list: "collision bin stays a list" {
  width: 260
  height: 60
  style.fill: "#ffebee"
}

ht -> lock
ht -> nulls
ht -> enum
ht -> list
```

**Fig. 1.** Four reasons it is “legacy” even though it implements `Map`.

## Why “synchronized” is still a drawback

`get`, `put`, `remove`, `size`, and the other table methods are `synchronized`. That is **one lock for the whole map**, including reads. Two threads cannot `get` different keys at once. `ConcurrentHashMap` obeys the same functional spec as `Hashtable` (and also forbids nulls) but retrievals generally do not lock, and you cannot lock the entire table to freeze all access. [[How does Hashtable differ from ConcurrentHashMap]]

A monitor per method does **not** make a check-then-act sequence atomic. `containsKey` then `put` is two lock acquisitions; another thread can run in between. That is why “thread-safe `Hashtable`” is the wrong story for compound updates.

`contains(Object)` is the pre-`Map` value search (same as `containsValue`). It is not `Collection.contains` on keys. Null argument → `NPE`.

## Iteration and collisions

View iterators (`entrySet` and friends) are fail-fast. `keys()` and `elements()` return `Enumeration`s that are **not**: if the table is structurally modified during enumeration, the result is **undefined**. Mixing those two APIs is a footgun.

Java 8 balanced trees went into `HashMap`, `LinkedHashMap`, and `ConcurrentHashMap`. They were **not** applied to `Hashtable`, so a high-collision bucket stays a sequential chain. Default capacity **11** is not a power of two; OpenJDK indexes with remainder, not `(n - 1) & hash`.

`Properties` still extends `Hashtable`. That keeps the class in the JDK. It is not a reason to declare `Hashtable` in new application maps.

> [!warning] “I’ll use Hashtable so the map is thread-safe”
> Coarse `synchronized` is not `ConcurrentHashMap`. It still forbids nulls, still serializes all access, and still does not compose two calls into one atomic action. `Collections.synchronizedMap(new HashMap<>(…))` is the wrapper `HashMap` documents when you only wanted a lock around a modern map.

> [!tip] Interview answer
> **`Hashtable` is legacy: whole-table lock on every call, no nulls, obsolete `Dictionary` parent, non-fail-fast `Enumeration`s, list-only collision bins. The javadoc replacement is `HashMap` without a monitor, or `ConcurrentHashMap` for concurrent writers. Do not sell it as the thread-safe `HashMap`.**
