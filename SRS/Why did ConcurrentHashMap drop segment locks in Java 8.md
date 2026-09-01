<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Versions/8 #Java/Collections/Concurrency #SRS

# Why did `ConcurrentHashMap` drop segment locks in Java 8?

> [!abstract] Short answer
> **A `Segment` lock was too coarse and too heavy for the design goals: lock-free reads, low update contention, and HashMap-like footprint.** Java 8 CASes the first node into an empty bin (the usual `put`) and `synchronized`s on that node when the bin is occupied — no extra lock object per bin, no stripe covering unrelated keys. `Segment` remains only for serialization.

## What stripes got wrong

Java 7 locked a whole `Segment` (`ReentrantLock`) for every mutating key that hashed to that stripe ([[How does ConcurrentHashMap use Segment locks in Java 7]]). Unrelated keys shared the monitor. Default **16** stripes also meant **16** lock objects up front, while `concurrencyLevel` was only a hint ([[What is concurrencyLevel in ConcurrentHashMap]]). `get` was already lock-free; the pain was **updates** and **space**.

The Java 8 source states the goals: keep concurrent `get` / iteration, **minimize update contention**, keep space about the same as `HashMap`, and allow many threads to insert into an empty table. A stripe lock fights all four.

```d2
direction: right
old: "Java 7 Segment\nReentrantLock covers many bins" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
neu: "Java 8 bin\nCAS if empty\nsynchronized(head) if not" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
old -> neu: "finer, fewer objects"
```

**Fig. 1.** Dropping segments is not “CAS instead of locking.” Occupied bins still take a monitor — one node, not a stripe.

How they built it ([[How does ConcurrentHashMap use CAS and synchronized in Java 8]]):

* Empty bin: `casTabAt` the first `Node`. Most puts under a decent hash never enter `synchronized`.
* Occupied bin: `synchronized` on that first node, then re-check it is still the head. No separate lock object per bin — the node **is** the lock (`synchronized` monitors, not a `ReentrantLock` per stripe).
* Long collision lists become `TreeBin`s (specialized red-black trees) so hostile `hashCode`s stay `O(log n)` instead of a giant stripe list.
* Resize is cooperative (`MOVED` forwarding nodes); other threads help instead of waiting on one segment rehash.
* `concurrencyLevel` is leftover sizing; a stub `Segment` is written only for old serialized streams.

`ReentrantLock` on Java 7 segments had a second failure mode: a `StackOverflowError` inside `lock()` could leave the lock unusable. Parallel class loading used `ConcurrentHashMap`, so a corrupted stripe could deadlock the VM. The rewrite’s `synchronized` bin heads are not those `ReentrantLock` instances. That is a JDK 7/8 robustness story, not the dump’s “HotSpot made `synchronized` faster.”

Reads still do not lock the table ([[Does ConcurrentHashMap get lock the whole table]]). Versus `HashMap`: same bin/tree shape, plus publication ([[What is the difference between HashMap and ConcurrentHashMap]]). The type is still 1.5 ([[In which Java version was ConcurrentHashMap introduced]]). Counting is a striped `LongAdder`-style counter, not a locked segment walk ([[How does ConcurrentHashMap size work]]).

```java
// Conceptual — why the two Java 8 put arms exist
// empty bin:  casTabAt(...)                    // no monitor; common case
// occupied:   synchronized (head) { ... }      // one bin, not a Segment
// never:      segments[i].lock();              // gone from the live table
```

**Listing 1.** Design the map as a `Node[]` with CAS + bin-head monitors, not as `Segment[]` of mini-`Hashtable`s.

> [!warning] “Java 8 is CAS” skips the colliding `put`
> CAS installs the **first** node only. A second key in that bin takes `synchronized` on the head. Other keys in the same bin share that monitor — still far smaller than a Java 7 stripe, not lock-free writes.

> [!warning] Do not quote JDK 6 `synchronized` folklore as the spec
> The implementation comment chooses builtin monitors so there is **no extra lock object per bin**. It does not say “HotSpot biased locking beat `ReentrantLock`.” Seeing `class Segment extends ReentrantLock` in current source is serialization compatibility, not live striping.

> [!tip] Interview answer
> **Segments serialized too many unrelated keys and cost extra `ReentrantLock` objects.** Java 8 keeps lock-free `get`, CASes empty bins, and locks only the bin head with `synchronized` — plus trees for collisions. `concurrencyLevel` no longer picks a lock table. CAS is the empty-bin path, not the whole map.
