<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch/TryWithResources #SRS

# What is the difference between try-with-resources and try-finally when both throw?

> [!abstract] Short answer
> **Handwritten `try`/`finally`: if the body and `close()` in `finally` both throw, the `finally` exception wins and the body exception is discarded.** **Try-with-resources reverses that:** the body exception is primary; `close()` exceptions are **suppressed** on it (`addSuppressed`). That is the main exception-handling reason to prefer TWR over a manual `finally` close.

## Who stays primary

In a `try`/`finally`, if the `try` (or `catch`) completes abruptly with reason `R` and `finally` then completes abruptly with reason `S`, the statement completes for **`S`**. `R` is forgotten. A `close()` in `finally` that throws therefore **hides** the body’s exception ([[What happens if try and finally both throw an exception]], [[What happens if finally returns after try throws an exception]]).

Try-with-resources records the body throw as primary. Automatic `close()` that then throws is attached with `addSuppressed`, not substituted. `getSuppressed()` lists those close failures ([[What is a suppressed exception in try-with-resources]], [[How does the compiler translate try-with-resources]]).

If the TWR body **succeeds**, a `close()` exception is **not** suppressed: it propagates as the primary, same as a failing `finally` close with no prior throw ([[What happens if close throws after a try-with-resources body succeeds]]).

An explicit `catch` or `finally` on a try-with-resources statement runs **after** resources have been closed (or close has been attempted).

```d2
direction: down
both: "body throws and close() throws" {
  width: 320
  height: 50
}
manual: "try/finally: close exception wins\n(body discarded)" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}
twr: "TWR: body is primary\nclose is suppressed" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
both -> manual
both -> twr
```

**Fig. 1.** Same two throws; different survivor.

```java
class Boom implements AutoCloseable {
    private final RuntimeException onClose;
    Boom(RuntimeException onClose) { this.onClose = onClose; }
    void fail() { throw new IllegalStateException("body"); }
    @Override public void close() { throw onClose; }
}

class Demo {
    static void manual() {
        Boom r = new Boom(new IllegalArgumentException("close"));
        try {
            r.fail();
        } finally {
            r.close();
        }
    }

    static void twr() {
        try (Boom r = new Boom(new IllegalArgumentException("close"))) {
            r.fail();
        }
    }
}
```

**Listing 1.** `manual` propagates `IllegalArgumentException` (“close”); the body’s `IllegalStateException` is lost. `twr` propagates `IllegalStateException` (“body”) with the close exception on `getSuppressed()`. If `fail()` were omitted, both styles would propagate the close exception as primary.

> [!warning] Manual `finally { close(); }` loses the first exception
> That is the interview contrast. Logging in `finally` or calling `addSuppressed` yourself can preserve it; TWR does that automatically.

> [!warning] Suppression only applies when the body already failed
> A successful TWR body plus a throwing `close()` is **not** a suppressed pair. You see one exception, the close failure ([[What happens if close throws after a try-with-resources body succeeds]]).

> [!tip] Interview answer
> **In `try`/`finally`, a throwing `close()` replaces the body’s exception.** **In try-with-resources, the body exception stays primary and `close()` is suppressed on it.** If the body succeeded, a close failure propagates normally in both styles.
