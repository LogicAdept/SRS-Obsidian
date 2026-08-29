<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# What happens if `try` and `finally` both throw an exception?

> [!abstract] Short answer
> **The exception from `finally` is the one that leaves the `try` statement.** The pending exception from `try` (or from `catch`) is **discarded**. Hand-written `finally` does **not** attach the original as a suppressed exception — that bookkeeping is try-with-resources. A `return` in `finally` is another way to drop the pending failure: the method then completes normally.

## Abrupt `finally` replaces reason `R`

`finally` still runs when `try` or `catch` completes abruptly ([[Is a finally block always executed in Java]], [[How would you explain the finally block in Java]], [[What happens if no catch matches and a finally block is present]]). If `finally` then throws `S`, the `try` statement completes abruptly because of **`S`**. The earlier reason `R` (the throw from `try` or `catch`) is forgotten.

The same **finally-wins** rule applies when `catch` throws one exception and `finally` throws another. Debugging then shows only the cleanup error; the original failure is gone unless you saved it yourself ([[How would you explain try-catch-finally]]).

Try-with-resources is the contrast: if the body (or an initializer) already has a primary exception, `close()` failures are `addSuppressed` on that primary ([[What is the difference between try-with-resources and try-finally when both throw]], [[What is a suppressed exception in try-with-resources]], [[How does the compiler translate try-with-resources]]). A plain `finally { throw … }` does none of that.

```d2
direction: down
try: "try (or catch) throws R" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
fin: "finally throws S" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
out: "caller sees S\nR is discarded" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
try -> fin -> out
```

**Fig. 1.** Manual `finally` does not keep `R` on `getSuppressed()`.

```java
class Demo {
    static void both() {
        try {
            throw new IllegalStateException("try");
        } finally {
            throw new RuntimeException("finally");
        }
    }

    static void catchThenFinally() {
        try {
            throw new IllegalStateException("try");
        } catch (IllegalStateException e) {
            throw new IllegalArgumentException("catch");
        } finally {
            throw new RuntimeException("finally");
        }
    }
}
```

**Listing 1.** Both methods throw `RuntimeException("finally")`. The try/catch exceptions are not suppressed on it. `return` in `finally` would instead complete the method normally and hide `R` entirely ([[What happens if finally returns after try throws an exception]]).

> [!warning] Interviews treat `throw` from `finally` as a bug
> The stack trace names the cleanup failure. The original cause is lost unless you stored it (`addSuppressed` / `initCause`) before throwing from `finally`. Prefer not to throw from `finally` at all.

> [!warning] Do not confuse this with try-with-resources
> After a successful TWR **body**, a `close` throw **is** the primary (nothing to suppress onto). After a failed body, `close` is suppressed. Ordinary `try`/`finally` never auto-suppresses.

> [!tip] Interview answer
> **If `try` and `finally` both throw, the caller sees the `finally` exception; the `try` exception is discarded.** The same if `catch` and `finally` both throw. Try-with-resources can suppress the later failure on the primary; a handwritten `finally` does not. `return` in `finally` swallows the throw completely.
