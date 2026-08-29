<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/Locks #Java/Concurrency/Synchronization/SynchronizedKeyword #SRS

# What is the difference between synchronized and ReentrantLock?

> [!abstract] Short answer
> **`synchronized`** takes an object’s **monitor** (`this` / `Class` / named object), **reentrant**, **auto-unlock** on exit (including throw). **`ReentrantLock`** is a **`Lock`** with the **same reentrant mutex idea**, but **you** **`lock()`/`unlock()`** (always **`finally`**). Extra: **`tryLock`**, **timed** lock, **`lockInterruptibly`**, optional **fairness**, **`newCondition()`** (several wait sets). **`wait`/`notify`** exist only on the **monitor**, not on the `Lock`. Keyword: [[What is the synchronized keyword for in Java]]. Monitor: [[What is monitor in Java]]. `Lock` buffer: [[How do you implement a bounded buffer with ReentrantLock]]. Same pair: [[What is the difference between synchronized and ReentrantLock]]. Static: [[On which object does a static synchronized method acquire a lock]]. Private mutex: [[Why might you synchronize on a private mutex object in Java]].

## Implicit monitor vs an explicit `Lock`

**`synchronized`:** instance method → **`this`**; **`static`** → declaring **`Class`**; **`synchronized (x)`** → **`x`**. Two instance `synchronized` methods on **one** object **share** **`this`** — they do **not** run together. Waiting for the monitor is **`BLOCKED`**; **interrupt does not abort** that wait (status sticks until you enter). Bytecode is **`monitorenter` / `monitorexit`**.

**`ReentrantLock`:** same **hold count** (enter again → unlock that many times). **`lock()`** is the blocking acquire. **`lockInterruptibly()`** can **give up** when interrupted. **`tryLock()`** polls. Fair mode ≈ FIFO; default **nonfair** (barging). **`Condition.await`/`signal`** replace **`wait`/`notify`** and you can have **more than one** condition per lock.

It is **not** “always faster than `synchronized`.” Prefer **`synchronized`** until you need **try/interrupt/fairness/`Condition`**.

```java
synchronized (lock) { n++; }

ReentrantLock rl = new ReentrantLock();
rl.lock();
try { n++; }
finally { rl.unlock(); }
if (rl.tryLock()) {
  try { n++; } finally { rl.unlock(); }
}
```

**Listing 1.** Same critical section. The `Lock` form is manual and can **poll**.

```d2
direction: down
s: "synchronized: auto unlock" {
  width: 240
  height: 36
  style.fill: "#e8f5e9"
}
r: "ReentrantLock: finally unlock" {
  width: 260
  height: 36
  style.fill: "#fff8e1"
}
s -> r: "need tryLock / interrupt / Condition"
```

**Fig. 1.** Same mutex idea. The `Lock` is for **control**, not a free speedup.

> [!warning] Forgot `unlock` and you never leave
> `synchronized` **cannot** leak the monitor past the block. A missed **`unlock()`** **deadlocks** everyone else on that `Lock`.

> [!warning] `lock()` is not `wait`
> Holding the `Lock` does not use **`Object.wait`**. Mix **`synchronized (rl)`** and **`rl.lock()`** and you have **two** locks.

> [!tip] Interview answer
> synchronized locks an object monitor and always unlocks when you leave the block, even if you throw. ReentrantLock is the same reentrant mutex as a Lock object, but I unlock in finally and I get tryLock, timed and interruptible acquire, fairness, and Condition. I do not switch to ReentrantLock just for speed.
