<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #SRS

# How would you explain the Singleton design pattern

> [!abstract] Short answer
> Singleton is a creational pattern that guarantees **one instance of a class** and provides a **global access point** to it: a private constructor plus a static `getInstance` method that creates the instance on the first call and returns the cached one afterwards.

## The mechanism

The pattern solves two problems at once, which is already a Single Responsibility Principle violation. It ensures a single instance — the usual reason is a shared resource such as a configuration or a connection pool, and a regular constructor cannot do this because a constructor call must return a new object by design. It also provides a global access point — like a global variable, but protected: no other code can overwrite the cached instance. The implementation always has the same two steps: hide the constructor so nobody can call `new`, and expose a static creation method that stores the object in a static field and hands back the same reference on every call.

```java
class Config {
    private static Config instance;
    private Config() { /* load settings */ }
    static Config getInstance() {
        if (instance == null) {          // naive: not thread-safe
            instance = new Config();
        }
        return instance;
    }
}
```

**Listing 1.** The canonical shape: private constructor, static field, lazy `getInstance`. This exact version is not thread-safe — see below.

## Where the trade-offs are

The lazy version above breaks under threads: two threads can both see `instance == null` and each construct an instance. Java offers several fixes — a `synchronized` method, double-checked locking with a `volatile` field, the holder idiom, or an enum — and the vault covers them in [[How do you implement a thread-safe singleton in Java]], [[What is double checked locking for a singleton]], [[What are the two common singleton implementation patterns]], and [[How does an enum provide a Singleton]]. Beyond thread safety, the pattern makes client code hard to unit-test, because the private constructor and the static access point block mocking, and it can mask bad design when components quietly depend on the shared object through it.

> [!warning] Two Singleton myths
> First: "Singleton guarantees one instance per JVM" — only if nothing bypasses it; reflection, serialization, and multiple classloaders can each produce extra instances. Second: "Spring beans are GoF Singletons" — a Spring singleton is a container scope, one bean per container, not a class restriction; the difference is spelled out in [[How does a Spring singleton differ from the Gang of Four Singleton pattern]].

> [!tip] Interview answer
> Singleton ensures a class has exactly one instance and gives a global access point to it. Mechanically: private constructor plus a static creation method that lazily caches the instance. The cost: you must handle thread safety explicitly, and the pattern mixes lifecycle management with business logic, hurts testability, and is often labeled an anti-pattern — see [[Why is the singleton pattern often labeled an anti pattern]].
