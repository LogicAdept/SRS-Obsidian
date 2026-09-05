<!--
reps: 0
priority: 0
-->
#Java/Language/Object/Finalize #Java/JVM/GarbageCollector #ProgrammingLanguages/CSharp #SRS

# What is non-deterministic finalization?

> [!abstract] Short answer
> **Cleanup that runs only after the GC decides the object is unreachable — at an unspecified time, on an unspecified thread, maybe never soon enough.** That is `Object.finalize()` in Java and a C# finalizer (`~Type`). Prompt resource release is `try`-with-resources / `IDisposable`, not the finalizer.

## “Sometime after it is garbage,” not a destructor

**Java.** `finalize` is called by the garbage collector if finalization is still enabled, once the VM has determined there is no remaining way for a non-finalizer thread to reach the object. The language does **not** say how soon that call happens — only that it is before the storage is reused — and does **not** say which thread runs it (that thread holds no user-visible locks). The JavaDoc is explicit: the collector **might call `finalize` only after an indefinite delay**. As of Java SE 21, an implementation may disable finalization entirely, in which case `finalize` is **never** called. The method is deprecated for removal since JDK 9; prefer `Cleaner` / `PhantomReference` or `AutoCloseable` ([[How would you explain the finalize method in Java and why it is discouraged]], [[How does the garbage collector decide an object can be collected]]).

**C#.** A finalizer (`~Car`) is invoked automatically; you cannot call it. **The programmer has no control over when** — the GC decides eligibility, then may run `Finalize` and reclaim the object. `GC.Collect` is not a reliable schedule. You also cannot rely on all finalizers at process exit: .NET Framework tries; **.NET 5+ does not** run finalizers on termination. `IDisposable.Dispose` / `using` is the deterministic path ([[What is the difference between IDisposable and a finalizer]]).

That delay is the whole meaning of **non-deterministic finalization**: reachability is a GC fact; the cleanup callback is queued and run later (Java: finalizer-reachable, then a later pass can reclaim). A circular group can become finalizable together, in any order, even concurrently ([[How does garbage collection treat cyclic references between live objects]]). A finalizer that runs late keeps native handles; one that never runs (disabled Java finalization, .NET exit) leaks them.

```d2
direction: down
unreach: "Object unreachable\nfrom application roots" {
  width: 280
  height: 55
  style.fill: "#fff8e1"
}
queue: "Finalizer queue\n(time and thread unspecified)" {
  width: 300
  height: 55
  style.fill: "#ffebee"
}
run: "finalize / ~Type runs\nthen memory may be reused" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
unreach -> queue
queue -> run: "indefinite delay; maybe never"
```

**Fig. 1.** Becoming garbage is not the same instant as running the finalizer. Deterministic cleanup is a `close`/`Dispose` you call.

```java
@Deprecated(since = "9", forRemoval = true)
protected void finalize() throws Throwable {
    try {
        // might run much later, on another thread, or never
    } finally {
        super.finalize();
    }
}
```

**Listing 1.** Conceptual Java snippet (not a full compilation unit). The API is deprecated for removal; do not use it for sockets or files. `super.finalize()` is not chained automatically.

```csharp
class FileHolder
{
    ~FileHolder() { /* GC timing; not for prompt close */ }
}
```

**Listing 2.** C#: one finalizer, no parameters, not called from your code. Put unmanaged cleanup in `Dispose` and `GC.SuppressFinalize(this)`.

> [!warning] This cue is not the `final` keyword
> `final` on a class, method, or field is a compile-time modifier. Finalization is a GC callback. Mixing them is a common exam trap.

> [!warning] Do not wait for the finalizer to close a resource
> Files, sockets, and DB connections need `try`-with-resources or `using`. Finalizers can revive the object (Java), run after other managed objects are already dead (C#), throw and be swallowed (Java), or never run at shutdown.

> [!tip] Interview answer
> **Non-deterministic finalization means the GC runs `finalize` / `~Type` at an unspecified later time — you do not get C++ destructor semantics.** Java does not specify the delay or the thread; the call can be delayed indefinitely or skipped if finalization is off. In C# you cannot call the finalizer, and .NET 5+ will not run them on process exit. Use `AutoCloseable` or `IDisposable` when the resource must be released now.
