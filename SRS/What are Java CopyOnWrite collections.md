<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency/CopyOnWrite #SRS

# What are Java CopyOnWrite collections?

> [!abstract] Short answer
> **`CopyOnWriteArrayList` and `CopyOnWriteArraySet`.** They are the `java.util.concurrent` types that implement mutation by replacing the underlying array with a fresh copy. Traversals need no client lock; iterators are snapshots and do not throw `ConcurrentModificationException`. There is no copy-on-write `Map` in the JDK.

## Two types, one array-copy idea

The concurrent package lists them as the alternatives to a synchronized `List` and a synchronized `Set`. Mutative operations (`add`, `set`, `remove`, …) copy the array. That is ordinarily too costly, and it pays off when traversals vastly outnumber mutations — listener lists, small mostly-read sets — and when you do not want to hold a lock for the whole iteration. [[What are CopyOnWriteArrayList thread safety tradeoffs]] [[Why use concurrent collections instead of Collections synchronized wrappers]]

`CopyOnWriteArrayList` is the list. Indexed `get` is cheap; each write copies every element. Iterators freeze the array as of construction: later writes are invisible to that iterator; `Iterator.remove` / `set` / `add` throw `UnsupportedOperationException`. `null` elements are allowed. [[What is the difference between CopyOnWriteArrayList and ArrayList]]

`CopyOnWriteArraySet` is a `Set` that uses an internal `CopyOnWriteArrayList` for every operation. It is thread-safe and snapshot-iterating for the same reason. Membership is an `equals` scan of the array, so it fits **small** sets, not a concurrent hash set. [[What is CopyOnWriteArraySet]] [[How do you get a concurrent Set in Java]]

A `Map` that needs concurrent readers uses `ConcurrentHashMap` or a skip list, not a copy-on-write array.

```java
List<Runnable> listeners = new CopyOnWriteArrayList<>();
Set<String> small = new CopyOnWriteArraySet<>();

listeners.add(task);                     // copies the list array
small.add("a");                          // scan, then copy if absent

for (Runnable task : listeners) {        // snapshot; no lock around the loop
    task.run();
}
```

**Listing 1.** The two copy-on-write collections. Both copy on write; only the list is indexed.

```java
Iterator<String> it = small.iterator();
small.add("b");                          // new array; `it` still sees the old snapshot
it.remove();                             // UnsupportedOperationException
```

**Listing 2.** Snapshot iterators on both types: no `ConcurrentModificationException`, no live view, no iterator `remove`.

```d2
direction: down
COW: java.util.concurrent {
  list: CopyOnWriteArrayList
  set: CopyOnWriteArraySet
}
set -> list: internal list
COW -> copy: mutation copies the array
COW -> snap: iterator snapshot
```

**Fig. 1.** JDK copy-on-write collections: a list, and a set implemented with that list. No copy-on-write map.

> [!warning] Not a concurrent hash structure, and not a `Map`
> `CopyOnWriteArraySet.add` is not `ConcurrentHashMap.newKeySet()`. Expect an O(n) `equals` scan and a full array copy on each successful add. Do not look for `CopyOnWriteHashMap` in the JDK. Frequent writes on a large list or set make copy-on-write the wrong family.

> [!tip] Interview answer
> **Java’s copy-on-write collections are `CopyOnWriteArrayList` and `CopyOnWriteArraySet`.** Each mutation copies the array so iteration needs no client lock and iterators are snapshots. Use them when reads vastly outnumber writes. There is no copy-on-write map in the JDK — for a concurrent map use `ConcurrentHashMap`.
