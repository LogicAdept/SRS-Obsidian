<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch/TryWithResources #SRS

# How does the compiler translate try-with-resources?

> [!abstract] Short answer
> **It desugars to `try`/`catch`/`finally` that records a primary exception and closes each non-null resource.** If a primary exception already exists, `close()` failures are `addSuppressed` onto it; otherwise `close()` may throw as the primary. Several resources become nested try-with-resources, so close order is reverse of initialization. An explicit `catch`/`finally` wraps that whole translation and therefore runs **after** close.

## Primary exception plus a generated `finally`

A resource must be an `AutoCloseable`. Resources initialize left to right. After the `try` block, each resource that initialized to a **non-null** value is closed, in **reverse** order. One exception from an initializer, the body, or a `close` is primary; later close failures are suppressed on it ([[What is try-with-resources]], [[What is a suppressed exception in try-with-resources]]).

The compiler expresses that with a local `#primaryExc`, a `catch (Throwable)` that stores and rethrows, and a `finally` that null-checks the resource before `close()`:

```java
// Conceptual — one resource, no catch/finally on the try-with-resources
{
    final R r = expr;
    Throwable primaryExc = null;
    try {
        /* body */
    } catch (Throwable t) {
        primaryExc = t;
        throw t;
    } finally {
        if (r != null) {
            if (primaryExc != null) {
                try {
                    r.close();
                } catch (Throwable suppressedExc) {
                    primaryExc.addSuppressed(suppressedExc);
                }
            } else {
                r.close();
            }
        }
    }
}
```

**Listing 1.** Generated shape for a basic try-with-resources with one resource. Identifiers like `primaryExc` are compiler-made. See [[What happens if close throws after a try-with-resources body succeeds]], [[What happens if a try-with-resources resource is null]].

A `try` with *n* resources is treated as nested try-with-resources, one resource each. After *n* translations you have nested `try`/`catch`/`finally` blocks: the rightmost resource closes first ([[What happens if a later try-with-resources constructor throws]]).

An **extended** try-with-resources (`catch` and/or `finally` written by you) translates to a **basic** try-with-resources **inside** an ordinary `try`. Your `catch` can see initializer and `close` exceptions; `finally` runs after every close has been attempted ([[What is the difference between try-with-resources and try-finally when both throw]], [[Can a try block exist without catch and finally]]).

```d2
direction: down
src: "try (A a = ...; B b = ...) { body }" {
  width: 340
  height: 50
  style.fill: "#e3f2fd"
}
nest: "outer manages A\ninner manages B" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
close: "close B, then close A" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
wrap: "your catch/finally\nrun after those closes" {
  width: 300
  height: 70
  style.fill: "#f3e5f5"
}
src -> nest -> close -> wrap
```

**Fig. 1.** Nested translation: LIFO close, then the programmer’s `catch`/`finally`.

> [!warning] `null` resources are skipped, not closed
> The generated `if (r != null)` means a resource whose initializer yielded `null` is never `close()`d. That is not an NPE at close time.

> [!warning] A later initializer still closes earlier resources
> If `B`’s initializer throws, `A` was already initialized, so the outer generated `finally` still closes `A`. Failures while closing `A` are suppressed on the initializer exception, not the other way around.

> [!tip] Interview answer
> **Try-with-resources compiles to try/finally that closes non-null resources and uses `addSuppressed` when `close` fails after a primary exception.** Several resources nest, so they close last-in-first-out. Your own `catch` and `finally` wrap that and run after close.
