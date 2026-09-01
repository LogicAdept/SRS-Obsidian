<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Concurrency #SRS

# How does `ConcurrentHashMap` use Segment locks in Java 7?

> [!abstract] Short answer
> **The table is an array of `Segment`s, and each `Segment` is a small hash table that extends `ReentrantLock`.** A writer locks **only** the segment its key hashes to. `get` does not take that lock: it volatile-reads the segment table and `HashEntry.value`. Java 8 dropped this as the live lock scheme ([[How does ConcurrentHashMap use CAS and synchronized in Java 8]]).

## One lock per stripe, not per map

Java 7 class docs: retrievals do not entail locking, and there is no way to lock the entire table ([[Does ConcurrentHashMap get lock the whole table]]). Updates are partitioned. `concurrencyLevel` (default **16**) is a **hint** for how many concurrent writers to try to accommodate without contention. The constructor rounds it up to a power of two (`ssize`) and allocates `segments[ssize]`, capped at `MAX_SEGMENTS` (`1 << 16`). More writers than stripes still run; they just share a lock. Placement is random, so actual concurrency varies.

That **16** is easy to mix with default **initial capacity 16** — two different knobs ([[What is concurrencyLevel in ConcurrentHashMap]]).

```d2
direction: down
map: "ConcurrentHashMap\nSegment[] (power of two)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
s0: "Segment 0\nReentrantLock + HashEntry[]" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
s1: "Segment 1\n…" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
get: "get: volatile reads, no lock" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
map -> s0
map -> s1
s0 -> get
s1 -> get
```

**Fig. 1.** High bits of the key hash pick a `Segment`. Low bits pick a bin inside that segment’s own table.

`Segment` “subclasses from `ReentrantLock` opportunistically” so mutative methods can `tryLock` / `lock` / `unlock` without a second lock object. `put` hashes, finds or creates the segment, then `Segment.put`: `tryLock`, or `scanAndLockForPut` (prescan with `tryLock` to soak cache misses), then under the lock walks the bin, inserts or replaces, `unlock`s. Other segments stay usable. `get` indexes the segment with a volatile read, then the bin, and returns `e.value` — `HashEntry.value` and `next` are `volatile`; the segment comment says lists stay readable without locking.

Each segment resizes **itself** while it holds its lock: if `count + 1` would exceed that segment’s threshold, `rehash(node)` doubles **that** `HashEntry[]` and installs the new node on the new table. It is not a whole-map rehash, and `get` can still walk old lists because nodes are cloned when `next` would change.

```java
// Conceptual — Java 7 stripe, not a JDK listing
static final class Segment<K,V> extends ReentrantLock {
    volatile HashEntry<K,V>[] table;
    transient int count;
    // put: tryLock or scanAndLockForPut, then mutate, unlock
}

V get(Object key) {
    int h = hash(key.hashCode());
    Segment<K,V> s = volatileSegmentFor(h); // high bits
    // volatile bin read; walk HashEntry; return e.value — no lock()
}

V put(K key, V value) {
    Segment<K,V> s = segmentFor(hash); // create if missing
    return s.put(key, hash, value, false); // ReentrantLock this stripe only
}
```

**Listing 1.** `get` never calls `lock()`. `put` locks one `Segment`. `count` is a plain `int` published under that lock, not a `volatile` field.

`size()` may eventually lock **all** segments after unlocked `modCount` retries ([[How does ConcurrentHashMap size work]]). Java 8 still serializes a dummy `Segment[]` for compatibility; that class is not the runtime lock table ([[Why did ConcurrentHashMap drop segment locks in Java 8]]). The type itself dates to Java 5 ([[In which Java version was ConcurrentHashMap introduced]]).

> [!warning] `concurrencyLevel` is not a thread cap
> It sizes the stripe array (power of two, default 16, max 65536). It does not reject a 17th writer. A bad hash distribution still piles keys onto one segment, so you get one lock and a long list — Java 7 has no tree bins.

> [!warning] Java 8 `Segment` is leftover serialization
> Seeing `static class Segment extends ReentrantLock` in a current JDK source does not mean puts still lock stripes. Live Java 8+ updates CAS an empty bin or `synchronized` the bin head. Default capacity **16** and default `concurrencyLevel` **16** are also not the same field.

> [!tip] Interview answer
> **Java 7 `ConcurrentHashMap` is a `Segment[]` of mini hash tables, each a `ReentrantLock`.** Writers lock only the stripe their key hashes to; `get` is volatile reads of `HashEntry.value`. `concurrencyLevel` (default 16) sizes that array as a hint, not a hard concurrency limit. Java 8 replaced this with per-bin CAS plus `synchronized`.
