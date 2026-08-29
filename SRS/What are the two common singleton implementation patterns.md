<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #Java/Concurrency #SRS

# What are the two common singleton implementation patterns?

> [!abstract] Short answer
> In Java interviews the two patterns are **eager** and **lazy**. **Eager:** a **`public static final`** instance created when the class is **initialized** (the JVM’s **per-class init lock** runs statics **once**). **Lazy:** the instance is created on **first use** — safest with a **private nested holder** (its class initializes on first `getInstance`) or an **enum constant** (the language’s unique instance; `==` is valid). Double-checked locking is a third, easy-to-get-wrong lazy form and needs **`volatile`**. Safe how-to: [[How do you implement a thread-safe singleton in Java]]. Enum: [[How does an enum provide a Singleton]]. DCL: [[What is double checked locking for a singleton]]. Pattern: [[How would you explain the Singleton design pattern]].

## Class-init lock vs first-touch class

**Eager** is simple and thread-safe without extra `synchronized` on `getInstance`. The class is initialized before first use of that field; other threads wait on the init lock. Cost: the instance exists even if never asked for (after the class loads).

**Lazy holder:** `getInstance()` touches `Holder.INSTANCE`, so `Holder` initializes then. Same init-lock guarantee, delayed. **Enum:** one constant, no extra instances from clone/reflection/deserialization in the usual model — [[What is the singleton serialization problem]]. **`synchronized getInstance`** is correct lazy and serializes every call. Unsynchronized `if (instance == null) instance = new …` is **not** a pattern, it is a race. [[How do you implement a thread-safe singleton in Java]]. Record: [[How do you implement Singleton with a Java record]]. Spring’s “singleton” is a **container scope**, not GoF — [[How does a Spring singleton differ from the Gang of Four Singleton pattern]].

```java
final class Eager {
 static final Eager INSTANCE = new Eager();
 private Eager() {}
}

final class LazyHolder {
 private LazyHolder() {}
 private static class Holder { static final LazyHolder INSTANCE = new LazyHolder(); }
 static LazyHolder getInstance() { return Holder.INSTANCE; }
}

enum EnumSingleton { INSTANCE }
```

**Listing 1.** Eager field, lazy holder, enum constant. Pick two of these three in an interview; all three are initialization-safe.

```d2
direction: down
e: "eager static field" {
 width: 180
 height: 36
 style.fill: "#fff8e1"
}
l: "lazy holder / enum" {
 width: 200
 height: 36
 style.fill: "#e8f5e9"
}
e -> l: "same init lock\ndifferent when"
```

**Fig. 1.** Both rely on **class initialization**, not on a home-grown unsynchronized field.

> [!warning] Lazy without a happens-before is not a second pattern
> A plain `static Foo instance` assigned in `getInstance` can publish a **partially constructed** object or create **two**. That is a bug, not “lazy singleton.”

> [!warning] DCL is not one of the two basics
> It works only if the instance field is **`volatile`**. Prefer holder or enum unless you must lazy-init a class that already has other statics.

> [!tip] Interview answer
> The two I name are eager static final and lazy, usually a nested holder or an enum constant. Both are safe because class initialization is synchronized by the JVM. I do not use unsynchronized lazy assignment, and I only mention double-checked locking if they ask, with volatile.
