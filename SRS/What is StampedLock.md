<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/Locks #SRS

# What is StampedLock?

> [!abstract] Short answer
> **`StampedLock`** is a **capability-based** reader/writer lock with **three modes**: **write** (exclusive), **read** (shared), and **optimistic read** (`tryOptimisticRead` + **`validate`**). Acquire methods return a **stamp**; **0** means try failed. It does **not** implement **`Lock`** or **`ReadWriteLock`** (use **`asReadLock()`** / **`asWriteLock()`** / **`asReadWriteLock()`** views). **Not reentrant.** **No owner** — another thread may unlock or convert a stamp. Vs RW: [[What is ReadWriteLock]], [[What is ReadWriteLock]]. Vs mutex: [[What is the difference between synchronized and ReentrantLock]]. No-owner cousin: [[What is Semaphore]].

## Stamp, then unlock that stamp

**Write:** `writeLock()` → `unlockWrite(stamp)`. Blocks readers; optimistic **`validate` fails**. **Read:** `readLock()` → `unlockRead(stamp)`. **Optimistic:** `tryOptimisticRead()` is **nonzero** only if **not write-locked**. **`validate(stamp)`** is true if **no write** ran since that stamp; then the last **write unlock happens-before** the optimistic read. Otherwise the field reads may be **garbage** — copy to locals, **validate**, retry or take a real read lock.

**`tryConvertToWriteLock(stamp)`** can upgrade when you are already writing, the **sole** reader, or optimistic and the lock is free. **Try** methods are **best-effort**, not fair. Stamps are **not** secrets and **recycle** after long uptime. For **internal** thread-safe components whose data you understand — not a drop-in mutex.

```java
StampedLock sl = new StampedLock();
long stamp = sl.tryOptimisticRead();
int a = x, b = y;
if (!sl.validate(stamp)) {
  stamp = sl.readLock();
  try { a = x; b = y; }
  finally { sl.unlockRead(stamp); }
}
```

**Listing 1.** Optimistic snapshot; fall back to a read lock if a writer intervened.

```d2
direction: down
opt: "tryOptimisticRead" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
val: "validate(stamp)" {
  width: 150
  height: 36
  style.fill: "#e8f5e9"
}
rd: "readLock / writeLock" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
opt -> val
val -> rd: "false: take a real lock"
```

**Fig. 1.** Optimistic mode is a weak read: a writer can break it at any time.

> [!warning] Not reentrant
> Nested `writeLock()` / `readLock()` on the same thread **deadlocks**. Do not call unknown code that might lock again.

> [!warning] Optimistic reads are inconsistent until `validate`
> Use them for **short, side-effect-free** field copies. Unvalidated data must not drive writes or alien methods.

> [!tip] Interview answer
> StampedLock is a reader-writer lock that also has optimistic reads: you take a stamp, copy fields, and validate that no writer ran. It is not a Lock, it is not reentrant, and it has no owner, so you unlock with the stamp you got. I use it inside a class I control, not as a general mutex.
