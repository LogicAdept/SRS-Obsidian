<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #Java/Concurrency #SRS

# What is double checked locking for a singleton?

> [!abstract] Short answer
> **Double-checked locking (DCL)** is a **lazy** singleton: read the instance **without** a lock; if **null**, **`synchronized`** and **check again** before `new`. The instance field **must be `volatile`**. The **volatile write** of the reference **happens-before** later **volatile reads**, so another thread that sees non-null also sees the **constructor’s writes**. Without `volatile`, a thread can observe a **non-null** reference to a **not-yet-initialized** object. Prefer **enum** or a **nested holder**. How-to: [[How do you implement a thread-safe singleton in Java]]. Two patterns: [[What are the two common singleton implementation patterns]]. Enum: [[How does an enum provide a Singleton]]. Volatile ref: [[What does volatile on a reference field guarantee for visibility]].

## Lock only on first creation

The outer `if (instance == null)` avoids the monitor on the **fast path**. The inner check stops two threads that both saw null from both constructing. A **local** `current = instance` reads the volatile **once** on the hit path.

**`synchronized (TheClass.class)`** is the usual lock (the `Class` monitor). That is **not** enough by itself: assignment of `instance` must be a **volatile** store. Field modifier: [[How would you explain the volatile field modifier in Java]]. Happens-before: [[How would you explain the happens-before guarantee in the Java Memory Model]].

This is **not** a Spring bean. A container “singleton” is **one instance per context**, not automatically thread-safe — [[Is a singleton Spring bean thread-safe]]. GoF vs Spring: [[How does a Spring singleton differ from the Gang of Four Singleton pattern]].

```java
final class DclSingleton {
    private static volatile DclSingleton instance;

    static DclSingleton getInstance() {
        DclSingleton current = instance;
        if (current == null) {
            synchronized (DclSingleton.class) {
                current = instance;
                if (current == null) {
                    instance = current = new DclSingleton();
                }
            }
        }
        return current;
    }

    private DclSingleton() {}
}
```

**Listing 1.** Local copy + **`volatile`**. Drop `volatile` and the pattern is unsafe.

```d2
direction: down
outer: "if instance == null" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
lock: "synchronized" {
  width: 140
  height: 36
  style.fill: "#e3f2fd"
}
inner: "if still null: new + volatile store" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
outer -> lock: "miss"
outer -> outer: "hit: return"
lock -> inner
```

**Fig. 1.** Uncontended reads skip the lock. Publication is the **volatile** assignment.

> [!warning] `volatile` is not optional decoration
> A plain `static` field plus DCL can publish a **partially constructed** instance. That is the classic DCL bug.

> [!warning] Prefer holder or enum
> DCL is easy to get wrong (missing `volatile`, locking `this` in a static method, reading the field twice). Class initialization already serializes **`new`**.

> [!tip] Interview answer
> Double-checked locking is lazy singleton with an unsynchronized null check and a second check inside synchronized. The instance field must be volatile so the constructor happens-before readers. I would still use an enum or a nested holder unless I have a reason to write DCL.
