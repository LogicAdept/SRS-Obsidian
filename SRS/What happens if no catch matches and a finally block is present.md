<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# What happens if no catch matches and a finally block is present?

> [!abstract] Short answer
> **`finally` still runs, then the exception keeps propagating.** After a `finally` that completes normally, the original throw continues. If nothing further up the stack catches it, that thread is terminated after its uncaught-exception handler (typically a stack trace). If `finally` itself `return`s or `throw`s, that abrupt completion **replaces** the pending exception.

## `finally` during propagation, then the throw resumes

A `catch` is selected only if the thrown object is assignment-compatible with that clause. If none of this `try`’s clauses match, no sibling `catch` runs ([[How many catch blocks execute for one thrown exception]], [[Does catch Exception also catch RuntimeException]]). The `finally` block of **this** `try` still executes while the exception is propagating, even if an **enclosing** `try` will catch it later ([[How would you explain the finally block in Java]], [[How would you explain try-catch-finally]]).

If that `finally` completes **normally**, the `try` statement completes abruptly because of the **same** thrown value `V`. Search for a handler continues outward.

If no handler exists anywhere, the thread is terminated. Before that, remaining `finally` clauses run, then the thread’s uncaught-exception handler (or the thread group’s `uncaughtException`). A typical main thread prints the exception and a backtrace.

If `finally` completes **abruptly** (`return` or `throw`), that new reason is propagated and `V` is discarded ([[What happens if finally returns after try throws an exception]], [[What happens if try and finally both throw an exception]]).

```d2
direction: down
throw: "try throws V\nno catch matches" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
fin: "finally runs" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
prop: "V continues outward" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
swap: "finally return/throw\nV discarded" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
throw -> fin
fin -> prop
fin -> swap
```

**Fig. 1.** Unmatched `catch` does not skip `finally`. Only an abrupt `finally` replaces `V`.

```java
class Demo {
    static void unmatched() {
        try {
            throw new NullPointerException("try");
        } catch (IllegalStateException e) {
            System.out.println("not this");
        } finally {
            System.out.println("finally");
        }
    }
}
```

**Listing 1.** Prints `finally`, then `NullPointerException` propagates. `catch (Exception e)` would have matched; this `IllegalStateException` clause does not ([[Does catch Exception also catch Error]]). `System.exit` or JVM death can still skip `finally` entirely ([[Is a finally block always executed in Java]]).

> [!warning] An outer `try` does not skip this `finally`
> Propagation visits every enclosing `finally` on the way out, then may match a `catch` on an outer `try`. Cleanup of the inner statement still happens.

> [!warning] `return` in this `finally` hides the unmatched throw
> After a normal `finally`, `V` is still pending. A `return` in `finally` makes the method complete normally and the caller never sees `V`.

> [!tip] Interview answer
> **`finally` still executes. If it finishes normally, the original exception continues; if nothing catches it, the thread’s uncaught handler runs.** If `finally` returns or throws, that replaces the pending exception. `finally` also runs when an outer `try` will catch it later.
