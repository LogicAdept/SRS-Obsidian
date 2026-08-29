<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS

# What is a monitor in Java?

> [!abstract] Short answer
> Every Java **object** has a **monitor**: a lock **one thread** may **own**, plus a **wait set**. **`synchronized` (this / `Class` / named object)** **locks** that object’s monitor; **`wait` / `notify` / `notifyAll`** use the **same** object’s wait set and require that you **already hold** the lock. Ownership is **reentrant**. Intrinsic locks: [[How would you explain monitor locks and intrinsic locks in Java]]. `wait`: [[How would you explain the Object wait method and waiting on monitors]]. `synchronized`: [[What is the synchronized keyword for in Java]]. Static: [[On which object does a static synchronized method acquire a lock]]. `holdsLock`: [[How can you check if a thread holds a monitor lock in Java]].

## Lock plus wait set, per object

**Lock:** only one owner; others **block** trying to enter (`Thread.State.BLOCKED`). **Unlock** on leaving the `synchronized` method or statement (normal or abrupt). **Wait set:** `wait` **releases** the monitor (all reentrant counts), parks in **WAITING** / **TIMED_WAITING**, then **re-acquires** before returning. That is **not** a second mutex API — it is the same object. `Lock` / `Condition` are **explicit** monitors. Private lock object: [[Why might you synchronize on a private mutex object in Java]]. Deadlock is **not** detected by the language.

The JVM does **not** expose an “owner id == 0 means free” field. You reason in **lock/unlock** actions, not in a published integer.

```java
synchronized void bump() { n++; }          // lock this
synchronized (lock) { lock.wait(); }       // lock lock; wait set of lock
static synchronized void m() { }           // lock TheClass.class
```

**Listing 1.** Three ways to enter a monitor. `wait` without owning it → `IllegalMonitorStateException`.

```d2
direction: down
obj: "object" {
  width: 100
  height: 36
  style.fill: "#fff8e1"
}
mon: "monitor lock" {
  width: 140
  height: 36
  style.fill: "#e8f5e9"
}
ws: "wait set" {
  width: 120
  height: 36
  style.fill: "#e3f2fd"
}
obj -> mon
obj -> ws
```

**Fig. 1.** One object, two structures. Mutex-only talk leaves out `wait`/`notify`.

> [!warning] Holding the monitor does not freeze fields
> Other threads can still read **unsynchronized** fields. The lock only excludes threads that **also** lock **that** object.

> [!warning] Monitor ≠ “the class’s mutex only”
> Instance methods lock **`this`**. Static methods lock the **`Class`**. `synchronized (x)` locks **`x`**.

> [!tip] Interview answer
> A monitor is the per-object lock plus wait set the JVM uses for synchronized and wait/notify. Only one thread owns the lock, and it can enter again because the lock is reentrant. Static synchronized uses the Class object’s monitor, not this.
