<!--
reps: 0
priority: 0
-->
#Java/JMM #SRS

# Why is the Java increment operator not atomic

> [!abstract] Short answer
> **`i++` compiles to three separate steps — read the value, add one, write it back — and two threads can interleave between them, so one update overwrites the other.** The operator *looks* atomic because it is one source line; at the JVM and memory level it is a read-modify-write with no synchronization. Fixes: `AtomicInteger.incrementAndGet()` (lock-free CAS) or a `synchronized` block.

## The interleaving that loses updates

On a plain (or even volatile!) field, `i++` behaves like `i = i + 1`. If two threads both read `i == 5`, both compute `6`, and both write `6` — one of the two increments is lost. `volatile` changes nothing here: it guarantees the write is *visible*, not that read-add-write happens as one unit.

```d2
direction: down
t1: "T1 reads i = 5" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
t2: "T2 reads i = 5" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
c1: "T1 writes i = 6" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
c2: "T2 writes i = 6\n(lost update: 7 expected)" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
t1 -> c1
t1 -> t2
t2 -> c2
```

**Fig. 1.** Both threads read the same starting value; the second write erases the first — one of two increments vanishes.

```java
public class IncrementRaceDemo {
    static int plain = 0;
    static java.util.concurrent.atomic.AtomicInteger atomic =
            new java.util.concurrent.atomic.AtomicInteger(0);

    public static void main(String[] args) throws Exception {
        int threads = 10, perThread = 100_000, expected = threads * perThread;

        Thread[] ts = new Thread[threads];
        for (int t = 0; t < threads; t++)
            ts[t] = new Thread(() -> { for (int i = 0; i < perThread; i++) plain++; });
        for (Thread t : ts) t.start();
        for (Thread t : ts) t.join();
        System.out.println("plain int: " + plain + " (expected " + expected + ")");

        ts = new Thread[threads];
        for (int t = 0; t < threads; t++)
            ts[t] = new Thread(() -> { for (int i = 0; i < perThread; i++) atomic.incrementAndGet(); });
        for (Thread t : ts) t.start();
        for (Thread t : ts) t.join();
        System.out.println("AtomicInteger: " + atomic.get() + " (expected " + expected + ")");
    }
}
```

**Listing 1.** Run on JDK 21:

```java
plain int: 962312 (expected 1000000)
AtomicInteger: 1000000 (expected 1000000)
```

**Listing 2.** Ten threads, one hundred thousand increments each: the plain `int` lost 37 688 updates in this run (the exact number varies run to run — 136 180 on a second run), while the CAS-based `AtomicInteger` hit the expected count exactly. A synchronized block around `guarded++` also reproduces 1 000 000.

## Why the atomic version works

`AtomicInteger.incrementAndGet()` is a single machine-level compare-and-swap loop: it retries until its read-compute-write lands as one atomic step, so interleavings cannot split it. The `synchronized` variant achieves the same by mutual exclusion — and adds the happens-before edges that publish the value ([[How would you explain the happens-before guarantee in the Java Memory Model]]). Choose the atomic class for counters and CAS-friendly updates, the lock when several variables must change together.

> [!warning] volatile does not fix the increment — and "small method" is not atomicity
> Two traps. First, the famous one: `volatile int i; i++` still loses updates, because visibility never implies atomicity — the read-modify-write is still three steps racing ([[What is memory visibility in the Java Memory Model]]). Second, the reverse lie: "i++ is one bytecode instruction, so it is atomic". Even where a single `iinc` instruction is used, the JMM grants no atomicity to it across threads; only `long`/`double` non-volatile *accesses* have a documented tearing question (word tearing is excluded, but there is no atomic read-modify-write anywhere). Counting correctness comes from CAS or locking, never from operator syntax. The spec-level framing: this is a data race — [[What is the difference between a race condition and a data race]] — within the broader visibility rules of [[How does the Java Memory Model define visibility and ordering]].

> [!tip] Interview answer
> **Because i++ is read-modify-write — three steps — and threads interleave: two threads read 5, both write 6, one increment is lost. One line of source does not mean one memory operation. volatile does not help; it fixes visibility, not atomicity. Use AtomicInteger.incrementAndGet, which is a CAS loop, or synchronize the block — our stress run lost tens of thousands of updates on a plain int and exactly zero with AtomicInteger.**

