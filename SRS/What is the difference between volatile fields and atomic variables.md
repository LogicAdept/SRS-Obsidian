<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Concurrency/Atomics #SRS

# What is the difference between volatile fields and atomic variables?

> [!abstract] Short answer
> **`volatile`:** a **single** read or write is **visible** and **ordered** (write happens-before a later read of **that** field). It does **not** make **`i++`** atomic. **`AtomicInteger` / `AtomicReference` / …:** **volatile-quality** gets/sets **plus** **atomic compound** ops (`incrementAndGet`, **`compareAndSet`**, `getAndUpdate`). **`volatile long`/`double`** are atomic as **one write**; still no `++`. Compound vs visibility: [[How does volatile visibility differ from atomicity for compound updates]]. `volatile`: [[How would you explain the volatile field modifier in Java]]. Atomics: [[How would you explain Java atomic types in java.util.concurrent.atomic]]. CAS: [[What is the difference between compareAndSet and weakCompareAndSet]]. Reference publish: [[What does volatile on a reference field guarantee for visibility]].

## One access vs a read-modify-write

**`volatile`:** compiler/CPU must not treat the field as a thread-private cache. A **reference** write publishes that object (with **transitive** happens-before for prior writes in the writer). **`i++`** is still **read, add, write** — two threads **lose updates**. Non-volatile **`long`/`double`** may **tear**; **`volatile`** (or an atomic) avoids that.

**Atomic classes:** `get`/`set` like **`volatile`**. **`incrementAndGet`** is one atomic RMW. **`compareAndSet`** is a **strong volatile CAS**. They are **not** a lock around **several** fields: two `AtomicInteger`s can still **race** as a pair. For a **boolean flag** or a **published reference**, **`volatile`** is enough.

```java
volatile int v;
v++; // not atomic

AtomicInteger a = new AtomicInteger();
a.incrementAndGet(); // atomic RMW
a.compareAndSet(0, 1); // CAS
```

**Listing 1.** Visibility on `v` does not compose `++`. The atomic API does.

```d2
direction: down
vol: "volatile: one read or write" {
 width: 240
 height: 36
 style.fill: "#fff8e1"
}
at: "Atomic*: RMW / CAS too" {
 width: 220
 height: 36
 style.fill: "#e8f5e9"
}
vol -> at: "need i++ / CAS"
```

**Fig. 1.** Same visibility story for a **single** access. Atomics add **indivisible updates**.

> [!warning] `volatile int` is not an atomic counter
> Use **`AtomicInteger`** (or a **lock**) for **`++` / `+=`**.

> [!warning] One atomic field ≠ one invariant
> Transferring between two accounts still needs **one lock** (or a **designed** atomic protocol). Two CAS variables do not make the **pair** atomic.

> [!tip] Interview answer
> volatile makes a single read or write visible and ordered, but increment is still three steps. AtomicInteger adds atomic increment and compareAndSet with the same kind of volatile memory effects. I use volatile for flags and published references, and atomics when I need a lock-free update of one variable.
