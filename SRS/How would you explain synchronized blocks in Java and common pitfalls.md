<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/SynchronizedKeyword #SRS

# How would you explain synchronized blocks in Java and common pitfalls?

> [!abstract] Short answer
> A **`synchronized (expr) { body }`** evaluates **`expr`**, **rejects `null`**, **locks that object’s monitor**, runs the **block**, then **unlocks** even if the block **throws**. The lock is the same kind as a **`synchronized` method**. **Reentrancy:** one thread may nest `synchronized` on the **same** `V`. **Pitfall:** taking the monitor does **not** stop other threads from touching **fields** or calling **unsynchronized** methods on that object. Keyword: [[What is the synchronized keyword for in Java]]. `wait`/`notify`: [[Why must wait and notify run inside synchronized blocks]]. Vs `Lock`: [[What is the difference between synchronized blocks and java.util.concurrent locks]].

## Evaluate, lock, block, unlock

The expression must be a **reference type**. If evaluation **aborts**, the statement aborts and **no lock** is taken. Then **`null` → `NullPointerException`**. Then lock **`V`**, execute, unlock on **normal or abrupt** completion. Nested `synchronized (t) { synchronized (t) { ... } }` is legal — [[How would you explain monitor locks and intrinsic locks in Java]].

**Common mistakes**

- **Half-guarded state.** `synchronized` setters and a **plain** getter still race. Mutual exclusion is only among threads that lock **that same** monitor.
- **Wrong object.** `synchronized (a)` and `synchronized (b)` do not exclude. `static` methods lock **`Class`**, not instances — [[On which object does a static synchronized method acquire a lock]].
- **`synchronized (this)` as API.** Callers can `synchronized (yourInstance)` and enter **your** protocol.
- **`wait` on another object** than the one you locked → **`IllegalMonitorStateException`**.
- **Deadlock.** Two threads take **A then B** vs **B then A**. The language does not prevent it.
- **Mixing `Lock.lock()` with `synchronized (theLock)`.** Those are **unrelated** monitors.

```java
class Cell {
    private int n;
    synchronized void set(int v) { n = v; }
    int get() { return n; } // pitfall: not on the same monitor
}
```

**Listing 1.** `get` is not synchronized. Locking `this` in `set` does not stop another thread from reading `n` without the lock.

```d2
direction: down
eval: "evaluate expr" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
npe: "null → NPE" {
  width: 140
  height: 36
  style.fill: "#ffebee"
}
lock: "lock V, run block, unlock" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
eval -> npe: "null"
eval -> lock: "non-null V"
```

**Fig. 1.** Block protocol. The monitor does not magically fence unsynchronized access.

> [!warning] The lock is not a force field on the object
> Other threads may still read and write fields and call methods that are **not** `synchronized` on **that** monitor. You must put **every** conflicting access on the same lock.

> [!warning] `synchronized (null)` throws
> The expression is evaluated first. A lock field that is still `null`, or `synchronized (map.get(k))` when missing, never enters the block.

> [!tip] Interview answer
> A synchronized block locks the object the expression names, runs the body, and always unlocks, including on exceptions. The classic pitfall is thinking the object is fully protected: only code that also locks that monitor is excluded. I use a private final lock object so callers cannot join the protocol, and I never wait on a different object than I synchronized on.
