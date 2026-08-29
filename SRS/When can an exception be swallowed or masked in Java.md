<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# When can an exception be swallowed or masked in Java?

> [!abstract] Short answer
> **Swallowed when a `catch` ignores it, or when `finally` `return`s and discards a pending throw.** **Masked** when `finally` (or a later `throw`) replaces that pending exception with a different one. try-with-resources is different: a body exception stays primary and a failed `close` is **suppressed**, not lost.

## Ignore, replace, or attach as suppressed

A `catch` that does nothing — or only continues as if the operation succeeded — **swallows** the exception. Callers see a normal path. Catching `InterruptedException` and not restoring interrupt status is the same idea for cancellation ([[How would you explain InterruptedException in Java threads]]).

If `try` or `catch` throws and then `finally` completes with `return`, the `try` statement completes **normally**. The throw is gone; there is no stack trace for that failure ([[What happens if finally returns after try throws an exception]], [[How would you explain the finally block in Java]]).

If `finally` **throws** instead, that new completion **replaces** the original. The first exception is not attached automatically. That is **masking** ([[What happens if try and finally both throw an exception]]).

try-with-resources keeps the exception from the `try` block when `close` also fails: the close exception is recorded with `addSuppressed`. A handwritten `try`/`finally` that throws from cleanup does not do that unless you call `addSuppressed` yourself ([[What is the difference between try-with-resources and try-finally when both throw]], [[What is try-with-resources]]).

```d2
direction: down
pending: "pending throw from try/catch" {
  width: 300
  height: 50
}
path: "what happens next?" {
  width: 320
  height: 50
}
empty: "empty catch / return in finally" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
mask: "throw in finally" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
sup: "TWR close fails" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
pending -> path
path -> empty: "swallowed"
path -> mask: "masked"
path -> sup: "primary + suppressed"
```

**Fig. 1.** Same pending failure, three different outcomes.

```java
class Demo {
    static void swallow() {
        try {
            throw new IllegalStateException("lost");
        } catch (IllegalStateException ignored) {
        }
    }

    static int mask() {
        try {
            throw new IllegalStateException("lost");
        } finally {
            return 0;
        }
    }
}
```

**Listing 1.** Empty `catch` swallows. `return` in `finally` also swallows. A `throw` in `finally` would mask with a different exception.

> [!warning] `return` in `finally` is a silent swallow
> `javac -Xlint:finally` warns. The caller never sees the original failure.

> [!warning] try/`finally` masking is not TWR
> Two throws in try-with-resources keep both (primary plus suppressed). A `throw` in `finally` drops the first unless you attach it.

> [!tip] Interview answer
> **An exception is swallowed if `catch` ignores it or `finally` returns after a throw.** It is masked if `finally` throws something else and the first exception is dropped. try-with-resources keeps the body exception and lists close failures as suppressed.
