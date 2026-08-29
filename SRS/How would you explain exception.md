<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS

# How would you explain exception?

> [!abstract] Short answer
> **An exception is an object that stops the normal flow and transfers control to a matching `catch`.** Every one is a `Throwable`. `Exception` is for problems a program may recover from; `Error` is for serious VM/system failure. If nothing catches it, the thread’s uncaught handler runs.

## A thrown object, not a return code

When the language’s rules are violated (for example an array index out of range), or when code executes `throw`, the VM **throws** a `Throwable`. Control leaves the current expressions and calls until a `catch` whose type matches that object (or a superclass). That is **non-local** transfer — not “return `-1` and hope the caller checks” ([[What information does a Throwable carry]], [[How should you throw and handle exceptions in Java]], [[How do you handle exceptions in Java applications]]).

`Throwable` has two direct subclasses:

- **`Exception`** — ordinary programs may wish to recover. `RuntimeException` (NPE, `ArithmeticException` from integer `/ 0`) sits under `Exception` and is **unchecked**. Other `Exception`s (for example `IOException`) are **checked**: catch or `throws` ([[What is RuntimeException]], [[What is the difference between Throwable and Exception]]).
- **`Error`** — ordinary programs are not expected to recover (heap/stack collapse, linkage). `catch (Exception e)` skips them on purpose ([[What is java.lang.Error]], [[How would you explain errors that surface at the JVM level]], [[Can you catch Throwable]]).

Monitors are still unlocked as `synchronized` methods/statements complete abruptly. If no handler matches, the uncaught exception handler runs and that thread ends.

```d2
direction: down
th: "Throwable" {
  width: 220
  height: 40
}
ex: "Exception" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
err: "Error" {
  width: 220
  height: 40
  style.fill: "#ffebee"
}
rte: "RuntimeException" {
  width: 240
  height: 40
}
th -> ex
th -> err
ex -> rte
```

**Fig. 1.** One root; two branches. Integer `/ 0` is `ArithmeticException` (`RuntimeException`), not `Error`.

```java
class Demo {
    static int at(int[] a, int i) {
        return a[i];
    }
}
```

**Listing 1.** A bad `i` throws `ArrayIndexOutOfBoundsException` — an exception object, a `RuntimeException`, not an `Error`. The call does not return a sentinel index.

> [!warning] “Exception” in speech vs `java.lang.Exception`
> Interviewers often say “exception” for any `Throwable`. `Error` is an exception in that sense but **not** a subclass of `Exception`.

> [!warning] Integer `/ 0` is not an `Error`
> It is `ArithmeticException`. Out of memory is `OutOfMemoryError`. Mixing those is the usual hierarchy mix-up.

> [!tip] Interview answer
> **An exception is a `Throwable` that aborts normal flow and searches up the call stack for a matching `catch`.** `Exception` is for recoverable problems; `Error` is for VM-level failure. Checked exceptions must be caught or declared; `RuntimeException` and `Error` need not.
