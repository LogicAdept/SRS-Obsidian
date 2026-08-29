<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# How would you explain try-catch-finally?

> [!abstract] Short answer
> **`try` is the guarded work, `catch` is a typed handler, `finally` is optional cleanup that runs after that `try` and after any matching `catch`.** At most one `catch` of that statement runs. Control does not go back into the `try`. If `finally` itself returns or throws, that new completion **replaces** whatever was pending.

## Three keywords, one `try` statement

A `try` statement groups a block that may complete abruptly. Each `catch` names a type; the **first** assignment-compatible clause runs, then that statement’s `finally` if present ([[How would you explain Java exception handling try catch and propagation]], [[Does control return to the try block after a catch handles an exception]]). You may have several `catch` clauses and **at most one** `finally` ([[Can a try statement have more than one finally block]]). Nothing may sit between `try`, `catch`, and `finally` ([[Can you place statements between try catch and finally]]).

`catch` is optional when `finally` is present; `finally` is optional when at least one `catch` (or a resource list) is present ([[Can you try-finally without catch]]).

`finally` runs on the way out — success, throw, `return` — then the original completion continues unless `finally` itself returns or throws ([[How would you explain the finally block in Java]], [[What happens if finally returns after try throws an exception]], [[What happens if try and finally both throw an exception]], [[What happens if finally mutates a local after try returns it]]). After a **normal** `finally`, a pending `return` value that was already evaluated still stands.

`finally` does not run if that `try` never started or the process is already gone ([[Is a finally block always executed in Java]]). For closeable resources, try-with-resources is the usual shape; a failing `close` is suppressed on the body exception instead of replacing it ([[What is try-with-resources]]).

```d2
direction: down
try: "try block" {
  width: 240
  height: 50
}
catch: "first matching catch" {
  width: 280
  height: 50
}
fin: "optional finally" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
try -> catch -> fin
```

**Fig. 1.** Handler first, cleanup second. The rest of the `try` is never resumed.

```java
class Demo {
    static void run() {
        try {
            throw new IllegalStateException("try");
        } catch (RuntimeException e) {
            System.out.println("caught");
        } finally {
            System.out.println("cleanup");
        }
    }
}
```

**Listing 1.** Prints `caught` then `cleanup`. The throw never resumes inside the `try`.

> [!warning] “`finally` always runs” is the interview shorthand
> It runs if that `try` was entered and the JVM still completes the statement. `System.exit`, a crash, or never reaching the `try` skip it.

> [!warning] `return` in `finally` is a bug, not a trick
> It compiles. It also discards a pending throw or the `try`’s return value. Let `finally` complete normally.

> [!tip] Interview answer
> **`try` guards the work, `catch` handles a named type, `finally` cleans up after both.** Only one `catch` of that `try` runs. `finally` still runs if an exception was thrown or not — unless the `try` never started or the process is already dead — and a `return`/`throw` inside `finally` replaces the pending result.
