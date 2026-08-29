<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS

# What is synchronization?

> [!abstract] Short answer
> **Synchronization** coordinates threads that **share** state: **mutual exclusion** (one owner of a lock) plus **visibility** (an **unlock happens-before** a later **lock** of the **same** monitor). In Java the language construct is **`synchronized`**: every object has a **monitor**. It does **not** “make threads run in parallel” — threads already **can**; sync **serializes** the **critical section**. Broader tools: **`volatile`**, **`Lock`**, atomics, j.u.c. Keyword: [[What is the synchronized keyword for in Java]]. `synchronized`: [[What is the synchronized keyword for in Java]]. Monitor: [[What is monitor in Java]], [[How would you explain monitor locks and intrinsic locks in Java]]. `Lock` too: [[How would you explain synchronization with synchronized and locks in Java]]. Static: [[On which object does a static synchronized method acquire a lock]]. Mechanisms list: [[What synchronization mechanisms exist in Java]].

## Exclusion and happens-before, not “more parallelism”

**`synchronized` method:** instance → lock **`this`**; **`static`** → the declaring class’s **`Class`**. **`synchronized (expr)`** locks that object. Ownership is **reentrant**. Waiters for the monitor are **`Thread.State.BLOCKED`**. Leaving the method/block (normal or abrupt) **unlocks**. **`wait`/`notify`** use the **same** object’s wait set and require that you **already hold** the lock.

The lock only excludes threads that **also** lock **that** object. Other threads can still read **unsynchronized** fields. Different objects → **different** monitors. **`Lock.lock()`/`unlock()`** is the explicit cousin (`finally` required).

```java
synchronized void bump() { n++; }              // lock this
synchronized (lock) { lock.wait(); }           // lock lock
static synchronized void m() { }               // lock TheClass.class
```

**Listing 1.** Three monitor entries. `i++` is still two steps **inside** the lock — the lock makes the **compound update** look atomic to **other lockers of the same object**.

```d2
direction: down
t1: "thread A" {
  width: 100
  height: 36
  style.fill: "#e8f5e9"
}
mon: "object monitor" {
  width: 140
  height: 36
  style.fill: "#fff8e1"
}
t2: "thread B BLOCKED" {
  width: 150
  height: 36
  style.fill: "#ffebee"
}
t1 -> mon: "owns"
t2 -> mon: "waits"
```

**Fig. 1.** One owner. The other waits on **that** lock, not on “the object’s fields.”

> [!warning] Synchronization is not parallelism
> Starting threads is concurrency. **`synchronized` restricts** who may run a section at once so shared writes are **ordered and visible**.

> [!warning] Holding the monitor does not freeze fields
> Unsynchronized readers still race. Every access path must use the **same** lock (or another happens-before edge).

> [!tip] Interview answer
> Synchronization means coordinating threads that share data, mainly with a lock so only one thread runs a critical section and its writes become visible to the next owner. In Java that is the per-object monitor behind synchronized, or an explicit Lock. It does not make code parallel; it serializes the parts that must not race.
