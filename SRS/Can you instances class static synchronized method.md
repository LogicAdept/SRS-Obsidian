<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/SynchronizedKeyword #SRS

# Can you instances class static synchronized method?

> [!abstract] Short answer
> The dump’s question is: **can you `new` instances of a class while one of its `static synchronized` methods is running?** **Yes, in the usual case.** That method locks the **`Class` object**, not any instance. Allocating and constructing an object does not take that monitor — unless the constructor (or an instance initializer) **also** waits on the same `Class` lock.

## Two different monitors

A `static synchronized` method acquires the monitor of the `Class` object for that class — the same lock as `synchronized (Foo.class)`. An instance `synchronized` method acquires the monitor of `this`. Those are not the same object, so one thread can sit in `Foo.staticSync()` while another thread runs `new Foo()` and even instance methods that synchronize on the **new** instance. Which object is locked: [[On which object does a static synchronized method acquire a lock]]. You cannot assign the `Class` lock to a chosen thread: [[Can Java code manually control which thread holds a monitor]].

`new` allocates the object, default-initializes instance fields, then runs constructors. None of that steps requires holding `Foo.class` once the class is already initialized (and a `static` method of `Foo` is running, so it is). The dump’s “static fields are not instance fields” is the wrong reason: the split is **which monitor**, not “fields don’t belong to instances.”

```java
public final class StaticSyncAndNew {
    static synchronized void holdClassLock() {
        try {
            Thread.sleep(Long.MAX_VALUE);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    StaticSyncAndNew() {}

    public static void main(String[] args) throws InterruptedException {
        Thread holder = new Thread(StaticSyncAndNew::holdClassLock);
        holder.setDaemon(true);
        holder.start();
        Thread.sleep(50);
        new StaticSyncAndNew(); // does not wait for holdClassLock
    }
}
```

**Listing 1.** `new` proceeds while another thread owns `StaticSyncAndNew.class`. It **would** block if the constructor called `holdClassLock()` or `synchronized (StaticSyncAndNew.class)`.

```d2
direction: down
ss: "static synchronized\nlocks Class object" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
nw: "new Foo()\nno Class lock (usual ctor)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
block: "ctor takes Foo.class\nthen new waits" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}
ss -> nw: "different monitors"
ss -> block: "same monitor"
```

**Fig. 1.** Instance `synchronized` methods on the new object still run: they lock `this`, not `Foo.class`. Two `static synchronized` methods of `Foo` **cannot** run together.

> [!warning] `new` is not a pass if the constructor needs the class lock
> A constructor that calls a `static synchronized` method, or `synchronized (Foo.class)`, waits like any other locker of that monitor. A `synchronized` constructor (legal Java) still locks **`this`** (the instance under construction), not the `Class`.

> [!warning] Do not treat `static synchronized` as “the class is frozen”
> Other threads may still read and write **instance** state, and even **static** fields, if they do not take `Foo.class`. Mutual exclusion is only among threads that lock that same monitor.

> [!tip] Interview answer
> Yes, you can usually construct new instances while a `static synchronized` method runs, because it locks the `Class` object and `new` does not. It blocks only if construction itself tries to take that same class lock. Static and instance `synchronized` methods are different monitors.
