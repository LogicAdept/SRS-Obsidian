<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #Java/JMM #SRS

# How do you synchronize access in a multithreaded Java application?

> [!abstract] Short answer
> Give every shared mutable location a **happens-before**. The language mutex is **`synchronized`** (instance monitor or the `Class` for `static synchronized`). `java.util.concurrent.locks` (`ReentrantLock`, `Condition`) is the explicit form. For a **single variable**, `volatile` or an **atomic**. For a **structure**, a concurrent collection (`BlockingQueue`, `ConcurrentHashMap`) rather than a raw `HashMap`. Sharing without that is a **data race** — [[How do you share data between two threads in Java]].

## One lock story, then libraries

`synchronized (obj) { … }` and synchronized instance methods lock **`obj` / `this`**. `static synchronized` locks the **`Class`** object. Unlock of that monitor happens-before the next lock of it. `wait` / `notify` / `notifyAll` use the **same** monitor — [[How do methods wait and notify notifyAll]]. Do not lock a publicly reachable `this` if callers might `synchronized (yourInstance)` by accident; a **private** lock object is the usual encapsulation.

`ReentrantLock` matches that mutex and adds `lockInterruptibly`, timed `tryLock`, fairness, and **several `Condition` wait-sets** — [[What is the difference between synchronized and ReentrantLock]]. Always `lock(); try { … } finally { unlock(); }`.

A **`volatile` write** happens-before a later read of that field. It does not make `++` atomic. `AtomicInteger` / `VarHandle.compareAndSet` (and `getAndAdd`) do single-variable RMWs — [[Compare compare and swap with fetch and add]].

`j.u.c` collections document their own HB (`BlockingQueue.put` before `take`). `HashMap` / `ArrayList` / `EnumMap` are **not** synchronized — [[Is EnumMap synchronized]]. `Collections.synchronizedMap` is one mutex on the wrapper; iterate under `synchronized (m)`.

`Thread.start` happens-before the new thread’s `run`; a successful **`join`** happens-before the joiner continues. That is how you publish to a worker without a shared lock.

```java
public final class SyncedCounter {
    private int n;

    public synchronized void inc() {
        n++;
    }

    public synchronized int get() {
        return n;
    }
}
```

**Listing 1.** One monitor, both mutator and reader. `n++` without `synchronized` (or an `AtomicInteger`) is a race even if `n` is `volatile`.

```d2
direction: down
share: "shared mutable state" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
mon: "synchronized / ReentrantLock" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}
one: "volatile / atomic field" {
  width: 260
  height: 45
  style.fill: "#fff8e1"
}
col: "concurrent collection" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
share -> mon: "compound actions"
share -> one: "one variable"
share -> col: "queue or map"
```

**Fig. 1.** Pick the smallest tool that still orders the accesses you care about.

> [!warning] `synchronized` on the wrong object does nothing
> Two methods that lock **different** objects do not exclude each other. Static and instance methods use **different** monitors (`Class` vs `this`).

> [!warning] A concurrent collection does not make your **invariants** atomic
> `ConcurrentHashMap` get/put are thread-safe. “Check then put if absent” still needs `putIfAbsent` (or a lock) if that pair must be one action.

> [!tip] Interview answer
> I synchronize on a private lock or use `ReentrantLock` for compound updates, `volatile` or atomics for one flag or counter, and a concurrent collection for a queue or map. I do not share an unsynchronized `HashMap`. The point is happens-before, not sprinkling `synchronized` on every method.
