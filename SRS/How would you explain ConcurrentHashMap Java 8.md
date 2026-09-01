<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Versions/8 #Java/Collections/Concurrency #SRS

# How would you explain `ConcurrentHashMap` Java 8?

> [!abstract] Short answer
> **Same 1.5 concurrent map, new table:** a `Node[]` of bins, lock-free `get`, `put` that CASes an empty bin and `synchronized`s the bin head when occupied, trees after enough collisions, no nulls, and atomic `computeIfAbsent`. Segment locks are gone. It is not a `synchronized Hashtable` and not a CopyOnWrite snapshot.

## The Java 8 picture

The type is still `@since 1.5` ([[In which Java version was ConcurrentHashMap introduced]]). Java 8 rewrote the **implementation** so updates are not striped `ReentrantLock`s ([[Why did ConcurrentHashMap drop segment locks in Java 8]], [[How does ConcurrentHashMap use Segment locks in Java 7]]).

Contract that interviews mix with HashMap/`Hashtable`:

* Thread-safe; retrievals do not lock the table; no whole-map lock ([[Does ConcurrentHashMap get lock the whole table]]).
* No null key or value ([[Does ConcurrentHashMap allow null keys or values]]).
* Iterators are **weakly consistent** — no `ConcurrentModificationException` ([[Are ConcurrentHashMap iterators fail-fast]]). They do not clone the map the way CopyOnWrite copies its array ([[What are Java CopyOnWrite collections]]).
* `size()` / `mappingCount()` are estimates under concurrent writes ([[How does ConcurrentHashMap size work]]).
* `concurrencyLevel` is a leftover sizing hint, not the lock count ([[What is concurrencyLevel in ConcurrentHashMap]]).

```d2
direction: down
tab: "Node[] table" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
empty: "empty: CAS first Node" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
list: "list: synchronized(head)" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
tree: "TreeBin if ≥8 nodes\nand table length ≥64" {
  width: 280
  height: 55
  style.fill: "#fce4ec"
}
tab -> empty
tab -> list
tab -> tree
```

**Fig. 1.** Java 8 bins. `get` walks `volatile` `val` / `next` with no monitor.

`putVal` ([[How does ConcurrentHashMap use CAS and synchronized in Java 8]]): init table if needed; empty slot → CAS; `MOVED` (−1) → help resize; else `synchronized` on the first node, re-check it is still the head, then list-append or `TreeBin`. `TREEIFY_THRESHOLD` is 8, but `treeifyBin` **resizes** while capacity is under 64. `get` never takes that lock.

Caches and histograms: `computeIfAbsent` is the atomic if-absent insert ([[Why should you use computeIfAbsent on ConcurrentHashMap]], [[How do you avoid a check-then-act race on ConcurrentHashMap]]). `containsKey` then `put` still races. The mapping function must not re-enter the map.

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.LongAdder;

class Demo {
    static void java8() {
        ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
        m.put("a", 1);                          // CAS or synchronized(head)
        Integer v = m.get("a");                 // no table lock
        m.computeIfAbsent("b", k -> 2);         // atomic if absent
        ConcurrentHashMap<String, LongAdder> freqs = new ConcurrentHashMap<>();
        freqs.computeIfAbsent("a", k -> new LongAdder()).increment();
        long n = m.mappingCount();              // long estimate; since 1.8
    }
}
```

**Listing 1.** The Java 8 APIs you actually name in an interview: bin-locked `put`, lock-free `get`, atomic `computeIfAbsent`, `mappingCount`.

> [!warning] Treeify-at-8 is not unconditional
> Eight nodes in a bin trigger `treeifyBin` only if the table is already large enough (64). A tiny table grows instead. `MOVED == -1` is a forwarding node, not a user `hashCode`.

> [!warning] `java.util.concurrent` is not “no races left”
> Individual methods are thread-safe without an external lock. Two-call sequences are not. Do not freeze the map with `synchronized (chm)`. `CopyOnWriteArrayList` is a different trade: copy-on-write snapshot iterators, costly mutative copies — not how this map iterates.

> [!tip] Interview answer
> **Java 8 `ConcurrentHashMap` is a `Node[]`: lock-free `get`, CAS into an empty bin, `synchronized` on the bin head otherwise, trees for bad collision chains, no nulls.** Segments are gone; `computeIfAbsent` is the atomic cache insert. It is still the 1.5 concurrent map — only the locking story changed.
