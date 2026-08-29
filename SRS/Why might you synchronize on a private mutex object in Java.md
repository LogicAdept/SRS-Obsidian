<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/SynchronizedKeyword #SRS

# Why might you synchronize on a private mutex object in Java?

> [!abstract] Short answer
> A `synchronized` **method** always takes the monitor of **`this`** (instance) or the **`Class`** object (static). A `synchronized (`*expr*`)` block takes the monitor of **whatever object** *expr* names — the **same** kind of lock. Callers who can name `this` or `Foo.class` can enter **that** monitor and **block** your methods, or interleave with a second lock order and **deadlock**. A **`private`** object exists **only** to be that monitor: outsiders cannot write `synchronized (yourMutex)`. Separate private locks also let **independent** fields move **concurrently**. Keyword: [[What is the synchronized keyword for in Java]]. Static target: [[On which object does a static synchronized method acquire a lock]]. Monitor: [[What is monitor in Java]].

## The lock is the object you name

Every object has a monitor. **One** thread owns it at a time; others **block**. Instance `synchronized` methods lock **`this`**; `static synchronized` methods lock the **`Class`**. A `synchronized` statement **evaluates** its expression (NPE if **null**), then locks **that** value. Those are the **same** monitors: `synchronized void bump() { count++; }` **is** `synchronized (this) { count++; }`. Unlock runs on **normal or abrupt** completion.

Anyone with a reference can use the **synchronized statement** on it. Mutual exclusion is **not** “fields of this object are sealed”; it is “threads that lock **this monitor** take turns.” Unsynchronized methods and field access **ignore** the lock. If your public API is `synchronized` methods, a client `synchronized (widget) { … }` **is** your lock. A **`private final Object mutex = new Object()`** is a monitor they **cannot** mention. Keep the field **`final`** so you do not accidentally lock **two** different objects over time. Nested same-object `synchronized` is **reentrant** (one thread may acquire again). Deadlock: [[How do you avoid deadlock in Java]]. Blocks and pitfalls: [[How would you explain synchronized blocks in Java and common pitfalls]].

**Fine-grained case.** If two fields are **never** used together, two private locks let an update of one **interleave** with the other. That is extra concurrency, not extra safety: you must be **sure** the split is real. `wait` / `notify` use the **wait set of the object whose monitor you hold** — wait on **`mutex`**, not `this`, if that is what you locked.

```java
final class GuardedCounter {
 private final Object mutex = new Object();
 private int n;

 void inc() {
 synchronized (mutex) {
 n++;
 }
 }

 int get() {
 synchronized (mutex) {
 return n;
 }
 }
}
```

**Listing 1.** One hidden monitor. `synchronized void inc()` would have locked **`this`**, which every holder of the counter can also lock.

```d2
direction: down
pub: "synchronized methods / synchronized(this)" {
 width: 280
 height: 40
 style.fill: "#fff8e1"
}
client: "client synchronized(instance)" {
 width: 240
 height: 36
 style.fill: "#ffebee"
}
priv: "synchronized(private mutex)" {
 width: 240
 height: 40
 style.fill: "#e8f5e9"
}
pub -> client: "same monitor"
priv -> client: "cannot name mutex" {
 style.stroke-dash: 3
}
```

**Fig. 1.** Privacy of the **reference** is privacy of the **monitor**.

> [!warning] Two locks are not “more synchronized”
> Split locks (`lock1` / `lock2`) only if the fields **never** compose. One thread can lock A then B while another locks B then A — the language **does not** detect deadlock. Mixing `synchronized` methods (`this`) with a private mutex means **two** protocols for one class; pick one per piece of state.

> [!warning] `wait` on the wrong object
> `wait` without owning that object’s monitor throws **`IllegalMonitorStateException`**. If you lock `mutex`, you `mutex.wait()`, not `this.wait()`. Locking `this` does **not** freeze unsynchronized getters.

> [!tip] Interview answer
> I synchronize on a private final object when I do not want callers to share my monitor. synchronized methods lock this or the Class, and anyone who has that reference can synchronized on it too. A private mutex is a lock they cannot name, and I can also use two of them when independent fields should not block each other. wait and notify have to use that same object.
