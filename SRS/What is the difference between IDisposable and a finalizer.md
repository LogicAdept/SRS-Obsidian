<!--
reps: 0
priority: 0
-->
#ProgrammingLanguages/CSharp #Java/JVM/GarbageCollector #Java/Language/Object/Finalize #SRS

# What is the difference between IDisposable and a finalizer?

> [!abstract] Short answer
> **`IDisposable.Dispose` is a method you (or `using`) call now to release unmanaged resources. A finalizer (`~Type` / `Object.Finalize`) is a last-chance callback the GC may run later if nobody called `Dispose`.** They are not two names for the same destructor. `Dispose` does not free the managed object’s memory — the collector still does that. A type that only owns other managed disposables needs `IDisposable`, not a finalizer.

## Deterministic call versus GC callback

The CLR garbage collector reclaims **managed** memory when an object is unused. It does **not** know about window handles, file handles, or other native resources, and you cannot predict when a collection will run. `IDisposable` is the contract for **explicit** cleanup: one parameterless `Dispose` that the **consumer** runs when the instance is finished. C# `using`, Visual Basic `Using`, F# `use`, or a `try`/`finally` all end in that call.

A **finalizer** is the runtime’s backup. You never call it. The collector may invoke it **before** reclaiming the object if `Dispose` never ran. That timing is non-deterministic ([[What is non-deterministic finalization]]). From .NET 5 onward, finalizers are **not** run on process exit, so “the destructor will close the file when the app shuts down” is false.

The **dispose pattern** shares one cleanup method and splits the two callers with a `bool`:

| Path | Who runs it | When | What it may touch |
| --- | --- | --- | --- |
| `Dispose()` | Your code / `using` | Immediately, deterministically | Managed `IDisposable` children **and** unmanaged resources, then `GC.SuppressFinalize(this)` |
| Finalizer `~T` | GC | Unspecified later (maybe not at exit) | **Unmanaged only** — other managed objects may already be gone |

`disposing == true` means the call is deterministic (`Dispose`). `disposing == false` means it came from the finalizer. On that path, only free native resources. Finalization order among objects is nondeterministic, so touching another managed object from `~T` is unsafe.

`GC.SuppressFinalize(this)` after a successful `Dispose(true)` takes the instance off the finalization queue. If the type has no finalizer, the call is a no-op. `Dispose` must be **idempotent**: a second call does nothing and must not throw.

A finalizer is required only when the type **directly** holds unmanaged resources. If it only owns managed `IDisposable` members, implement `IDisposable` and cascade `Dispose` — **do not** write `~T`. The recommended native wrapper is `SafeHandle`, which already has a finalizer so your type usually should not.

Java’s pairing is the same idea under different names: `AutoCloseable` / try-with-resources versus `finalize` ([[How would you explain the finalize method in Java and why it is discouraged]], [[What is finalize why it needed]]).

```d2
direction: down
need: "Instance holds a native handle\nor owns IDisposable children" {
  width: 320
  height: 50
  style.fill: "#fff8e1"
}
split: "Who releases the native resource?" {
  width: 300
  height: 40
}
disp: "IDisposable.Dispose / using\nnow, on your thread" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
fin: "~Type / Object.Finalize\nGC schedule, unspecified thread" {
  width: 300
  height: 55
  style.fill: "#ffebee"
}
mem: "GC still reclaims the managed object" {
  width: 300
  height: 45
  style.fill: "#e3f2fd"
}
need -> split
split -> disp: "preferred"
split -> fin: "only if Dispose was skipped"
disp -> mem: "SuppressFinalize"
fin -> mem: "if it runs at all"
```

**Fig. 1.** `Dispose` is prompt cleanup you invoke. A finalizer is a delayed GC callback. Neither is a C++ destructor; heap memory stays the collector’s job.

```csharp
public class ResourceHolder : IDisposable
{
    private bool _disposed;
    // IntPtr or similar only if you truly own unmanaged memory.
    // Prefer SafeHandle and then you often need no ~ResourceHolder at all.

    public void Dispose()
    {
        Dispose(disposing: true);
        GC.SuppressFinalize(this);
    }

    ~ResourceHolder() => Dispose(disposing: false);

    protected virtual void Dispose(bool disposing)
    {
        if (_disposed) return;
        if (disposing)
        {
            // Dispose managed IDisposable fields here — never from the finalizer.
        }
        // Release unmanaged resources on both paths.
        _disposed = true;
    }
}
```

**Listing 1.** Conceptual C# (not a full compilation unit). `Dispose()` is the public, non-virtual entry. The finalizer only calls `Dispose(false)`. Types that wrap `SafeHandle` typically omit `~ResourceHolder`.

> [!warning] `Dispose` is not `free` of the object
> Calling `Dispose` releases **resources the collector cannot see**. The instance remains a managed object until it is unreachable and the GC reclaims it. Skipping `using` and hoping `~T` closes a file, socket, or lock is the usual production leak.

> [!warning] Do not put a finalizer on every `IDisposable`
> A finalizer is an advanced last resort for **direct** unmanaged ownership. From the finalizer you must not use other managed objects. Prefer `SafeHandle`. In C# you write `~Type`, not an `override` of `Object.Finalize`.

> [!tip] Interview answer
> **`IDisposable` is deterministic cleanup you call; a finalizer is non-deterministic cleanup the GC might run if you forget.** Use `using` (or `try`/`finally`) so `Dispose` runs now, then `SuppressFinalize` so the collector does not run `~Type` as well. The finalizer path must not touch other managed objects, because they may already have been finalized. Prefer `SafeHandle` over writing your own finalizer, and never treat either mechanism as freeing the object’s heap memory.
