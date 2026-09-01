<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #Java/JVM/Memory #SRS

# How does `WeakHashMap` use `ReferenceQueue`?

> [!abstract] Short answer
> **Each entry is a `WeakReference` registered with a private queue.** After the key becomes weakly reachable, the collector clears that reference and **enqueues** it. The map does **not** sit on `remove()`. On the next table access it **`poll()`s** the queue and unlinks those entries (`expungeStaleEntries`). Removal is not instantaneous when you drop the last strong ref.

## Enqueue is the GC; expunge is the next `get`/`put`

`java.lang.ref`: register a reference with a queue if you want notification after the matching reachability change. The collector then clears the reference and appends it to the queue. A hashtable with weak keys can **poll** that queue on each access instead of dedicating a thread. That is how `WeakHashMap` is specified to work. `poll()` returns a reference immediately if one is waiting, otherwise `null` — it does not block. `remove()` would block; this map does not use that. [[What is WeakHashMap used for]] [[How do you attach extra data to an object with WeakHashMap]]

Implementation (`jdk-21-ga`): `Entry` extends `WeakReference` and is constructed with `super(key, queue)`. `getTable()` (used by `get`, `put`, `containsKey`, resize, …) calls `expungeStaleEntries()`, which loops `queue.poll()` and splices each returned `Entry` out of its bucket, nulls the strong value, and decrements `size`.

```d2
direction: down
gc: "GC: key weakly reachable\nclear WeakReference\nenqueue Entry" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
poll: "next get/put/size\nqueue.poll()" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
exp: "unlink bucket node\nvalue = null" {
  width: 260
  height: 70
  style.fill: "#c8e6c9"
}

gc -> poll
poll -> exp
```

**Fig. 1.** Two steps. Between them, `size()` may still count a key the collector has already logically discarded.

```java
// Conceptual: not a copy of WeakHashMap
ReferenceQueue<Object> queue = new ReferenceQueue<>();
// Entry e = new WeakReference(key, queue) { V value; ... };

public V get(Object key) {
    // getTable() → expungeStaleEntries()
    for (Object x; (x = queue.poll()) != null; ) {
        // unlink x from table[indexFor(hash)], drop value
    }
    // then hash lookup
    return null;
}
```

**Listing 1.** Conceptual: poll on access, never `queue.remove()`. Official `size()` javadoc: the count is a snapshot and may include unprocessed stale entries until the next access.

`clear()` drains the queue with `poll()` and then nulls the table (GC during allocation may enqueue more; it polls again). The **null key** uses a static sentinel, so that `WeakReference` is never cleared by GC. [[Does WeakHashMap allow null keys or values]] [[What happens to a WeakHashMap entry when the last strong reference to the key is dropped]] [[How does WeakHashMap work]]

Not synchronized for callers. Expunge synchronizes on the queue only while splicing. Iterators are fail-fast for structural mods; GC-looking removal can still look like another thread. [[Why not build a SoftHashMap on SoftReferences the way WeakHashMap uses WeakReferences]]

> [!warning] “The entry vanishes the instant I drop the key”
> Enqueue happens after the collector decides the key is weakly reachable, on its schedule. The row stays in the array until some map operation **polls**. Do not write a loop that waits on `ReferenceQueue.remove` expecting `WeakHashMap` to do that for you. Soft refs to the key delay weak enqueue: weakly reachable means not strongly **and** not softly reachable.

> [!tip] Interview answer
> **`WeakHashMap` entries are weak references registered on a `ReferenceQueue`.** When the GC clears a key, that entry is enqueued. The map `poll`s the queue on access (`get`/`put`/`size`, …) and then removes the mapping. It is not instant and it does not block on the queue.
