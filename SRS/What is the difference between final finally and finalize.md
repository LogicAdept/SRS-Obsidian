<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #Java/JVM/GarbageCollector #Java/Language/Object/Finalize #Java/Language/Modifiers/Final #SRS

# What is the difference between `final` `finally` and `finalize`?

> [!abstract] Short answer
> **They are unrelated except for the letters.** `final` is a modifier (no subclass, no override, no reassignment). `finally` is the cleanup clause of a `try` statement. `finalize()` is `Object`’s deprecated finalizer — the GC **might** call it, or never. For resources use try-with-resources, not `finalize`.

## Three different language features

**`final`** — a modifier. A `final` class has no subclasses. A `final` method cannot be overridden or hidden. A `final` field or local variable cannot be reassigned after it is assigned. Method parameters may be `final` too.

**`finally`** — a clause of `try`. It runs after `try` and any matching `catch`, including after `return` or `throw`, **if that `try` was entered** and the process still completes the statement. It is not a literal always ([[How would you explain the finally block in Java]], [[Is a finally block always executed in Java]]). Prefer try-with-resources for `AutoCloseable` ([[What is try-with-resources]], [[How would you explain the AutoCloseable interface in Java]]).

**`finalize()`** — `protected void finalize() throws Throwable` on `Object`. `@Deprecated(since="9", forRemoval=true)`. Subclasses should **remove** it. Use `Cleaner` / `PhantomReference`, or `close()` + `AutoCloseable`. The collector may never call it (finalization disabled/removed, or an indefinite delay). `System.gc()` does not promise a call. An exception from `finalize` is **ignored**. It is not `finally`.

```d2
direction: right
fin: "final\nmodifier" {
  width: 240
  height: 70
}
fly: "finally\ntry clause" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
ize: "finalize()\ndeprecated" {
  width: 260
  height: 70
  style.fill: "#fff8e1"
}
```

**Fig. 1.** Same root letters; three features. Do not treat them as a family.

```java
class Demo {
    final int n = 1;

    static int value() {
        try {
            return 1;
        } finally {
            System.out.println("cleanup");
        }
    }
}
```

**Listing 1.** `final` on the field. `finally` still runs before `value()` returns `1`. There is no `finalize` here on purpose.

> [!warning] `finally` is not “always”
> If the `try` never started, or the VM exits (`System.exit`), `finally` does not run. Interview shorthand overstates it.

> [!warning] Do not override `finalize` for cleanup
> It is deprecated for removal. It may never run. `System.gc()` in a demo does not make it reliable. Use try-with-resources.

> [!tip] Interview answer
> **`final` stops subclassing, overriding, or reassignment.** **`finally` is `try` cleanup.** **`finalize()` is a deprecated GC hook that might never run** — use try-with-resources instead. They only share a name stem.
