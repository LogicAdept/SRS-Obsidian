<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/SynchronizedKeyword #Java/Language #SRS

# What is the synchronized keyword for in Java?

> [!abstract] Short answer
> **`synchronized`** **locks an object’s monitor**, runs the body, then **unlocks** (even if the body throws). That is **mutual exclusion** plus **visibility** (unlock happens-before a later lock of the **same** monitor). **Instance method** → **`this`**. **`static` method** → that type’s **`Class`**. **Block** → the object you name. **Reentrant.** Not “make it parallel.” Waiters for the monitor are **`BLOCKED`**. Bytecode: **`monitorenter` / `monitorexit`**. Definition: [[What is synchronization]]. Monitor: [[What is monitor in Java]]. Blocks and pitfalls: [[How would you explain synchronized blocks in Java and common pitfalls]]. Static: [[On which object does a static synchronized method acquire a lock]]. Vs `Lock`: [[What is the difference between synchronized and ReentrantLock]].

## Lock, body, unlock

The statement evaluates a reference, **waits** until it can lock that monitor, then executes. A synchronized **method** is the same protocol on `this` or the `Class`. Reentrancy is a **nesting count**: lock N times, unlock N times. Other threads **block** until the count is back to zero.

`wait` / `notify` / `notifyAll` require **owning that same monitor** — [[Why must wait and notify run inside synchronized blocks]]. `Lock` is a different type with `tryLock` — [[How would you explain synchronization with synchronized and locks in Java]]. Two `synchronized` methods on **different** objects do **not** exclude each other. `static synchronized` on `Foo` does **not** lock `Foo` instances — [[On which object does a static synchronized method acquire a lock]].

```java
class Box {
    private int n;
    synchronized void bump() { n++; }                 // this
    static synchronized void typeLock() {}            // Box.class
    void other(Object m) { synchronized (m) { } }     // m
}
```

**Listing 1.** Three ways to take a monitor. `bump()` from the same thread can call itself (reentrant).

```d2
direction: down
enter: "synchronized" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
lock: "lock monitor" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
body: "run body" {
  width: 140
  height: 36
  style.fill: "#e8f5e9"
}
un: "unlock (always)" {
  width: 160
  height: 36
  style.fill: "#ffebee"
}
enter -> lock
lock -> body
body -> un
```

**Fig. 1.** Acquire, work, release. Visibility follows the unlock → later lock edge.

> [!warning] Same keyword, different objects, no exclusion
> `synchronized (a)` and `synchronized (b)` are independent. Publishing a lock object as `this` lets callers `synchronized (yourInstance)` and **join your protocol** whether you wanted that or not.

> [!warning] Exclusion is not a multi-field transaction by magic
> Everything in **one** synchronized region on **one** monitor is mutually exclusive. Two methods that lock **different** objects can still race on the same fields.

> [!warning] `synchronized` does not start threads
> It **serializes** a section so shared updates do not race. Use **`Thread.start` / an executor** for concurrency. The keyword does **not** freeze **unsynchronized** fields.

> [!tip] Interview answer
> synchronized takes an object’s monitor so only one thread runs that critical section at a time, and unlock makes prior writes visible to the next locker of the same monitor. Instance methods lock this, static methods lock the Class object, blocks lock whatever you pass. The same thread can reenter; wait and notify need that same monitor.
