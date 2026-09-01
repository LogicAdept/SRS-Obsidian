<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers #Java/JMM #SRS

# How would you explain the volatile field modifier in Java?

> [!abstract] Short answer
> **`volatile`** is a **field** modifier (never `final` at the same time). The memory model then treats each **write** to that field as a **release** that **happens-before** every **later read** of the **same** field: other threads see a **consistent** value, and the accesses happen as many times, and in the same order, as the program text of each thread. It is **not** a lock, **not** a CPU-cache contract, and **not** atomicity for **`i++`**. Vs atomics: [[What is the difference between volatile fields and atomic variables]]. Compound updates: [[How does volatile visibility differ from atomicity for compound updates]]. Reference fields: [[What does volatile on a reference field guarantee for visibility]].

## Consistent value, not exclusive use

Locking is the usual way to give a thread exclusive use of shared variables. `volatile` is a **second** mechanism, more convenient when you only need **visibility and ordering**, not mutual exclusion. Two threads may still run in parallel; they just cannot each keep a private, stale copy of that field.

A write to `v` **synchronizes-with** later reads of `v` (synchronization order). That edge is a **happens-before**, so the write is **visible to and ordered before** those reads. Happens-before is **transitive**: writes the writer made **before** the volatile store are visible to a reader that has done the matching volatile load. That is why a `volatile` **reference** can publish an otherwise unsynchronized object — the object’s fields are visible **after** the reader sees the reference, not because those fields are themselves `volatile`.

Reads and writes of **`volatile long` / `double`** are **atomic** as 64-bit values (a non-volatile `long`/`double` write may be two 32-bit halves). **`volatile int n; n++;`** is still **read, add, write**: two threads can lose an increment. Use **`AtomicInteger`**, **`LongAdder`**, or a **monitor**. JMM overview: [[How would you explain memory Java]]. Happens-before list: [[How would you explain the happens-before guarantee in the Java Memory Model]].

```java
class Stop {
    volatile boolean stop; // writer stores true; reader loops on stop
}

class LostUpdate {
    volatile int n;
    void bump() { n++; } // not atomic: two bumps can both read the same n
}
```

**Listing 1.** A stop flag is the usual `volatile` use. Incrementing a `volatile int` is not a single atomic update.

```d2
direction: down
w: "write volatile v" {
  width: 170
  height: 40
  style.fill: "#e8f5e9"
}
r: "later read of v" {
  width: 170
  height: 40
  style.fill: "#e3f2fd"
}
w -> r: "happens-before\n(same field)"
```

**Fig. 1.** One field, write then later read. No exclusion: both threads may still run.

> [!warning] Visibility is not atomicity and not a mutex
> `i++` on a `volatile` counter can drop updates. `volatile` does not keep other threads out of a critical section.

> [!warning] Not “flush L1 / do not cache in registers”
> The language guarantee is **happens-before** and a **consistent** value, not a hardware cache protocol. A field cannot be both `final` and `volatile`.

> [!tip] Interview answer
> Volatile makes a write to that field happen-before later reads of the same field, so other threads see a consistent value. It is not a lock and it does not make i-plus-plus atomic. For a compound update I use an atomic integer or a synchronized block.
