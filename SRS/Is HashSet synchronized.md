<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Concurrency #SRS

# Is `HashSet` synchronized?

> [!abstract] Short answer
> **No.** `HashSet` is not synchronized. Concurrent readers plus a writer (or two writers) need an external lock, a `Collections.synchronizedSet` wrapper, or a concurrent set such as `ConcurrentHashMap.newKeySet()`. Fail-fast iterators are not a lock.

## The class is a plain `HashMap` underneath

The Java SE 21 class comment states the implementation is **not synchronized**. If multiple threads access a hash set and at least one modifies it, you must synchronize externally. The backing structure is a `HashMap`, which is also unsynchronized ([[How is HashSet implemented in terms of HashMap]]). There is no hidden monitor on `add` / `contains` / `remove`.

The documented wrap is `Collections.synchronizedSet`, **at creation**, so nothing else keeps a raw `HashSet` reference:

```java
Set<String> s = Collections.synchronizedSet(new HashSet<>());
s.add("a"); // safe: goes through the wrapper

synchronized (s) {
    Iterator<String> i = s.iterator();
    while (i.hasNext()) {
        i.next();
    }
}
```

**Listing 1.** Wrapper methods are synchronized on the returned set. **Iteration is not.** `Collections.synchronizedSet` requires you to lock that same object for `Iterator`, `Spliterator`, or `Stream` traversal. Skipping the `synchronized (s)` block is unspecified concurrent access ([[How do you obtain synchronized wrappers for standard Java collections]]).

```d2
direction: down
raw: "HashSet\nnot synchronized" {
  width: 240
  height: 70
  style.fill: "#ffcdd2"
}
wrap: "Collections.synchronizedSet\none lock; iterate under synchronized(s)" {
  width: 360
  height: 80
  style.fill: "#fff3e0"
}
chm: "ConcurrentHashMap.newKeySet()\nconcurrent set; no nulls" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}

raw -> wrap
raw -> chm
```

**Fig. 1.** Three answers to “I need a hash set and threads.” The default constructor is none of the thread-safe ones.

`HashSet` iterators are **fail-fast**: a structural change from another path can throw `ConcurrentModificationException`. That check is best-effort and is **not** a happens-before protocol. Do not use CME as a lock, and do not treat “I have not seen a CME” as proof the set is safely published.

## Concurrent set vs locked `HashSet`

`ConcurrentHashMap.newKeySet()` (and `newKeySet(int)`) creates a `Set` backed by a `ConcurrentHashMap` to `Boolean.TRUE`. Retrievals do not lock the whole table; iterators do not throw `ConcurrentModificationException` ([[Are ConcurrentHashMap iterators fail-fast]]). That is the usual replacement when a single wrapper lock on every `HashSet` call is too coarse ([[Why use concurrent collections instead of Collections synchronized wrappers]]).

The trade: like `ConcurrentHashMap` / `Hashtable`, **null is forbidden**. `HashSet` permits one null element ([[Does HashSet allow a null element]]); `newKeySet().add(null)` is a `NullPointerException` ([[Does ConcurrentHashMap allow null keys or values]]).

External locking on a private mutex that encapsulates the set is the other documented option. Then every access, including iteration, must take that same lock. Publishing the raw `HashSet` beside the wrapper (or locking a different object than `Collections.synchronizedSet` returned) breaks the serial-access rule.

> [!warning] Wrapping does not lock `for-each`
> `for (E e : synchronizedSet)` still calls `iterator()` **outside** a lock unless you wrap the loop in `synchronized (s)`. The javadoc’s example is the contract. Two threads iterating without that lock is the same bug as two threads on a raw `HashSet`.

> [!warning] Fail-fast is not thread safety
> `ConcurrentModificationException` from a `HashSet` iterator means “I noticed a `modCount` change,” not “the other thread’s `add` was ordered with mine.” Unsynchronized concurrent mutation remains a data race on the table.

> [!tip] Interview answer
> **No — `HashSet` is not synchronized; it is an unsynchronized `HashMap` of keys.** For a locked set, wrap at creation with `Collections.synchronizedSet` and synchronize on that wrapper when you iterate. For a concurrent hash set, use `ConcurrentHashMap.newKeySet()`, and remember it rejects `null`.
