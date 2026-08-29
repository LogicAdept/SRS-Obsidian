<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS

# What synchronization mechanisms exist in Java?

> [!abstract] Short answer
> **Language:** **`synchronized`** (per-object **monitor** + **`wait`/`notify`**), **`volatile`**, **`final`** freeze. **Locks:** **`ReentrantLock`**, **`ReadWriteLock`**, **`StampedLock`**, **`Condition`**. **Synchronizers:** **`CountDownLatch`**, **`CyclicBarrier`**, **`Phaser`**, **`Semaphore`**. **Atomics / `VarHandle`**. **`BlockingQueue`**. **`Thread.join` / `start`** are happens-before edges too. Prefer **j.u.c** over rolling **`wait`/`notify`**. Definition: [[What is synchronization]]. Keyword: [[What is the synchronized keyword for in Java]]. Package: [[How would you explain the java.util.concurrent package]]. Monitor vs `Lock`: [[What is the difference between synchronized and ReentrantLock]]. `volatile` vs atomic: [[What is the difference between volatile fields and atomic variables]]. Latch vs barrier: [[What is the difference between CyclicBarrier and CountDownLatch]].

## Language first, then the concurrent library

**Monitor:** exclusive owner, reentrant, auto-unlock. **`volatile`:** one access visible/ordered, not `i++`. **`final`:** freeze after the constructor for safe publication.

**`Lock`:** `tryLock` / interruptible / `Condition` (several wait sets). **RW / stamp:** readers or optimistic reads. **Semaphore:** permit count. **Latch:** one-shot zero. **Barrier / Phaser:** rendezvous (Phaser is dynamic). **Atomics:** CAS / RMW. **`BlockingQueue`:** producer-consumer without a hand-rolled wait loop.

These are **tools**, not a pile you apply all at once. Shared mutable state still needs **one** story.

```java
synchronized (lock) { n++; }
volatile boolean ready;
new CountDownLatch(n).await();
ReentrantLock rl = new ReentrantLock();
rl.lock();
try { n++; } finally { rl.unlock(); }
```

**Listing 1.** Monitor, `volatile`, a latch, and an explicit `Lock`.

```d2
direction: down
lang: "synchronized / volatile / final" {
 width: 280
 height: 36
 style.fill: "#e8f5e9"
}
juc: "locks / synchronizers / atomics / queues" {
 width: 340
 height: 40
 style.fill: "#fff8e1"
}
lang -> juc: "need tryLock, parties, CAS, put/take"
```

**Fig. 1.** The keyword is the monitor. `java.util.concurrent` is everything else you reach for next.

> [!warning] A list is not a design
> Two `synchronized` methods on **`this`** still share **one** lock. A **`ConcurrentHashMap`** is not a **transaction**.

> [!warning] `wait`/`notify` are last resort
> **`Condition`**, **`BlockingQueue`**, **`CountDownLatch`** already encode the usual patterns.

> [!tip] Interview answer
> Java has monitors via synchronized and wait notify, plus volatile and final for visibility. The concurrent package adds Lock, read-write and stamped locks, latches barriers phasers semaphores, atomics, and blocking queues. I start with synchronized or a concurrent collection and only use the fancier types when I need tryLock, a rendezvous, or CAS.
