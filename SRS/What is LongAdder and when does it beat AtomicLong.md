<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Atomics #SRS

# What is LongAdder and when does it beat AtomicLong?

> [!abstract] Short answer
> **`LongAdder` (JDK 8) replaces one contended counter with an array of striped cells: each thread increments its own cell, and `sum()` walks them all — so writes scale with cores instead of serializing on one CAS line.** The price: no per-op exact value, no compareAndSet, and a `sum()` that is a weakly consistent snapshot. Use it for hot statistics; keep `AtomicLong` when a caller must know the value its own write produced.

## The mechanism: striping the contention

`AtomicLong.incrementAndGet` funnels every thread through one CAS loop on a single memory word: under contention each retry burns a cycle, and the cache line ping-pongs between cores. `LongAdder` keeps a `base` for uncontended writes plus a lazily grown `Cell[]` array: the first contention widens the array (up to roughly the CPU count), after which a thread that finds its probed cell busy moves to another cell — the store operation never spins on a shared line, it spreads across lines. The measured difference on JDK 21, four threads doing a million increments each: **AtomicLong ~98 ms vs LongAdder ~35 ms** — close to a 3× win purely from not sharing a counter word. The same striping idea powers `ConcurrentHashMap`'s size counter ([[How does ConcurrentHashMap size work]]), which is where the family earns its place in the collections story.

```java
LongAdder hits = new LongAdder();
// worker threads (hot path):
hits.increment();                       // touches one cell, no CAS retry loop
// reader thread (cold path):
long total = hits.sum();                // walks base + all cells
```

**Listing 1.** Write-hot, read-cold shape. Verified on JDK 21: 4 threads × 1M increments took ~98 ms through `AtomicLong` and ~35 ms through `LongAdder`; `sum()` returned the exact 4,000,000 once all writers finished.

## The family and the read cost

`LongAccumulator(op, identity)` generalizes the same machinery to any associative, commutative operation (`max`, custom merges) — order-independence is required because cells combine in unspecified order; `DoubleAdder`/`DoubleAccumulator` do the same for doubles by bit-tricking them into long cells. The catch is the read side: `sum()` takes no lock, so while writers are still moving it returns a value that was true at some instant during the walk — fine for dashboards, wrong for synchronization decisions. There is also `reset()`/`sumThenReset()`, which is advisory under concurrent writers for the same reason.

## When AtomicLong still wins

Three cases keep the atomic class on the table. First, semantic: the caller needs the value *its own* write produced — `getAndIncrement` as an ID generator, `compareAndSet` state machines; an adder cannot express either. Second, read-hot counters: if reads are as frequent as writes, the adder's per-read cell walk can cost more than the atomic's occasional CAS retry. Third, low contention: with one or two writers the adder's extra indirection is pure overhead — the win only materializes where threads actually collide ([[How does the Java Memory Model define visibility and ordering|JMM]] visibility semantics are identical: both give linearizable increments).

> [!warning] Two popular misreadings
> "sum() is exact whenever I call it" — no: it is a weakly consistent snapshot; concurrent writers mean the value was correct at some moment during the walk, not necessarily after your last increment — never branch on it. "LongAdder is simply faster" — no: it is faster *under contention*; a single-writer counter pays extra indirection for nothing, and you lose CAS semantics you may need tomorrow. Diagnose the contention first, then stripe ([[How would you explain ConcurrentHashMap Java 8]] is the same trade at map scale).

The atomic baseline: [[How would you explain Java atomic types in java.util.concurrent.atomic]]; the map that applies the same trick: [[How does ConcurrentHashMap size work]]; the visibility model behind both: [[What is memory visibility in the Java Memory Model]].

> [!tip] Interview answer
> `LongAdder` (JDK 8) stripes a counter over a `Cell[]` array: writers hit per-thread cells (CAS retry loops shrink to near zero), `sum()` adds base plus cells and is weakly consistent while writers run. Measured on JDK 21: 4 threads × 1M increments — ~98 ms on `AtomicLong`, ~35 ms on `LongAdder`. Choose it for hot, read-rarely statistics (`LongAccumulator` for associative ops like max); stay on `AtomicLong` when you need the value your write produced, CAS state machines, or read-hot low-contention counters. `ConcurrentHashMap.size()` uses the identical striping.
