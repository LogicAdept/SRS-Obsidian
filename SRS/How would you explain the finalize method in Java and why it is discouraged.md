<!--
reps: 0
priority: 0
-->
#Java/Language/Object/Finalize #Java/JVM/GarbageCollector #Java/Legacy #SRS

# How would you explain the `finalize` method in Java and why it is discouraged?

> [!abstract] Short answer
> **`Object.finalize` is a `protected` hook the GC *may* run before reclaiming an instance** — not a destructor. Timing, thread, and order are **unspecified**; it can run **late, concurrently, or never**. It is **`@Deprecated(since = "9", forRemoval = true)`** because finalization is **insecure, slow, and unreliable**. Prefer **`try`-with-resources / `AutoCloseable`**, or **`Cleaner`** for long-lived non-memory resources. Do not write new finalizers.

## What `finalize` actually does

The finalizer of an object is the `finalize` definition that would run for its class. `Object`’s method **does nothing**. A subclass may override it to release native/OS resources that the GC will not free when it reclaims the Java object ([[How would you explain key methods declared on java.lang.Object]]).

If finalization is **enabled**, the JVM invokes that finalizer **before** the storage is reused — but the language **does not say how soon**, **which thread**, or **in which order**. Several finalizer threads may run; a whole unreachable graph can finalize **concurrently**. The calling thread **holds no user-visible locks**. An **uncaught exception is ignored** and finalization of that object **stops** ([[What happens to finalization if finalize runs slowly or throws an exception]]).

If finalization is **disabled or removed**, the GC **never** calls `finalize`. Java SE 21 allows implementations to disable it. A JVM launched with **`--finalization=disabled`** (since JDK 18) runs **no** finalizers, including JDK ones. Enabled remains the default on current JDKs; the method is **not** gone in 17 or 21.

`finalize` is **never automatically invoked more than once**. It **may resurrect** the object (store `this` in a static). After that, the object is only discarded when the VM again finds it unreachable — **without** a second finalizer call.

Unlike constructors, finalizers **do not chain**. If you override `finalize`, you must call **`super.finalize()`** yourself (typically in `finally`) unless you intend to skip the superclass cleanup.

```java
@Override
protected void finalize() throws Throwable {
    try {
        // subclass cleanup
    } finally {
        super.finalize();
    }
}
```

**Listing 1.** Conceptual: the chaining pattern from the `Object.finalize` API note. New code should not add this method.

```d2
direction: down
dead: "object unreachable" {
  width: 200
  height: 55
  style.fill: "#fff3e0"
}
maybe: "GC might schedule finalize\nlate / concurrent / never" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
twr: "try-with-resources\nclose() on the way out" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
dead -> maybe
```

**Fig. 1.** Finalization is a GC-scheduled maybe. Deterministic `close` is not.

## Why it is discouraged

Finalization was a safety net for resource leaks. The platform now treats it as a **flawed** mechanism:

- **Latency** — unbounded delay; **no guarantee** the finalizer ever runs. File descriptors and native memory can exhaust while objects sit on the heap waiting.
- **Resurrection and security** — a finalizer can do anything, including publishing a **partially initialized** instance (subclass constructor threw after `Object()` finished). A subclass can add a finalizer even when the superclass has none.
- **Always on** — a non-trivial `finalize` makes **every** instance finalization-eligible; you cannot cancel it after `close()`.
- **Threads** — unspecified threads turn a “single-threaded” class into concurrent code (deadlocks, races). Finalizers of unrelated libraries **share** those threads and can starve each other.
- **GC cost** — extra work at allocation and before/after finalization even when `close` already ran.

So the API is terminally deprecated: **do not override `finalize` for new types**. For a resource used in one block, implement **`AutoCloseable`** and use **try-with-resources** ([[What is try-with-resources]], [[How would you explain the AutoCloseable interface in Java]]). For a long-lived object that cannot expose `close`, register a **`Cleaner`** action that **must not** refer to the registered instance (static nested `Runnable` / `State`; a capturing lambda keeps the object alive). Cleaning still waits on the GC, so it is **not** a substitute when release must be timely; prefer explicit `close`. Call `Cleanable.clean()` from `close()` so the happy path does not wait for phantom reachability.

> [!warning] `finalize` is not C++ destruction
> Leaving scope does not run it. The GC might not run. `--finalization=disabled` or a future JDK **silently skips** it. An exception inside `finalize` is **swallowed**. Treating it as “the OS will get the file back” is how descriptor leaks show up in production.

> [!warning] `super.finalize()` is not inserted for you
> Skipping it drops superclass cleanup. Skipping `try/finally` drops it if your body throws — and that throw is then **ignored**. The compiler will not save you the way it inserts `super()` in constructors.

> [!tip] Interview answer
> **`finalize` is a protected Object method the GC might call before reclaiming an object; timing, thread, and order are unspecified, and it can resurrect the instance or never run.** It has been deprecated since Java 9 and is marked for removal because it is a security, performance, and reliability hazard. Use try-with-resources or a Cleaner; do not write new finalizers, and do not call it a destructor.
