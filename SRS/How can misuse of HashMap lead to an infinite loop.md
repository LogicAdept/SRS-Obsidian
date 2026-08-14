<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Concurrency #Java/Concurrency #Java/Versions/8 #SRS

# How can misuse of `HashMap` lead to an infinite loop?

> [!abstract] Short answer
> **Concurrent structural updates on an unsynchronized `HashMap` are undefined.** The famous CPU-spinning `get` was a **pre-Java 8** implementation: `resize` moved a bin by reversing the `next` chain (`transfer`). Two threads doing that on the same list could make a node point at itself or at a cycle; later `get`/`put` never saw `next == null`. Java 8+ `resize` keeps relative order and does not reverse that way. The map is still not thread-safe. Use `ConcurrentHashMap` or an external lock.

## The spec does not promise a loop — it forbids the sharing

The `HashMap` javadoc: the implementation is **not synchronized**. If several threads use the map and one of them adds or deletes mappings, you must synchronize externally. Fail-fast iterators may throw `ConcurrentModificationException`; that is best-effort, not a livelock detector. [[Is java.util.HashMap thread safe]] is the contract.

The infinite-loop interview question is about what **OpenJDK used to do** when that rule was broken, not a documented API.

## Pre-Java 8: reverse the bin while moving it

Through Java 7, `resize` allocated a larger `Entry[]` and `transfer` walked each chain, **prepending** each node onto the new bucket:

```java
Entry<K,V> next = e.next;
int i = indexFor(e.hash, newCapacity);
e.next = newTable[i];
newTable[i] = e;
e = next;
```

**Listing 1.** Conceptual OpenJDK 7 `transfer`. Insert-at-head reverses the list. That was legal: `HashMap` iteration order is unspecified.

```d2
direction: down
two: "Two threads resize\nthe same bin" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
rev: "Each prepends nodes\nonto newTable[i]" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
cyc: "next forms a cycle" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
get: "get walks next\nnever null" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}

two -> rev -> cyc -> get
```

**Fig. 1.** A data race on `e.next` / `newTable[i]`, not a specified `Map` operation. A later lookup that follows `next` until null never returns.

That is misuse: sharing a `HashMap` across writers without a lock. Lost entries and corrupt tables were also possible. The hang was just the most dramatic symptom.

## Java 8+ changed `resize`, not the thread-safety story

Java 8 `HashMap` rebuilds bins by splitting on one hash bit and **preserving** `next` order (`lo`/`hi` tails, then `loTail.next = null`). [[How and when does HashMap resize its buckets]] is that path. The old `transfer` reverse is gone, so **that** cycle recipe does not apply. Concurrent `put` is still unspecified: you can still lose mappings or see a broken table. Java 8 did **not** make `HashMap` a concurrent map. Tree bins (JEP 180) are for collision performance, not for threads.

The supported replacements remain `Collections.synchronizedMap` or `ConcurrentHashMap`. [[How does Hashtable differ from ConcurrentHashMap]] is the concurrent table.

> [!warning] “Java 8 fixed HashMap, so it is thread-safe”
> It fixed a particular list-reversal. The class is still unsynchronized. Do not reproduce the race in production to “see the loop.” The correct demo is: don’t share `HashMap` with writers; use a concurrent map.

> [!tip] Interview answer
> **Unsynchronized concurrent `put`/`resize` on `HashMap` is undefined. Before Java 8, `transfer` reversed each bin; two resizes could cycle `next`, so `get` spun forever. Java 8 resize keeps order, so that hang is not the current implementation, but `HashMap` is still not thread-safe. Use `ConcurrentHashMap` or a lock.**
