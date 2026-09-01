<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #Patterns/AntiPatterns #Java/OOP #SRS

# Why is the singleton pattern often labeled an anti pattern?

> [!abstract] Short answer
> GoF Singleton **looks** like a clean “one instance” API (`private` constructor + `getInstance()`), then **hides a global**. Callers hard-wire the type; you cannot **substitute** a stub without extra seams. Lifetime is the **process / class loader**, not a use case. In Java, **serialization**, **reflection**, and **another class loader** can still produce a second instance. An antipattern is a path that **looks like a solution** and then hurts — Singleton is that in many apps, not in every context. Pattern: [[How would you explain the Singleton design pattern]]. Spring’s “singleton”: [[How does a Spring singleton differ from the Gang of Four Singleton pattern]]. Enum form: [[How does an enum provide a Singleton]].

## Global access is the product, and the problem

**What the pattern sells.** One object, a well-known access point, `private` constructors so `new` from outside fails ([[How would you explain private constructors and common patterns that use them in Java]]). That is convenient for a logger or a “the” configuration.

**Why people call it an antipattern.** An antipattern is not “any bad idea.” It is something that **looks like a good solution** and then locks you in. `Clock.getInstance().now()` in a hundred classes **is** a global. Tests cannot swap a frozen clock unless you add `loadInstance` / a mutable holder — and even then static init may have already constructed the real service.

**Coupling and lifetime.** The dependency is **invisible** in constructors. The instance lives as long as the class is initialized. You cannot have two configurations in one JVM without tricks. Thread-safety of `getInstance()` is a separate mess ([[How do you implement a thread-safe singleton in Java]]; [[What is double checked locking for a singleton]]).

**Java extras that break “exactly one.”** `readObject` can allocate another ([[What is the singleton serialization problem]]). `setAccessible` can call the private constructor. A second class loader loads a second `Clock` class. **Spring singleton** means one bean **per container**, not GoF-per-JVM.

**Way out.** Pass the collaborator (constructor injection). Keep a registry only if it is **substitutable**. Prefer an **enum** constant when you truly want a JVM-unique, serialization-safe instance.

```d2
direction: down
gof: "getInstance() in every caller" {
  width: 280
  height: 40
  style.fill: "#ffebee"
}
inj: "constructor parameter" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Hard-wired Singleton vs an injected collaborator you can stub.

```java
class Clock {
    private static final Clock INSTANCE = new Clock();

    private Clock() {}

    static Clock getInstance() {
        return INSTANCE;
    }

    long now() {
        return System.currentTimeMillis();
    }
}

class Stamp {
    static long mark() {
        return Clock.getInstance().now();
    }
}
```

**Listing 1.** `Stamp` cannot take a fake `Clock`. That global `getInstance()` is why the pattern is labeled an antipattern in tests and in large codebases.

> [!warning] Context decides, not a slogan
> The same shape can be a pattern (one hardware port, one process-wide cache you accept) and an antipattern (domain services, “the” database). “Always evil” is as wrong as “always use Singleton.”

> [!warning] Spring singleton is not this debate
> A Spring singleton bean is still injected. The anti-pattern is **GoF global access**, not “the container creates one instance.”

> [!warning] Making `getInstance` lazy does not fix design
> Double-checked locking and enums fix **construction races**, not hidden dependencies.

> [!tip] Interview answer
> Singleton is labeled an antipattern because it is a global: callers depend on a concrete `getInstance()`, tests cannot substitute easily, and the lifetime is the JVM. Java can still create extra instances via serialization, reflection, or another class loader. Inject the dependency instead; use a true Singleton only when one process-wide instance is the actual requirement.
