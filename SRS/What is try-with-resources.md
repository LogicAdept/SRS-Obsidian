<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch/TryWithResources #Java/IO #SRS

# What is try-with-resources?

> [!abstract] Short answer
> **It is a `try` statement that takes `AutoCloseable` resources in parentheses and closes them automatically when the block ends.** Added in Java 7. You do not write that `close()`. If the body throws and `close` also throws, the close exception is **suppressed** on the primary one (`getSuppressed()`). Optional `catch`/`finally` on the same statement run **after** automatic close.

## `try (` resources `)` then the block

Resources initialize left to right and close **right to left**. Only a non-`null` resource is closed ([[What happens if a try-with-resources resource is null]]). The type must be a subtype of `java.lang.AutoCloseable` (`java.io.Closeable` is the I/O subtype) ([[How would you explain the AutoCloseable interface in Java]], [[What forms of try catch and try with resources exist in Java]]). If a later initializer throws, earlier resources still close ([[What happens if a later try-with-resources constructor throws]]).

The compiler translates this into nested `try`/`finally` that call `close()` ([[How does the compiler translate try-with-resources]]). A **basic** form has no `catch` or `finally` of yours — that is a legal `try` without those clauses ([[Can a try block exist without catch and finally]]). An **extended** form may still have them; they run **after** the generated close.

If the body throws and `close` also throws, the close exception is **suppressed** on the primary one — unlike a handwritten `finally` that `throw`s and replaces the body exception ([[What is a suppressed exception in try-with-resources]], [[What is the difference between try-with-resources and try-finally when both throw]]). If the body succeeds and `close` throws, that close exception **is** the result ([[What happens if close throws after a try-with-resources body succeeds]]).

Since Java 9 you may name an existing `final` / effectively final variable in the resource list.

```d2
direction: down
hdr: "try (a; b)" {
  width: 280
  height: 50
}
body: "try block" {
  width: 240
  height: 50
}
close: "b.close(); a.close()" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
ext: "your catch / finally" {
  width: 280
  height: 50
}
hdr -> body -> close -> ext
```

**Fig. 1.** Close is reverse initialization order. Extended `catch`/`finally` come after automatic close.

```java
class Demo {
    static String firstLine(String path) throws java.io.IOException {
        try (java.io.FileReader file = new java.io.FileReader(path);
             java.io.BufferedReader reader = new java.io.BufferedReader(file)) {
            return reader.readLine();
        }
    }
}
```

**Listing 1.** `reader` closes first, then `file`. `readLine` throwing still runs both closes.

> [!warning] Your `finally` is not the close
> On an extended try-with-resources, `catch` and `finally` run after resources are already closed. A throw from that `finally` still replaces the pending result. A handwritten `finally` that throws does **not** auto-suppress.

> [!warning] `AutoCloseable.close` is not required to be idempotent
> A second `close()` may have a side effect. Prefer `Closeable` (or an idempotent `close`) if the object might be closed twice. If the body succeeded, a throwing `close` **is** the result.

> [!tip] Interview answer
> **Try-with-resources is `try` with `AutoCloseable` resources in the header; the compiler closes them in reverse order.** `catch` and `finally` are optional and run after close. If `close` throws too, that exception is suppressed on the primary one — which is the difference from a `finally` that throws.
