<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch/TryWithResources #SRS

# What is a suppressed exception in try-with-resources?

> [!abstract] Short answer
> **A secondary failure attached to the exception that is actually thrown.** When the `try` body (or an earlier initializer) already has a primary exception and `close()` also throws, try-with-resources keeps the primary and calls `addSuppressed` for each close failure. `getSuppressed()` reads them; `printStackTrace` lists a `Suppressed:` heading. If the body completes normally, a `close` exception is **not** suppressed — it **is** the thrown result.

## Primary plus extras, not a cause chain

Cause (`getCause`) means “this throwable was constructed because of that one.” Suppression means “an independent sibling failure happened while delivering this one” — typically the body throw plus a `close` in the generated `finally` ([[What information does a Throwable carry]], [[How does the compiler translate try-with-resources]], [[What is try-with-resources]]).

If initialization and the body complete normally, there is no primary. Then `close()` throwing `V` **is** `V` leaving the statement ([[What happens if close throws after a try-with-resources body succeeds]]). If a later resource constructor throws, earlier resources still close; those close failures are suppressed on the **initializer** exception ([[What happens if a later try-with-resources constructor throws]]).

Hand-written `try`/`finally` that throws from both sides **discards** the first exception. TWR is the construct that keeps both ([[What is the difference between try-with-resources and try-finally when both throw]], [[What happens if try and finally both throw an exception]]).

`addSuppressed(this)` is illegal (`IllegalArgumentException`). `addSuppressed(null)` throws `NullPointerException`. Suppression can be disabled by a `Throwable` constructor; then `getSuppressed()` is empty.

```d2
direction: down
body: "body throws primary P" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
close: "close() throws S" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
out: "throw P\nP.addSuppressed(S)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
body -> close -> out
```

**Fig. 1.** `P` is what the caller `catch`es. `S` is on `P.getSuppressed()`.

```java
class Demo {
    static class R implements AutoCloseable {
        @Override
        public void close() {
            throw new RuntimeException("close");
        }
    }

    static void bodyAndClose() {
        try (R r = new R()) {
            throw new IllegalStateException("body");
        }
    }
}
```

**Listing 1.** The thrown object is `IllegalStateException`. `getSuppressed()[0]` is the `RuntimeException` from `close`. `getCause()` on the `IllegalStateException` is `null` unless you set a cause yourself ([[What is try-with-resources]]).

> [!warning] `getCause()` is not `getSuppressed()`
> Wrapping (`new RuntimeException(io)`) fills **cause**. A TWR `close` failure after a body throw fills **suppressed**. Looking only at `getCause()` misses close errors.

> [!warning] Successful body ⇒ `close` is primary
> People assume every `close` exception is “suppressed.” After a normal body, it is the statement’s exception. Several failing closes after a successful body: the **rightmost** close is primary; the others are suppressed on it.

> [!tip] Interview answer
> **A suppressed exception is a close (or other sibling) failure attached to the primary throwable with `addSuppressed`.** You read them via `getSuppressed()`, not `getCause()`. If the body succeeded, a `close` throw is not suppressed — it is what gets thrown.
