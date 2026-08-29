<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/Locks #Java/Concurrency/Synchronization/SynchronizedKeyword #SRS

# What is the difference between synchronized blocks and java.util.concurrent locks?

> [!abstract] Short answer
> A **`synchronized` block** (or method) takes an object’s **monitor**: **reentrant**, **one wait set**, **unlocks automatically**. **`java.util.concurrent.locks`** is **library mutexes**: **`Lock` / `ReentrantLock`**, **`ReadWriteLock`**, **`StampedLock`**, **`Condition`**, **`LockSupport`**. Same idea (mutual exclusion + happens-before), but **you `unlock` in `finally`**, and you get **`tryLock`**, **interruptible / timed** acquire, **fairness**, **several conditions**, **shared/optimistic** modes. Vs `ReentrantLock` only: [[What is the difference between synchronized and ReentrantLock]]. Both styles: [[How would you explain synchronization with synchronized and locks in Java]]. Blocks: [[How would you explain synchronized blocks in Java and common pitfalls]]. Monitor: [[What is monitor in Java]]. RW / stamp: [[What is ReadWriteLock]], [[What is StampedLock]]. Collections are **not** this package: [[Why use concurrent collections instead of Collections synchronized wrappers]].

## Language monitor vs `locks` types

**`synchronized (x) { … }`:** bytecode **`monitorenter`/`monitorexit`**. **`wait`/`notify`** on **`x`**. Interrupt **does not abort** waiting to **enter**. Hold only the **shortest** region; a **private** lock object beats locking **`this`**.

**`Lock`:** **`lock`/`unlock`**, **`tryLock`**, **`lockInterruptibly`**, **`newCondition()`**. **`ReentrantLock`** matches monitor **reentrancy**. **`ReentrantReadWriteLock`:** many readers **or** one writer. **`StampedLock`:** stamps, **optimistic** read, **not reentrant**, **no owner**. **`Condition`** is the wait-set analogue (can have **several** per lock). None of that is **`ConcurrentHashMap`** — that is **`java.util.concurrent`** **collections**.

Use **`synchronized`** until you need those extras. **`Lock` is not faster by decree.**

```java
synchronized (lock) { n++; }

Lock rl = new ReentrantLock();
rl.lock();
try { n++; }
finally { rl.unlock(); }

ReadWriteLock rw = new ReentrantReadWriteLock();
rw.readLock().lock();
try { use(n); }
finally { rw.readLock().unlock(); }
```

**Listing 1.** Block vs explicit `Lock` vs shared read lock. Always `unlock` in `finally` on the library path.

```d2
direction: down
mon: "synchronized (obj): monitor" {
  width: 260
  height: 36
  style.fill: "#e8f5e9"
}
pkg: "j.u.c.locks: Lock / RW / StampedLock" {
  width: 320
  height: 40
  style.fill: "#fff8e1"
}
mon -> pkg: "need try / interrupt / readers / stamps"
```

**Fig. 1.** Same job: exclude other lockers. The package is for **API shape**, not a different memory model.

> [!warning] `locks` ≠ concurrent collections
> **`ConcurrentHashMap`**, **`CopyOnWriteArrayList`**, **`BlockingQueue`** live next door. They are **not** `Lock` replacements for `synchronized (map)`.

> [!warning] Mixing styles on one object
> `synchronized (rl)` and `rl.lock()` are **two** locks. `wait` does not pair with **`Condition.signal`**.

> [!tip] Interview answer
> synchronized is the language monitor: you enter a block and it always unlocks. java.util.concurrent.locks is Lock, read-write, StampedLock, and Condition, where I unlock in finally and I can tryLock or wait interruptibly. I stay with synchronized until I need that control, and I do not confuse those types with concurrent collections.
