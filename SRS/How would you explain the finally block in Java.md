<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# How would you explain the `finally` block in Java?

> [!abstract] Short answer
> **`finally` is the cleanup clause of a `try` statement: it runs after the `try` block and after any matching `catch`, however those blocks finish — normal return, `throw`, `break`, or `continue`.** If `finally` itself returns or throws, that new completion **replaces** whatever was pending. It is not a guarantee that the process is still alive.

## Runs on the way out — unless the try never started

A `try` may pair with `catch`, `finally`, both, or (for try-with-resources) a resource list. `catch` is optional when `finally` is present ([[Can you try-finally without catch]], [[Can a try statement have more than one finally block]]). You cannot put statements between `try`, `catch`, and `finally` ([[Can you place statements between try catch and finally]]).

The `try` block runs first. Then, if a `catch` matches, that handler runs. Then `finally` runs. After a normal `finally`, the statement completes as the `try`/`catch` did: if they threw and nothing caught it, the exception still propagates ([[What happens if no catch matches and a finally block is present]]).

If `finally` completes abruptly — `return`, `throw`, `break`, `continue` — that reason **wins**. A pending exception from `try` or `catch` is discarded ([[What happens if try and finally both throw an exception]], [[What happens if finally returns after try throws an exception]]). Try-with-resources is different: a failing `close` is **suppressed** on the body exception, not a replacement ([[What is the difference between try-with-resources and try-finally when both throw]]).

`finally` does not run if that `try` was never entered. It also does not run if the JVM or process dies first (`System.exit` / `Runtime.exit` never complete the `try`; remaining threads on program exit do not run `finally`; a crash or `halt` is the same idea) ([[Is a finally block always executed in Java]]).

```d2
direction: down
try: "try / matching catch" {
  width: 280
  height: 50
}
fin: "finally" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
out: "leave the try statement" {
  width: 280
  height: 50
}
try -> fin -> out
```

**Fig. 1.** `finally` is on the exit path of the `try` statement, not a second `catch`.

```java
class Demo {
    static void run() {
        try {
            throw new IllegalStateException("try");
        } finally {
            System.out.println("cleanup");
        }
    }
}
```

**Listing 1.** No `catch`: `finally` still prints, then the exception continues to the caller.

> [!warning] `return` or `throw` in `finally` hides the original outcome
> Interviewers treat this as a bug. Let `finally` complete normally so the `try`/`catch` result is the one that leaves.

> [!warning] “Always executes” is not “the process cannot die”
> If the `try` never started, or the VM exits without completing that statement, `finally` does not run.

> [!tip] Interview answer
> **`finally` is guaranteed cleanup for a `try` that actually started: it runs after `try` and any matching `catch`, on both success and throw.** If `finally` returns or throws, that replaces the pending result. It will not run if the process is already gone, and it is not a substitute for try-with-resources on closeable resources.
