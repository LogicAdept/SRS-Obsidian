<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Set #SRS

# How do you get a concurrent Set in Java?

> [!abstract] Short answer
> **There is no `ConcurrentHashSet` type. For a concurrent hash set, call `ConcurrentHashMap.newKeySet()` (Java 8+).** Use `CopyOnWriteArraySet` only when the set stays small and reads dwarf writes. Use `ConcurrentSkipListSet` when you need a concurrent *sorted* `NavigableSet`. `Collections.synchronizedSet` is a single mutex around another set, not a concurrent collection.

## The usual answer: a `ConcurrentHashMap` key set

`ConcurrentHashMap.newKeySet()` (and `newKeySet(int initialCapacity)`) creates a new `Set` backed by a `ConcurrentHashMap` that maps each element to `Boolean.TRUE`. The runtime type is `ConcurrentHashMap.KeySetView`; you cannot `new` that class yourself. `add` puts the key with that mapped value; `add` returns `false` when the key was already present. `null` is forbidden (`NullPointerException`), like the map.

The map is a hash table with **full concurrency of retrievals** and high expected concurrency for updates. Retrievals **do not entail locking** and generally do not block; they may overlap with puts and removes. Iterators are weakly consistent: they do not throw `ConcurrentModificationException`, and they are meant for one thread at a time. That is the default concurrent set for uniqueness checks, “seen” sets, and similar write-friendly membership ([[Is HashSet synchronized]]).

```java
Set<String> seen = ConcurrentHashMap.newKeySet();
seen.add("a");
boolean added = seen.add("b"); // true the first time; false if already present
```

**Listing 1.** Java 8+ factory. Size with `newKeySet(expectedCount)` when you know the scale. Do not confuse this with `someMap.keySet()`: that view **rejects** `add` / `addAll` unless you used `keySet(mappedValue)`.

```d2
direction: down
need: "Need a thread-safe Set?" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
hash: "ConcurrentHashMap.newKeySet()\nhash membership, Java 8+" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
cow: "CopyOnWriteArraySet\nsmall, read-mostly, snapshot walks" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
sorted: "ConcurrentSkipListSet\nNavigableSet, expected log(n)" {
  width: 320
  height: 80
  style.fill: "#fce4ec"
}
wrap: "Collections.synchronizedSet\none lock; sync on iteration" {
  width: 320
  height: 80
  style.fill: "#eceff1"
}

need -> hash
need -> cow
need -> sorted
need -> wrap
```

**Fig. 1.** Pick the implementation by membership cost, size, ordering, and whether you can live with one lock.

## The other concurrent `Set` types

`CopyOnWriteArraySet` (1.5) wraps a `CopyOnWriteArrayList`. It is thread-safe. Official fit: sizes **generally stay small**, **read-only operations vastly outnumber** mutative ones, and you need interference-free traversal. Every `add` / `remove` usually **copies the whole array**. Iterators are snapshots: fast, no extra locking, and they do **not** support `remove` ([[What is CopyOnWriteArraySet]]).

`ConcurrentSkipListSet` (1.6) is a scalable concurrent `NavigableSet` on a `ConcurrentSkipListMap`. Elements are ordered by natural order or a constructor `Comparator`. `contains` / `add` / `remove` are expected **log(n)**. `null` is forbidden. Iterators are weakly consistent. `size()` is **not** constant time (it walks). Bulk ops (`addAll`, `removeIf`, `forEach`, …) are **not** atomic as a whole ([[What is ConcurrentSkipListSet]]).

## The wrapper that is not this API

`Collections.synchronizedSet(new HashSet<>())` returns a synchronized **view**. All access must go through that view. You must still `synchronized (s)` around `Iterator` / `Spliterator` / `Stream` walks. That is one lock on a `HashSet`, not `ConcurrentHashMap` concurrency ([[Why use concurrent collections instead of Collections synchronized wrappers]]).

> [!warning] `map.keySet()` is not `newKeySet()`
> `ConcurrentHashMap.keySet()` with no mapped value is a key view that **does not support** `add` / `addAll`. `newKeySet()` (or `keySet(mappedValue)`) is the addable set. Adding `null` throws `NullPointerException` even though `HashSet` allows one `null`.

> [!warning] `CopyOnWriteArraySet` is not “the concurrent HashSet”
> A large or write-heavy set will copy the array on every mutation. Use `newKeySet()` for that load. Use `ConcurrentSkipListSet` when you need ordered views, not because it is “more concurrent.”

> [!tip] Interview answer
> **There is no `ConcurrentHashSet`; call `ConcurrentHashMap.newKeySet()` for a concurrent hash set (`Boolean.TRUE` values, no `null`, Java 8).** `CopyOnWriteArraySet` is for small read-mostly snapshots; `ConcurrentSkipListSet` is the concurrent sorted `NavigableSet`. `Collections.synchronizedSet` is a mutex wrapper — you still lock around iteration.
