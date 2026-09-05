<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Concurrency/Atomics #SRS

# How does volatile visibility differ from atomicity for compound updates?

> [!abstract] Short answer
> **`volatile` is visibility (and ordering), not a mutex.** A write to a `volatile` field happens-before a later read of **that** field. It does **not** make `++`, `x = x + 1`, or “check then set” a **single** action. Those are **read–modify–write**: two threads can both read the same value and both write. For one counter, use **`AtomicInteger`** (`incrementAndGet` / `getAndAdd`) or a lock. CAS vs fetch-and-add: [[Compare compare and swap with fetch and add]]. Volatile on a reference: [[What does volatile on a reference field guarantee for visibility]].

## Happens-before without exclusion

`volatile` reads/writes have memory effects **like** unlocking then locking a monitor, **without** mutual exclusion. Two threads can execute `n++` on a `volatile int` at once: each reads, adds one, writes. You can lose updates. That is a **data race** on the RMW, even though each `volatile` read/write is ordered with the matching write/read of the same field.

A **compound** update is any sequence that must look atomic to others: increment, `if (x == 0) x = 1`, pushing two fields that must stay a pair. `volatile` on one field does not freeze the others. A `volatile` **reference** publishes the object it points to only as far as **safe publication of that reference**; mutating the object’s non-volatile innards is still a race — [[What is the difference between volatile fields and atomic variables]].

`AtomicInteger` / `VarHandle.getAndAdd` / `compareAndSet` perform the RMW as **one** atomic operation (with the documented memory effects). For several fields, use **`synchronized`** or `ReentrantLock` — [[How do you synchronize access in a multithreaded Java application]].

```java
import java.util.concurrent.atomic.AtomicInteger;

public final class VolatileVsAtomic {
    private volatile int v;
    private final AtomicInteger a = new AtomicInteger();

    public void bumpVolatile() {
        v++; // not atomic
    }

    public void bumpAtomic() {
        a.incrementAndGet();
    }
}
```

**Listing 1.** `v++` is get, add, put on a volatile field — three steps. `incrementAndGet` is one RMW.

```d2
direction: down
v: "volatile write → later read\nhappens-before" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
rmw: "n++ / check-then-act\nnot one action" {
  width: 260
  height: 55
  style.fill: "#fce4ec"
}
at: "AtomicInteger / lock\natomic compound" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
v -> rmw: "does not imply"
rmw -> at: "need"
```

**Fig. 1.** Seeing the latest `n` is not the same as updating `n` without lost increments.

> [!warning] `volatile boolean` stop flag is visibility, not a transaction
> Other state you mutate before setting the flag still needs its own HB (or stay immutable). The flag only orders **that field**.

> [!warning] `volatile long` / `double` is not “++ is atomic”
> 64-bit types have extra torn-read rules when **not** `volatile`. Making them `volatile` fixes **visibility of a single write**, not increment.

> [!tip] Interview answer
> `volatile` makes one write visible to a later read of that field. It does not make `++` atomic. For a counter I use `AtomicInteger` or a lock. For a flag, `volatile` is enough if I only store the flag.
