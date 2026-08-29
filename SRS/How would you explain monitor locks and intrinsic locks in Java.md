<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS

# How would you explain monitor locks and intrinsic locks in Java?

> [!abstract] Short answer
> **Monitor lock**, **intrinsic lock**, and **implicit / built-in monitor lock** are the **same thing**: the lock **every object** has. **Only one thread** holds a given monitor at a time; others **block** until they can lock it. A thread may lock the **same** monitor **again** (reentrant); each **unlock** undoes one **lock**. You take it with **`synchronized (obj)`**, a **`synchronized` instance method** (`this`), or a **`static synchronized` method** (the **`Class`** object). Unlock runs when the block/method **finishes**, even by exception. `java.util.concurrent.locks.Lock` is a **different** API; it must match the **same memory effects** as monitor lock/unlock, but **`synchronized (lockInstance)` is not `lock.lock()`**. What a monitor is: [[What is monitor in Java]]. Who holds it: [[How can you check if a thread holds a monitor lock in Java]]. You cannot assign the owner: [[Can Java code manually control which thread holds a monitor]].

## One monitor per object

`synchronized` computes an object, **locks its monitor**, runs the body, **unlocks** on the way out. Wait sets sit on the **same** object: `wait` **releases** the monitor and parks; `notify`/`notifyAll` wake waiters who must **reacquire** it — [[How would you explain the Object wait method and waiting on monitors]]. `Thread.sleep` **keeps** every monitor. Unlock of **m** happens-before a later lock of **m**. Survey: [[How do you synchronize access in a multithreaded Java application]]. Notify: [[How does notify differ from notifyAll in Java]].

`Thread.holdsLock(obj)` is **current thread** vs that object’s monitor (`assert` only). `Lock` adds `tryLock`, interruptible acquire, and `Condition`s, but you must **`unlock` in `finally`** — there is no automatic lexical release.

```java
final class Cell {
    private int n;
    synchronized void bump() { n++; }          // monitor of this
    static synchronized void classLock() {}    // monitor of Cell.class
    void other(Object m) { synchronized (m) { } }
}
```

**Listing 1.** Three ways to take an intrinsic lock. Nested `bump()` from the same thread reenters `this`.

```d2
direction: down
obj: "object / Class" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
mon: "one monitor\nreentrant" {
  width: 160
  height: 45
  style.fill: "#fff8e1"
}
wait: "wait set" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}
obj -> mon
obj -> wait
```

**Fig. 1.** Intrinsic lock + wait set are per object. `Lock` objects have their **own** monitor too — do not mix it with `lock()`.

> [!warning] `synchronized (aLock)` is not `aLock.lock()`
> A `Lock` is an ordinary object. Taking **its** monitor has **no specified relationship** to `lock()` / `unlock()`. Do not use `Lock` instances as `synchronized` targets except inside their own implementation.

> [!warning] Reentrant still needs balanced unlock
> Nested `synchronized` on the same object is fine. For `Lock`, every successful `lock` needs an `unlock`. Forgetting `finally` leaves the lock held.

> [!tip] Interview answer
> Intrinsic lock and monitor lock mean the lock every Java object has, taken with synchronized. Only one thread owns it at a time, but the same thread can reenter. wait and notify use that same monitor; Lock is a separate type that mimics the memory effects but is not that object’s synchronized lock.
