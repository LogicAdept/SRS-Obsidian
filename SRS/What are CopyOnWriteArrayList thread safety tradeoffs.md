<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency/CopyOnWrite #SRS

# What are `CopyOnWriteArrayList` thread safety tradeoffs?

> [!abstract] Short answer
> **Readers can traverse without a client lock; every mutation copies the whole array.** That copy is ordinarily too costly. The type wins when traversals vastly outnumber writes — listener lists, rare config changes. It loses when writes are frequent or the list is large. Iterators are a **snapshot**: no `ConcurrentModificationException`, and they do not see later updates.

## Snapshot reads versus copy-on-write

`CopyOnWriteArrayList` is a thread-safe `ArrayList` variant. Mutative operations (`add`, `set`, `remove`, …) replace the underlying array with a fresh copy. Traversal does not need a `synchronized` block on the list. That is the point versus `Collections.synchronizedList`: you can iterate while another thread mutates, without holding the list lock for the whole loop. [[Why use concurrent collections instead of Collections synchronized wrappers]] [[How do you obtain synchronized wrappers for standard Java collections]]

The iterator (and spliterator) is snapshot-style: it keeps the array as of construction. That array never changes for the life of the iterator, so interference is impossible and `ConcurrentModificationException` is guaranteed not to be thrown. The iterator will **not** reflect later adds, removes, or `set`s. `Iterator.remove` / `set` / `add` throw `UnsupportedOperationException`. [[What is the difference between CopyOnWriteArrayList and ArrayList]]

`CopyOnWriteArraySet` is the set-shaped sibling built on the same copy-on-write list. `null` elements are allowed, unlike `ConcurrentHashMap`. [[What is CopyOnWriteArraySet]] [[What are Java CopyOnWrite collections]]

```java
CopyOnWriteArrayList<Runnable> listeners = new CopyOnWriteArrayList<>();
listeners.add(listener);                 // copies the array

for (Runnable listener : listeners) {    // snapshot; no lock around the loop
    listener.run();
}
```

**Listing 1.** The usual fit: many traversals, rare `add` / `remove`.

```java
Iterator<Runnable> it = listeners.iterator();
listeners.add(another);                  // new array; `it` still sees the old snapshot
it.remove();                             // UnsupportedOperationException
```

**Listing 2.** Snapshot isolation is the safety model, not a live view. The iterator cannot mutate the list.

```d2
direction: down
Write: add / set / remove {
  copy: fresh array copy
}
Read: iterator / get {
  snap: snapshot of the array at start
}
Write.copy -> cost: O(n) per mutation
Read.snap -> safe: no CME, no later writes
```

**Fig. 1.** Thread safety is paid for on the write path. Reads see a frozen array.

> [!warning] Snapshot is not “fail-safe live,” and reads are not a lock-free queue
> An iterator will miss updates that happen after it was created. That is by design, not a bug. Do not call this a lock-free collection in the `ConcurrentLinkedQueue` sense: the win is **no client lock on traversal**, while each mutation still copies every element. A hot write loop on a large `CopyOnWriteArrayList` is the wrong tool.

> [!tip] Interview answer
> **`CopyOnWriteArrayList` copies the entire array on every mutation so traversals need no client lock.** Iterators are snapshots: they never throw `ConcurrentModificationException` and they never see later writes. Use it when reads vastly outnumber writes, such as listener lists. Frequent mutation makes the copy cost the wrong tradeoff.
