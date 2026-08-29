<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/Locks #SRS

# What is ReadWriteLock?

> [!abstract] Short answer
> A **`ReadWriteLock`** is a **pair of `Lock`s**, **not** a `Lock` itself: **`readLock()`** (shared) and **`writeLock()`** (exclusive). **Many readers** may hold the read lock **together**; a **writer** needs the write lock **alone**. A successful **read acquire sees** everything from the previous **write release**. The usual class is **`ReentrantReadWriteLock`**. Vs a single monitor: [[How would you explain monitor locks and intrinsic locks in Java]]. Vs `ReentrantLock`: [[What is the difference between synchronized and ReentrantLock]]. Optimistic variant: [[What is StampedLock]]. When you still want one mutex: [[How do you synchronize access in a multithreaded Java application]].

## Shared reads, exclusive writes

Use it when data is **read often and written rarely**, operations are **not tiny**, and you have **multiple cores**. If writes are frequent or reads are nanoseconds, a plain `ReentrantLock` / `synchronized` can win — the docs say **profile**.

**`ReentrantReadWriteLock`:** reentrant like `ReentrantLock`. A **writer may take the read lock** (downgrade: write, then read, then unlock write). A **reader cannot take the write lock** — upgrade **deadlocks**. To go from read to write: **unlock read**, lock write, **re-check** the invariant (another writer may have run). Default **nonfair**; fair mode is roughly arrival-order and a fair **read** waits if a **writer** is already queued. `tryLock` on the nested locks **does not** honor fairness. **`Condition` only on the write lock**; `readLock().newCondition()` throws. Instrumentation (`getReadLockCount`, …) is **monitoring**, not control. Max **65535** recursive holds per side.

`Lock` usage still needs **`unlock` in `finally`**.

```java
final ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();
final Lock r = rwl.readLock();
final Lock w = rwl.writeLock();

Data get(String key) {
    r.lock();
    try { return m.get(key); }
    finally { r.unlock(); }
}
Data put(String key, Data value) {
    w.lock();
    try { return m.put(key, value); }
    finally { w.unlock(); }
}
```

**Listing 1.** Official dictionary sketch: readers share `r`; mutators take exclusive `w`.

```d2
direction: down
mode: "writer holds writeLock?" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
ex: "exclusive: no other reader/writer" {
  width: 280
  height: 45
  style.fill: "#ffebee"
}
sh: "many readLocks OK" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
mode -> ex: "yes"
mode -> sh: "no"
```

**Fig. 1.** Reader-writer coordination: share while idle of writers; exclusive when writing.

> [!warning] Do not upgrade read → write in place
> A thread holding **only** the read lock that then calls `writeLock().lock()` **never succeeds**. Release the read lock first, take the write lock, **re-read** state.

> [!warning] Not a free speedup
> Short reads, hot writes, or a single core: extra complexity can **lose**. Concurrent collections (`ConcurrentHashMap`) often beat wrapping a `TreeMap` in this lock.

> [!tip] Interview answer
> ReadWriteLock gives a shared read lock and an exclusive write lock so many readers can proceed together. A write-lock release happens-before the next read-lock acquire, so readers see the writer’s updates. On ReentrantReadWriteLock I can downgrade write to read, but I cannot upgrade, and I always unlock in finally.
