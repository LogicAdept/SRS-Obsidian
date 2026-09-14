<!--
reps: 0
priority: 0
-->
#Java/JMM/HappensBefore #Java/OOP/Initialization #SRS

# What does class initialization guarantee about static field visibility in Java

> [!abstract] Short answer
> **A class or interface is initialized immediately before its first active use (JLS 12.4.1), and the static initializers run exactly once under a per-class initialization lock (JLS 12.4.2).** Every thread that subsequently uses the class waits until initialization completes, so it observes the fully initialized static state — no volatile, no explicit locking needed.

The trigger list is closed: a class `T` is initialized immediately before the first time an instance of `T` is created, a static method declared by `T` is invoked, a static field declared by `T` is assigned, or a static field declared by `T` that is not a constant variable is used. Certain reflective calls trigger it too, and a superclass is initialized first. Nothing else initializes a class — which is why a mere type reference or `T.class` lookup stays lazy.

The visibility guarantee is mechanical, not magic: JLS 12.4.2 assigns each class a unique initialization lock and, after running "the class variable initializers and static initializers of the class ... in textual order, as though they were a single block", marks the class fully initialized, notifies waiting threads, and releases the lock. Any other thread that reaches an active use of the same class must block on that lock first, so every write performed by the static initializer is visible to it. This is the same visibility role an unlock-then-lock pair plays for monitors — but provided by the class initialization protocol itself rather than the synchronizes-with list in JLS 17.4.4. That is the honest framing: interviews lump it in with the happens-before rules, and functionally it behaves like one, yet the edge lives in the initialization procedure of chapter 12, not chapter 17.

```d2
direction: right
t1: "T1: first active use\n(new, static call, static field)" {
  width: 280
  height: 88
  style.fill: "#e3f2fd"
}
lock: "JVM holds initialization lock LC\nruns static initializers once" {
  width: 290
  height: 88
  style.fill: "#fff3e0"
}
t2: "T2: reaches a use of the class\nblocks until fully initialized" {
  width: 290
  height: 88
  style.fill: "#e3f2fd"
}
done: "class marked fully initialized\nnotify waiting threads" {
  width: 290
  height: 88
  style.fill: "#e8f5e9"
}
t1 -> lock: "triggers init"
lock -> done: "initializers complete"
t2 -> done: "waits on LC, then proceeds\nsees all static writes"
```

**Fig. 2.** The initialization lock serializes the first use: the second thread cannot observe a half-initialized static state, because its use cannot complete before the class is labeled fully initialized.

```java
class ConfigHolder {
    static final Config CFG = Config.load();  // runs once under LC

    static Config get() {          // first call triggers initialization
        return CFG;                // all threads see the loaded config
    }
}

class Config {
    static Config load() {
        return new Config("prod"); // heavy work, done at most once
    }
}
```

**Listing 1.** The initialization-on-demand holder idiom: thread safety comes entirely from the class initialization protocol, which is why it is the recommended lazy-singleton form without volatile or an explicit lock.

> [!warning] Circular static initialization can observe defaults
> Transitivity of this guarantee only covers uses that come *after* initialization. If a static initializer calls into another class whose initializer calls back, the recursive request finds the class "in progress" and proceeds without waiting — the callback can read static fields that still hold default values ([[What is the default value happens-before rule in the Java Memory Model]]). Keep initializers free of cycles; the JVM will not detect them for you. Also mind the constant-variable carve-out: reads of `static final` compile-time constants do not trigger initialization at all, and their values are folded in at compile time.

> [!tip] Connect the two initialization stories
> Instance-level default writes and class-level static writes are two sides of the same visibility story: the default-value rule covers the fields of every object ([[What is the default value happens-before rule in the Java Memory Model]]), and the initialization lock covers the statics of every class. A broken static initializer throws `ExceptionInInitializerError` and marks the class erroneous — later uses fail with `NoClassDefFoundError` ([[Can a static initializer throw a checked exception]]). For the language-level mechanics of `static` itself see [[What does the static keyword mean in Java]]; for the parallel object-construction guarantee see [[Why do final fields guarantee visibility for properly constructed objects]].
