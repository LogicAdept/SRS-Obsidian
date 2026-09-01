<!--
reps: 0
priority: 0
-->
#Java/Language/Object/Finalize #Java/JVM/GarbageCollector #Java/Legacy #SRS

# What is `finalize`, and why was it needed?

> [!abstract] Short answer
> **`finalize` is `Object`’s `protected` method that the GC *may* run once before it reuses an object’s storage** — a hook for releasing **native/OS resources the collector will not free** (files, sockets, native memory). Java **heap** memory does **not** need it. It was a **safety net**, not a C++ destructor: **timing is unspecified**, it **may never run**, and it is **`@Deprecated(since = "9", forRemoval = true)`**. New code uses **try-with-resources** or **`Cleaner`**.

## What it is

The finalizer of an instance is the `finalize` that would run for its class. `Object`’s method **does nothing**. A subclass override was meant to dispose of **system resources** before the object is discarded ([[How would you explain the finalize method in Java and why it is discouraged]]). The VM **does not** promise **when**, **which thread**, or **that it happens at all**. An exception from `finalize` is **ignored**; the method is **never automatically invoked twice** ([[What happens to finalization if finalize runs slowly or throws an exception]]).

It can **resurrect** the object (store `this` in a reachable place). After that, the collector must again decide the object is unreachable — **without** a second `finalize`.

## Why it existed

The GC reclaims **Java memory** when an object is no longer needed. That is **insufficient** when the instance holds an **OS resource** (file descriptor, native block). If `close()` is never called, the information needed to release that resource is lost when the object disappears — a **leak**. Early Java had no try-with-resources; `try/finally` around `close` was easy to get wrong.

Finalization tried to piggy-back on GC: if a resource-bearing object becomes unreachable, run `finalize` so it can still `close`. That is the only honest “why it is needed.” It is **not** there to free the Java heap, return control to the OS, or act as a destructor when a variable goes out of scope.

```d2
direction: down
heap: "GC reclaims Java memory" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
os: "file / socket / native memory\nstill held by the OS" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
hook: "finalize was the safety net\n(unreliable — now deprecated)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
os -> hook
```

**Fig. 1.** Heap collection is automatic. Non-memory resources were the reason `finalize` existed.

```java
@Override
protected void finalize() throws Throwable {
    try {
        // historical: close a native handle if the caller forgot
    } finally {
        super.finalize();
    }
}
```

**Listing 1.** Conceptual: the old pattern. Do not add this to new types. `super.finalize()` is not inserted for you.

Today that net is **withdrawn**: deprecation for **removal**, `--finalization=disabled`, **`AutoCloseable`** + try-with-resources for lexical lifetime, **`Cleaner`** when you cannot expose `close` ([[How would you explain the AutoCloseable interface in Java]], [[What is try-with-resources]]).

> [!warning] Not a C++ destructor
> Leaving a block does not run `finalize`. The GC may not run before exit. Treating `finalize` as “memory cleanup” fights the collector and still leaks files.

> [!warning] Resurrection is allowed, not useful
> `finalize` may publish `this` again. It will **not** run a second time, so you cannot use that trick as a lifecycle. It is one of the reasons the mechanism is a security and GC hazard.

> [!tip] Interview answer
> **`finalize` is a protected Object hook the GC might call to release native resources the heap collector cannot free.** It was a leak safety net from Java 1.0, not a destructor and not for Java memory. It is deprecated for removal; use try-with-resources or Cleaner, and never rely on it running.
