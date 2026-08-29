<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# Can you try-finally without catch?

> [!abstract] Short answer
> **Yes.** `try { ... } finally { ... }` is a complete `try` statement. `catch` is optional. The `finally` block still runs if the `try` block throws; the exception then **propagates** unless `finally` itself completes abruptly.

## Cleanup without a handler

A non-resource `try` must have at least one `catch` **or** a `finally`. Omitting `catch` is legal. That form is for **cleanup that must run** (unlock, restore state) while still letting the exception leave the statement ([[Can a try block exist without a catch in Java]], [[Can a try block exist without catch and finally]]).

If the `try` block throws and there is no matching `catch` (including **no** `catch` at all), the `finally` block runs, then the original throw continues — unless `finally` completes abruptly, in which case that new reason **replaces** the original ([[What happens if no catch matches and a finally block is present]], [[What happens if try and finally both throw an exception]], [[What happens if finally returns after try throws an exception]]).

There is only one `finally` per `try`. Nothing may sit between `try` and `finally` ([[Can a try statement have more than one finally block]], [[Can you place statements between try catch and finally]]). For `AutoCloseable` resources, try-with-resources often replaces a manual `try`/`finally` close ([[How does the compiler translate try-with-resources]]).

```d2
direction: down
tryb: "try { work }" {
  width: 240
  height: 50
}
fin: "finally { cleanup }" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
prop: "exception still propagates" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
tryb -> fin -> prop
```

**Fig. 1.** No `catch` means no handler. `finally` still runs; the throw is not swallowed.

```java
class Demo {
    static int run(boolean fail) {
        try {
            if (fail) {
                throw new IllegalStateException();
            }
            return 1;
        } finally {
            // always runs; IllegalStateException still leaves the method
        }
    }
}
```

**Listing 1.** Legal `try`/`finally` with no `catch`. `run(true)` throws `IllegalStateException` after `finally`. Adding `catch` would be a **handler**, not a requirement for the `try` to compile.

> [!warning] Missing `catch` is not “pointless”
> It is the usual shape when you must clean up **and** still fail. Adding a `catch` that swallows the exception is worse than omitting `catch`.

> [!warning] `finally` can hide the original throw
> If `finally` throws or `return`s, the `try` block’s exception is discarded. That is independent of whether a `catch` exists.

> [!tip] Interview answer
> **Yes — `try`/`finally` without `catch` is legal.** Use it for cleanup when you still want the exception to propagate. `finally` always runs; it does not catch. A bare `try` with no `finally` and no resources does not compile.
