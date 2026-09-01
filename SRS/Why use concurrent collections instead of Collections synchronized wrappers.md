<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #SRS

# Why use concurrent collections instead of `Collections` synchronized wrappers?

> [!abstract] Short answer
> **When many threads share a collection, a concurrent type lets them proceed together; a synchronized wrapper holds one lock for every call.** `Collections.synchronizedMap` / `synchronizedList` / `synchronizedSet` are correct if all access goes through the wrapper, but they serialize readers and writers. `ConcurrentHashMap` is the usual map choice under contention. Wrappers can still be fine when few threads, the collection is small, or it is read-mostly.

## One exclusion lock versus not

A synchronized wrapper is a mutex around a plain collection. Every method call takes that one lock on the wrapper. Threads queue. Compound actions that are not a single method (iterate the whole map, check-then-act) still need an explicit `synchronized` on the **same wrapper** — including the entire iterator loop. Miss that, and behavior is undefined. [[How do you obtain synchronized wrappers for standard Java collections]]

Concurrent collections in `java.util.concurrent` are thread-safe **without** a single client-visible exclusion lock. You cannot lock a `ConcurrentHashMap` to freeze the table for a multi-step update. Retrievals do not lock the whole map. Updates are built to overlap. Some types are non-blocking queues; `CopyOnWriteArrayList` / `CopyOnWriteArraySet` snapshot the array on writes. When many threads will access a map, `ConcurrentHashMap` is normally preferable to a synchronized `HashMap`; `ConcurrentSkipListMap` to a synchronized `TreeMap`. [[Why is ConcurrentHashMap faster than Hashtable]] [[How do you get a concurrent Set in Java]] [[What is CopyOnWriteArraySet]]

Iterators differ. Concurrent collections are **weakly consistent**: they traverse elements as they existed when constructed, may (but need not) reflect later writes, and do **not** throw `ConcurrentModificationException`. A synchronized wrapper’s iterator is still the backing collection’s fail-fast iterator. You must hold the wrapper lock for the whole traversal. [[Are ConcurrentHashMap iterators fail-fast]]

```java
Map<String, Integer> wrapped = Collections.synchronizedMap(new HashMap<>());
Map<String, Integer> concurrent = new ConcurrentHashMap<>();

synchronized (wrapped) {                 // required for the whole loop
    for (String key : wrapped.keySet()) {
        process(key);
    }
}

for (String key : concurrent.keySet()) { // weakly consistent; no wrapper lock
    process(key);
}
```

**Listing 1.** Same “thread-safe map” goal; only the wrapper needs a manual lock around iteration.

```java
Map<String, Integer> m = Collections.synchronizedMap(new HashMap<>());
if (!m.containsKey("a")) {
    m.put("a", 1);                       // two calls, two lock acquires — a race
}
concurrent.putIfAbsent("a", 1);          // one atomic map operation
```

**Listing 2.** A wrapper lock per method is not one atomic compound action. Concurrent maps add `putIfAbsent` / `compute` instead of “lock the whole table.”

```d2
direction: right
Wrapper: {
  lock: one mutex
  t1: thread A
  t2: thread B
  t1 -> lock: wait
  t2 -> lock: wait
}
CHM: {
  bins: ConcurrentHashMap
  t3: thread A
  t4: thread B
  t3 -> bins
  t4 -> bins
}
```

**Fig. 1.** Synchronized wrapper: every call takes the same lock. Concurrent map: overlapping access, no exclusive table lock.

> [!warning] Iteration still needs the wrapper lock
> `Collections.synchronizedMap` does not make a for-each loop safe by itself. You must `synchronized (theWrapper)` around the iterator. Concurrent iterators do not throw `ConcurrentModificationException`, but they are not a freeze of the whole collection. You also cannot `synchronized` on a `ConcurrentHashMap` to make several calls exclusive — that lock is not how the map is governed.

> [!tip] Interview answer
> **Reach for concurrent collections when many threads share the data.** A `Collections.synchronizedMap` wrapper is one lock on the whole object — correct, but it serializes every reader and writer, and you must still lock the wrapper to iterate. Concurrent types are not one exclusion lock; their iterators are weakly consistent and do not throw `ConcurrentModificationException`. Wrappers remain reasonable when contention is low or the collection is small or read-mostly.
