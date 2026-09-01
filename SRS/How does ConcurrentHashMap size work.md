<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Concurrency #SRS

# How does `ConcurrentHashMap` `size` work?

> [!abstract] Short answer
> **It does not lock the table and it is not a stable snapshot under concurrent writes.** Class docs: `size` / `isEmpty` / `containsValue` are for a quiet map, or as a monitoring estimate — not for control decisions. Java 8+ sums a `LongAdder`-style striped counter (`mappingCount()` is the `long` form). Java 7 summed per-segment counts, retried on `modCount` drift, then locked every segment.

## An aggregate, not a mutex

There is no whole-map lock ([[Does ConcurrentHashMap get lock the whole table]]), so a walk or a counter sum can overlap puts and removes. `size()` returns an `int` and saturates at `Integer.MAX_VALUE`. `mappingCount()` (Java 8) is the same estimate as a `long`, and its javadoc says the actual count may differ if insertions or removals are in flight. `isEmpty()` uses the same counter and treats a transient negative sum as empty.

```d2
direction: right
j7: "Java 7 size()\nsum Segment.count\nretry on modCount\nthen lock all segments" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
j8: "Java 8+ size() / mappingCount()\nsumCount: baseCount + CounterCells\nno table lock" {
  width: 300
  height: 110
  style.fill: "#e8f5e9"
}
j7 -> j8: "rewritten"
```

**Fig. 1.** Same public `size()` contract; two counters. Java 8 dropped the “retry, then lock every segment” path.

Java 8+ maintains the element count with a `LongAdder` specialization: CAS `baseCount` when uncontended; on collision, stripe into `CounterCell`s (`volatile long value`). `size()` / `mappingCount()` / `isEmpty()` all call `sumCount()` (base plus cells). Reads can cache-thrash if you hammer `size()` on a hot map — that is why resize checks do not re-read the counter on every single-node put. The cells are a count, not a walk of the bins, so they can be briefly negative while updates race.

Java 7 `size()` summed each `Segment`’s `count`. A plain sum can tear while another thread mutates, so the method retried while the sum of per-segment `modCount` stayed unstable (`modCount` increments on that segment’s `put` / `remove`). After `RETRIES_BEFORE_LOCK` (2) unlocked passes, it locked **every** segment, counted once, then unlocked. `count` was an ordinary `int` published by lock/volatile-read pairing, not a `volatile` field. Segment mechanics: [[How does ConcurrentHashMap use Segment locks in Java 7]].

```java
// Conceptual — two generations of the same API
int sizeJava8() {
    long n = sumCount(); // baseCount + CounterCell.value
    if (n < 0L) return 0;
    if (n > Integer.MAX_VALUE) return Integer.MAX_VALUE;
    return (int) n;
}

int sizeJava7() {
    // unlocked: sum Segment.count until Σ modCount is stable
    // if still moving after a few tries: lock all segments, count, unlock
    return overflow ? Integer.MAX_VALUE : size;
}
```

**Listing 1.** Java 8+ never takes segment locks to answer `size()`. Java 7 only did that after retries failed.

```java
import java.util.concurrent.ConcurrentHashMap;

class Demo {
    static void monitor(ConcurrentHashMap<String, Integer> map) {
        int n = map.size();           // int; caps at Integer.MAX_VALUE
        long m = map.mappingCount();  // Java 8; same estimate, long
        // fine for logs / dashboards; not a predicate for "is full"
    }
}
```

**Listing 2.** Prefer `mappingCount()` when the map can outgrow `int`. Neither call is a linearizable census under concurrent updates.

Weakly consistent iterators have the same “no table lock” reason ([[Are ConcurrentHashMap iterators fail-fast]]). Do not use `size() == 0` then `put` as a unique-insert protocol — that is a check-then-act race ([[How do you avoid a check-then-act race on ConcurrentHashMap]]).

> [!warning] Do not branch on `size()` under writers
> `if (map.size() == n)` can be stale before the next line. The class page says aggregate status is not for program control while other threads update. There is no `size() == capacity` invariant you can wait on; capacity is internal (`sizeCtl`), and the count is a striped estimate.

> [!warning] Java 7 “sum twice, then lock” is not Java 8
> Interview dumps mix the segment algorithm with today’s `mappingCount()`. Java 8+ `size()` does not lock all bins. Dumps that call `Segment.count` `volatile` are also off: it was a plain `int` with lock/volatile-read discipline. `mappingCount()` is still an **estimate**, not a locked recount.

> [!tip] Interview answer
> **`size()` does not lock the whole map.** Under concurrent puts it is a monitoring estimate — Java 8+ sums `baseCount` plus striped `CounterCell`s; Java 7 summed segment counts, retried on `modCount`, then locked every segment. Use `mappingCount()` for a `long`. Do not use `size()` as a control predicate while other threads write.
