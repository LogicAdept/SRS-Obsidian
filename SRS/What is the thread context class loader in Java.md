<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# What is the thread context class loader in Java

> [!abstract] Short answer
> A per-thread slot holding a `ClassLoader` reference, read via `Thread.getContextClassLoader()` and set via `setContextClassLoader`. It lets code running in a thread load classes through a loader chosen by the thread's creator — not through the loader that defined that code. If never set, a thread inherits it from its parent; the main thread's context loader is the application loader; `null` means the system loader.

## Why parent delegation needs this bridge

Parent-first lookup only reaches upward: a loader can see its ancestors' classes, never its descendants'. Service utilities live exactly on the wrong side of that wall — `java.util.ServiceLoader` is defined in `java.base` by the bootstrap loader, and `java.sql.DriverManager` sits on the platform loader since Java 9 — so their own defining loaders cannot see application classes at all. The context loader is the inversion: instead of asking "what loader defined me", the framework asks "what loader does the current thread carry". The javadoc states the intent: the context `ClassLoader` may be set by the creator of the thread for use by code running in this thread when loading classes and resources; if not set, the default is to inherit the context class loader from the parent thread, and the context `ClassLoader` of the primordial thread is typically set to the class loader used to load the application. A `null` return means the system class loader, or failing that, the bootstrap class loader.

```d2
direction: right
boot: "bootstrap\ndefines ServiceLoader" {
  width: 170
  height: 60
  style.fill: "#e3f2fd"
}
app: "application loader\ndefines user drivers" {
  width: 190
  height: 60
  style.fill: "#e8f5e9"
}
fw: "framework code\n(parent-first: cannot reach app)" {
  width: 220
  height: 60
  style.fill: "#ffebee"
}
slot: "thread context\nclass loader slot" {
  width: 170
  height: 60
  style.fill: "#fff3e0"
}
boot -> app: "cannot see (parent-first)"
fw -> slot: "reads"
slot -> app: "can name"
```

**Fig. 1.** The context loader is the only downward edge: framework code reads the thread's slot and reaches classes its own loader could never load.

## Who reads the slot

`ServiceLoader.load(service)` creates a new service loader for the given service type, using the current thread's context class loader — the two-arg overload lets you pass the loader explicitly instead. JDBC driver discovery works through the same service mechanism ([[How do you register a JDBC driver]]), and servlet containers set a per-webapp context loader on their request threads so container code resolves webapp classes. Nothing reads the slot implicitly: a plain `loadClass` call or one-arg `Class.forName` still uses the loader they were written to use ([[What does Class.forName do and what are its overloads]]).

```java
ClassLoader ctx = Thread.currentThread().getContextClassLoader();

// these two are equivalent:
ServiceLoader<Driver> a = ServiceLoader.load(Driver.class);
ServiceLoader<Driver> b = ServiceLoader.load(Driver.class, ctx);

// framework side: pin the loader you need and restore it after
ClassLoader saved = Thread.currentThread().getContextClassLoader();
Thread.currentThread().setContextClassLoader(MyPlugin.class.getClassLoader());
try {
    ServiceLoader<Driver> found = ServiceLoader.load(Driver.class);
} finally {
    Thread.currentThread().setContextClassLoader(saved);
}
```

**Listing 1.** The default reads the slot; the restore pattern keeps a pinned loader from leaking into the next task on the thread.

> [!warning] It is a convention, not a mechanism
> The context loader has no built-in effect: it is an ordinary field that libraries must read explicitly, and some libraries never do. Code that ignores the slot and calls `Class.forName(name)` resolves through its own defining loader — from a bootstrap- or platform-defined class that lookup cannot see your application classes at all.

> [!warning] Per-thread mutable state, kept alive by pools
> Thread pools reuse threads, and each thread keeps whatever loader was last set — often a webapp loader from a previous deployment. The `ServiceLoader` documentation warns that applications sharing one VM may have different thread context class loaders, that a lookup may locate a provider only visible via one application's context loader and unsuitable for another, and that memory leaks can also arise. Always restore the previous value in `finally`.

> [!tip] Interview answer
> **It is a per-thread `ClassLoader` slot that inverts parent delegation: bootstrap- or platform-defined framework code reads the current thread's slot to load classes from the application. Default is inheritance from the creating thread, the main thread carries the application loader, and `null` means the system loader. `ServiceLoader` and JDBC discovery read it — but it is a convention, so set-and-restore it around framework calls or thread pools leak loaders.**

