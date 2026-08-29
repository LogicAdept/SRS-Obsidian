<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch/TryWithResources #SRS

# What happens if `close` throws after a try-with-resources body succeeds?

> [!abstract] Short answer
> **That `close()` exception is thrown out of the statement.** With no primary exception from the body, cleanup failure is **not** suppressed. A successful body can still fail on close. That matters for types whose `close` flushes (for example `BufferedWriter`): a failed final flush is a real exception the caller must handle.

## `close` is the primary when the body completed normally

Resources close after the `try` block, in reverse initialization order, skipping nulls ([[What is try-with-resources]], [[How does the compiler translate try-with-resources]], [[What happens if a try-with-resources resource is null]]).

If initialization and the body complete normally, and automatic close then throws `V`, the try-with-resources statement completes abruptly because of `V`. The generated translation calls `r.close()` in the `finally` **without** `addSuppressed` when `#primaryExc` is still null.

Suppression is only for a **later** close (or close after an earlier failure) when a primary already exists: body throw, a previous initializer, or an earlier close in reverse order ([[What is a suppressed exception in try-with-resources]], [[What happens if a later try-with-resources constructor throws]], [[What is the difference between try-with-resources and try-finally when both throw]]).

If **several** resources fail to close after a successful body, the **rightmost** failing close (first in LIFO) is primary; the others are suppressed on it.

`BufferedWriter.close` closes the stream, **flushing it first**. A flush I/O error on the way out is therefore this case: the writes in the body may have looked fine, then `close` throws `IOException`.

```d2
direction: down
body: "try body completes normally" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
close: "close() throws V" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
out: "V is thrown (not suppressed)" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
body -> close -> out
```

**Fig. 1.** No body exception ⇒ `close` failure is the statement’s exception.

```java
class Demo {
    static class R implements AutoCloseable {
        @Override
        public void close() {
            throw new RuntimeException("close failed");
        }
    }

    static void afterSuccess() {
        try (R r = new R()) {
            // body succeeds
        }
    }
}
```

**Listing 1.** `afterSuccess` throws `RuntimeException` from `close`. Nothing is on `getSuppressed()`. An extended `catch` around the try-with-resources can still catch this `V` ([[What is try-with-resources]]).

> [!warning] Do not treat “body succeeded” as “the file is durable”
> For buffered writers, the last bytes may still be in the buffer until `close`/`flush`. A thrown `IOException` from `close` means the caller’s `try` did **not** complete normally.

> [!warning] Suppression needs a primary first
> If the body throws and then `close` throws, the body exception is primary and `close` is suppressed. If only `close` throws, there is nothing to suppress onto — `close` **is** the primary.

> [!tip] Interview answer
> **If the try body succeeds and `close` throws, that close exception leaves the try-with-resources — it is not suppressed.** Suppression is for extra failures after a primary already exists. A failed flush inside `BufferedWriter.close` is this situation.
