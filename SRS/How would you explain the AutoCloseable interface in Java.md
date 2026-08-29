<!--
reps: 0
priority: 0
-->
#Java/IO #Java/Exceptions/TryCatch/TryWithResources #SRS

# How would you explain the `AutoCloseable` interface in Java?

> [!abstract] Short answer
> **It is the type that try-with-resources can close for you.** `void close() throws Exception` releases the resource. A `try (` … `)` header may only name subtypes of `AutoCloseable`. `java.io.Closeable` is the I/O subtype that narrows `close` to `IOException` and requires an idempotent `close`.

## The hook try-with-resources calls

`AutoCloseable` is a single-method interface: `close()` relinquishes underlying resources (files, sockets, and similar). The compiler inserts that call when the resource goes out of a try-with-resources statement — in **reverse** initialization order, and only if the resource initialized to non-`null` ([[What is try-with-resources]], [[What happens if a try-with-resources resource is null]], [[Can a try block exist without catch and finally]]).

The resource type must be a subtype of `AutoCloseable`. You may declare the variable in the header, or refer to an existing `final` / effectively final variable. A plain `try` without resources still needs `catch` or `finally`.

`close` is declared `throws Exception`. Implementers should throw a **more specific** type, or nothing, if close cannot fail. Relinquish the resource and mark it closed **before** throwing. Unlike `Closeable.close`, `AutoCloseable.close` is **not required** to be idempotent — but it should be. Do not throw `InterruptedException` from `close`: suppression would fight the interrupt status ([[How would you explain InterruptedException in Java threads]]).

If the body throws and `close` also throws, the close exception is **suppressed** on the primary one ([[What is a suppressed exception in try-with-resources]], [[What happens if close throws after a try-with-resources body succeeds]]).

```d2
direction: down
try: "try (resource)" {
  width: 280
  height: 50
}
body: "try block" {
  width: 260
  height: 50
}
close: "resource.close()" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
try -> body -> close
```

**Fig. 1.** Try-with-resources initializes, runs the block, then calls `AutoCloseable.close`.

```java
class Box implements AutoCloseable {
    public void close() {
        System.out.println("closed");
    }
}

class Demo {
    static void run() {
        try (Box b = new Box()) {
            System.out.println("work");
        }
    }
}
```

**Listing 1.** `Box` is a legal resource because it implements `AutoCloseable`. `close` runs when the `try` ends.

> [!warning] `close()` is not required to be idempotent
> Calling it twice may have side effects unless you implement `Closeable` or make `close` harmless on a second call.

> [!warning] `throws Exception` is a wide contract
> A custom `close` that declares `Exception` forces callers (and try-with-resources) to handle `Exception`. Narrow the throws clause when you can.

> [!tip] Interview answer
> **`AutoCloseable` is what makes try-with-resources work: the compiler calls `close()` when the `try` ends.** `Closeable` is the I/O subinterface with `IOException` and an idempotent `close`. Don’t throw `InterruptedException` from `close`, and don’t treat a second `close` as automatically safe.
