<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Concurrency #SRS

# Does `ConcurrentHashMap` `get` lock the whole table?

> [!abstract] Short answer
> **No.** Retrievals, including `get`, do not take a lock, and the class has no way to lock the entire table. Readers overlap with `put` / `remove`. That is the opposite of `Hashtable`, whose `get` is `synchronized` on the map itself.

## Retrievals stay lock-free; updates do not freeze the table

The contract is older than the Java 8 rewrite: full concurrency of retrievals, no whole-table lock, and `get` may run at the same time as an update. A completed write for a key happens-before a later **non-null** `get` of that same key. A null `get` means absent — values cannot be null ([[Does ConcurrentHashMap allow null keys or values]]).

`Hashtable.get` is a synchronized method, so every lookup takes the same monitor as every write. Independent keys still queue. `ConcurrentHashMap` has no equivalent “lock the map” API, so you cannot freeze it for a check-then-act compound the way you can with `synchronized (hashtable) { ... }`.

```d2
direction: right
ht: "Hashtable.get\nsynchronized(this)\nwhole table" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
chm: "ConcurrentHashMap.get\nvolatile / acquire reads\nno lock" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
put: "put / remove\nCAS empty bin\nelse synchronized(bin head)" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
ht -> chm: "not this"
chm -> put: "writers only"
```

**Fig. 1.** `get` never takes the table lock. Writers lock at most one bin head (Java 8+), not the whole map.

Java 8+ `get` hashes, acquire-reads the bin (`tabAt`), and walks the list or tree through `volatile` `val` / `next`. There is no `synchronized` on that path. `putVal` CASes an empty bin; if the bin already has a node, it `synchronized` on that first node, then re-checks it is still the head. Java 7 `get` was the same idea: volatile reads of the segment table and `HashEntry.value`, no lock. `Segment.put` took that segment’s `ReentrantLock`. `concurrencyLevel` is now only a sizing hint. Bin-lock details: [[How does ConcurrentHashMap use CAS and synchronized in Java 8]]. Segment era: [[How does ConcurrentHashMap use Segment locks in Java 7]].

```java
// Conceptual — lock story, not a copy of the JDK method
V chmGet(Object key) {
    Node<K,V>[] tab = table;                 // volatile table
    Node<K,V> e = tabAt(tab, indexFor(key)); // acquire-read of one bin
    // match head, else walk volatile next / tree find
    return e == null ? null : e.val;         // volatile val; no monitor
}

synchronized V hashtableGet(Object key) {    // locks the Hashtable instance
    // walk that one bucket under the same lock every writer uses
    return foundValue;
}
```

**Listing 1.** `ConcurrentHashMap.get` publishes with volatile/acquire reads. `Hashtable.get` is `synchronized`, so it locks the whole table.

```java
import java.util.Hashtable;
import java.util.concurrent.ConcurrentHashMap;

class Demo {
    static void lookups() {
        var chm = new ConcurrentHashMap<String, Integer>();
        chm.put("a", 1);
        Integer fromChm = chm.get("a"); // overlaps other puts; no table lock

        var ht = new Hashtable<String, Integer>();
        ht.put("a", 1);
        Integer fromHt = ht.get("a"); // exclusive with every other ht method
    }
}
```

**Listing 2.** Same call shape, different exclusion: only `Hashtable` serializes the lookup on `this`.

Iterators are weakly consistent for the same reason — they do not take a table lock and they never throw `ConcurrentModificationException` ([[Are ConcurrentHashMap iterators fail-fast]]). `Hashtable` drawbacks, including whole-table `synchronized`: [[How would you explain drawbacks of the legacy Hashtable class]].

> [!warning] No table lock is not a compound-action lock
> Two `get`s, or `get` then `put`, are still racy. There is no `synchronized (concurrentHashMap)` protocol that excludes other threads. Use `putIfAbsent`, `compute`, `merge`, or `replace` when the update must see a single mapping.

> [!warning] “No lock on get” is not “no memory ordering”
> Visibility comes from volatile/acquire reads of the table, bin, `next`, and `val`, plus the happens-before from a completed write to a non-null `get` of that key. `put` still locks: empty bin via CAS, occupied bin via `synchronized` on the head (Java 8+), or a segment `ReentrantLock` in Java 7. Long `compute*` functions may block **other updates** while the function runs; they do not make `get` lock the table.

> [!tip] Interview answer
> **No. `ConcurrentHashMap.get` does not lock the table — retrievals are specified not to entail locking, and there is no whole-map lock.** Visibility is volatile/happens-before, not a mutex. `Hashtable.get` is `synchronized` on the map, so even independent reads contend. Writes lock a bin (or, in Java 7, a segment), never the entire table.
