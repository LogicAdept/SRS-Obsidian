<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/SynchronizedKeyword #SRS

# On which object does a static synchronized method acquire a lock?

> [!abstract] Short answer
> On the **`Class` object for the method’s class** — the monitor of **`Foo.class`** for `static synchronized` in `Foo`, not **`this`** (there is no instance). Same monitor as **`synchronized (Foo.class)`**. An instance `synchronized` method uses **`this`**. `synchronized`: [[What is the synchronized keyword for in Java]]. Monitors: [[How would you explain monitor locks and intrinsic locks in Java]]. Instances vs static: [[Can you instances class static synchronized method]].

## Declaring class, not the caller

A `static synchronized` method is a **class method**. Before the body runs it acquires that **`Class`’s** monitor and releases it on return (normal or abrupt), like a `synchronized` statement. Two `static synchronized` methods on **the same class** exclude each other. A `static synchronized` method on **`Bar`** does **not** take **`Foo.class`**. A subclass that **inherits** `Foo.m` still locks **`Foo.class`**, because the method is **declared** in `Foo`.

Each **class loader** defines its own `Class` object: `Foo` loaded twice is **two** locks. Blocks: [[How would you explain synchronized blocks in Java and common pitfalls]].

```java
class Foo {
 static synchronized void m() { /* lock Foo.class */ }
 static void n() {
 synchronized (Foo.class) { /* same monitor as m */ }
 }
 synchronized void inst() { /* lock this */ }
}
```

**Listing 1.** `m` and `n` contend. `inst` does not take `Foo.class` unless it also locks it.

```d2
direction: down
st: "static synchronized" {
 width: 190
 height: 36
 style.fill: "#e3f2fd"
}
cl: "Foo.class monitor" {
 width: 180
 height: 40
 style.fill: "#e8f5e9"
}
ins: "instance synchronized" {
 width: 200
 height: 36
 style.fill: "#fff8e1"
}
th: "this" {
 width: 80
 height: 36
 style.fill: "#f3e5f5"
}
st -> cl
ins -> th
```

**Fig. 1.** Static → `Class` of the declaring class. Instance → the receiver.

> [!warning] Not a JVM-wide lock
> Only that **`Class`**. Other classes and other loaders proceed. Locking `Foo.class` from outside still shares the lock with `Foo`’s static synchronized methods.

> [!warning] `synchronized (this)` in a static method does not compile
> There is no `this`. Use `Foo.class` or a **private** `static final` lock object.

> [!tip] Interview answer
> A static synchronized method locks the Class object of the class that declared the method, the same monitor as synchronized on Foo.class. Instance synchronized methods lock this instead. Subclass callers still take the declaring class’s Class, not the subclass’s, unless the method is declared there.
