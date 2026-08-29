<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #Java/Concurrency #Java/JMM #SRS

# How do you implement a thread-safe singleton in Java?

> [!abstract] Short answer
> Rely on **class initialization** (one lock per class, runs once) or on an **enum constant**. Lazy: a **private nested holder** whose `static` instance is first touched in `getInstance`. Eager: `public static final` field. Double-checked locking works only if the instance field is **`volatile`**. `synchronized getInstance` is correct and slower. Enum uniqueness: [[How does an enum provide a Singleton]].

## Initialization lock, or `volatile`, or enum

A `static` field is created when its class is initialized. That procedure uses a per-class lock: one thread runs static initializers; others wait; when the class is fully initialized, later uses see those writes. So `public static final Singleton INSTANCE = new Singleton()` is a **safe eager** singleton. A **holder** class is initialized only when `getInstance` first reads `Holder.INSTANCE` (use of a non-constant static field), so the outer type can load without constructing the instance.

`public static synchronized Singleton getInstance()` publishes with monitor unlock/lock. Safe; every call takes the lock.

Double-checked locking: read `volatile` instance, lock only if null, write `volatile` after `new`. Without `volatile` another thread can see a non-null reference **before** constructor stores are visible — a data race. Local copy of the field is the usual inner-loop form. Detail: [[What is double checked locking for a singleton]].

An enum class has **no instances** except its constants (`new` is a compile-time error). `Enum.clone` throws; reflective construction is forbidden; serialization does not create duplicates. One constant is one object, created during enum class init. Class singletons still lose to reflection and default serialization unless you add extra machinery — [[What is the singleton serialization problem]].

```java
public enum EnumSingleton {
    INSTANCE;
}

public final class HolderSingleton {
    private HolderSingleton() {}

    private static final class Holder {
        static final HolderSingleton INSTANCE = new HolderSingleton();
    }

    public static HolderSingleton getInstance() {
        return Holder.INSTANCE;
    }
}
```

**Listing 1.** Enum constant (unique instance) and initialization-on-demand holder (lazy, still class-init safe). Keep the nested class **private**.

```java
public final class DclSingleton {
    private static volatile DclSingleton instance;

    private DclSingleton() {}

    public static DclSingleton getInstance() {
        DclSingleton s = instance;
        if (s == null) {
            synchronized (DclSingleton.class) {
                s = instance;
                if (s == null) {
                    instance = s = new DclSingleton();
                }
            }
        }
        return s;
    }
}
```

**Listing 2.** Double-checked locking. Drop `volatile` and publication is not safe.

```d2
direction: down
q: "One instance, concurrent getInstance" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
ok: "enum / holder / eager static\nclass-init lock" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
dcl: "DCL only with volatile" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
bad: "plain field, no lock" {
  width: 220
  height: 45
  style.fill: "#fce4ec"
}
q -> ok
q -> dcl
q -> bad
```

**Fig. 1.** Prefer enum or holder. DCL is optional and easy to get wrong.

> [!warning] A private constructor is not enum-unique
> Reflection and default serialization can still create a second instance of a class singleton.

> [!warning] A public nested `Holder` is part of the API
> Callers can load `Holder` directly. Make it `private`.

> [!tip] Interview answer
> I use an enum constant or a private holder class so the JVM’s class-init lock publishes the instance. If I write double-checked locking, the field is `volatile`. A synchronized getter is correct but locks on every call.
