<!--
reps: 0
priority: 0
-->
#Java/Exceptions #SRS

# How do you propagate an exception up the call stack in Java?

> [!abstract] Short answer
> **Do not catch it.** Control leaves the method and looks for the nearest enclosing `catch` in a caller. For a **checked** exception, the method must declare `throws` (or wrap it in an unchecked type). Unchecked exceptions propagate with no `throws`. There is no C#-style `throw;` — rethrow with `throw e` or wrap.

## Uncaught means “search the caller”

A `throw` (or a method that throws) completes abruptly. The JVM looks for the nearest dynamically enclosing `catch` that can handle that type. If the current method has none, the search continues at the **invocation** that called this method, then that method’s caller, and so on ([[How do you handle exceptions in Java applications]], [[What happens if no catch matches and a finally block is present]]).

`finally` blocks and try-with-resources `close` still run as control leaves each `try`. They do not stop propagation unless they complete abruptly themselves.

**Checked:** a method whose body can throw checked type `E` must `catch` `E` or declare `throws E` (or a supertype). `throws` does **not** handle the exception; it **permits** it to leave so callers are forced to catch-or-specify ([[What happens if you neither catch nor declare a checked exception]], [[Can a constructor throw a checked exception]], [[How do checked exceptions work with method overriding]], [[Can a lambda throw a checked exception]]).

**Unchecked:** `RuntimeException` and `Error` need no `throws`. They still propagate until a matching `catch` or the thread’s uncaught handler ([[Must you declare RuntimeException in a throws clause]], [[Can main throw exceptions outward and where are they handled]]).

**Catch then propagate:** `throw e;` rethrows the same object (stack already filled). `throw new Wrapper(e)` starts a new throwable with `e` as cause; callers then see the wrapper type, not `E`. Wrapping a checked exception in `RuntimeException` / `UncheckedIOException` lets this method omit `throws E` ([[Does wrapping a checked exception in RuntimeException require a throws clause]]).

If no `catch` in the thread matches, the uncaught exception handler runs and that thread terminates.

```d2
direction: down
inner: "inner() throws IOException" {
  width: 300
  height: 50
}
mid: "middle() throws IOException\n(no catch)" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
top: "caller catch or uncaught handler" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
inner -> mid -> top
```

**Fig. 1.** Propagation is “no matching catch here,” not a special send API. `throws` only makes the checked case legal.

```java
class Demo {
    static void inner() throws java.io.IOException {
        throw new java.io.IOException("x");
    }

    static void middle() throws java.io.IOException {
        inner();
    }

    static void wrap() {
        try {
            inner();
        } catch (java.io.IOException e) {
            throw new java.io.UncheckedIOException(e);
        }
    }
}
```

**Listing 1.** `middle` propagates the same checked type. `wrap` propagates an unchecked wrapper; `wrap` needs no `throws IOException`.

> [!warning] `throws` is not a handler
> It is the specify half of catch-or-specify. Callers still must catch or declare. Omitting `throws` on a method that can throw a checked exception is a compile-time error, not silent wrapping.

> [!warning] Java has no bare `throw;`
> After `catch (Exception e)`, write `throw e;` or wrap. A new `throw new Exception()` without a cause drops the original unless you pass it to `super` / the constructor.

> [!tip] Interview answer
> **You propagate by not catching — the exception walks up the call stack until a matching `catch`.** Checked types need `throws` on each method that lets them through, or wrap them in an unchecked exception. Unchecked exceptions propagate without `throws`; if nothing catches them, the thread’s uncaught handler runs.
