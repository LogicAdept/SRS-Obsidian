<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/Locks #Java/Concurrency/Synchronization/SynchronizedKeyword #SRS

# How would you explain synchronization with synchronized and locks in Java?

> [!abstract] Short answer
> **`synchronized`** takes an object’s **monitor** (intrinsic lock): **one owner**, **reentrant**, auto **unlock** when the method/block ends. **`java.util.concurrent.locks.Lock`** (`ReentrantLock`) is the same **exclusive** idea with **`tryLock`**, **timeouts**, **`lockInterruptibly`**, and **`Condition`s**, but you **`unlock` in `finally`**. **`ReadWriteLock`** splits **shared read** vs **exclusive write**. **`StampedLock`** adds **optimistic read** (stamp + `validate`) for short, side-effect-free reads; it is **not reentrant** and has **no owner**. Survey: [[How do you synchronize access in a multithreaded Java application]]. Monitors: [[How would you explain monitor locks and intrinsic locks in Java]]. `synchronized` vs `ReentrantLock`: [[What is the difference between synchronized and ReentrantLock]]. Readers/writers: [[What is ReadWriteLock]].

## Block-structured monitors vs explicit `Lock`

`synchronized (obj)` / synchronized methods lock **that object’s monitor**. Static methods lock **`Class`**. Unlock happens-before a later lock of the **same** monitor. `wait`/`notify` need that monitor — [[How would you explain synchronized blocks in Java and common pitfalls]]. `Lock` matches those **memory effects** on successful `lock`/`unlock`, but acquisition **need not** be lexical: hand-over-hand locking is allowed, and **you** must release. Do **not** `synchronized (lockInstance)` — that monitor is unrelated to `lock()`.

**`ReentrantLock`:** optional **fairness**; `newCondition()` for multiple wait-sets. **`ReentrantReadWriteLock`:** many readers or one writer; **downgrade** write→read; **no** read→write upgrade. **`StampedLock`:** write / read / **`tryOptimisticRead`**. Optimistic mode is a **weak** read that a writer can invalidate; copy fields to locals and **`validate`**. Designed as an **internal** tool; `asReadLock()` if you need a `Lock` view. j.u.c locks vs blocks: [[What is the difference between synchronized blocks and java.util.concurrent locks]].

```java
synchronized (mutex) { /* one thread; auto unlock */ }

Lock lock = new ReentrantLock();
lock.lock();
try { /* same exclusive idea */ }
finally { lock.unlock(); }
```

**Listing 1.** Monitor vs `Lock`. Interrupted/timed acquire exists only on the `Lock` side (`lockInterruptibly`, `tryLock(time, unit)`).

```d2
direction: down
mon: "synchronized\nmonitor, auto unlock" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
rl: "ReentrantLock\ntryLock, interrupt, Condition" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
rw: "ReadWriteLock\nshared read / exclusive write" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
st: "StampedLock\noptimistic read + stamp" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
mon -> rl: "need try/interrupt"
rl -> rw: "many readers"
rw -> st: "short optimistic reads"
```

**Fig. 1.** Same job (coordinate access); more knobs as you leave `synchronized`.

> [!warning] `StampedLock` is not a drop-in `ReentrantLock`
> **Not reentrant.** A nested call that locks again deadlocks. Optimistic reads can see **torn** fields until `validate` succeeds. Release/convert with the **matching stamp**.

> [!warning] `Lock.unlock` is on you
> No compiler-enforced `finally`. Unlocking from the wrong thread is implementation-defined (`ReentrantLock` requires the holder; `StampedLock` has **no ownership**).

> [!tip] Interview answer
> synchronized is the built-in reentrant monitor with automatic unlock. ReentrantLock adds timed and interruptible acquire and Condition wait-sets, but I unlock in finally. ReadWriteLock lets many readers share; StampedLock adds optimistic reads when I can validate a snapshot, and it is not reentrant.
