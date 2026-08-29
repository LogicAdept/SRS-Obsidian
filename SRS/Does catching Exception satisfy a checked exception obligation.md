<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/Exceptions/TryCatch #SRS

# Does catching `Exception` satisfy a checked exception obligation?

> [!abstract] Short answer
> **Yes, for checked types that are subclasses of `Exception`.** A `try` whose `catch` can catch `E` is not treated as throwing `E`. `IOException` and `SQLException` are subclasses of `Exception`, so `catch (Exception e)` is a legal catch-or-specify for them. The same handler also swallows `RuntimeException`. It does **not** catch `Error`, and it does not cover a checked type that is not an `Exception` (for example `Throwable` itself).

## Catch-or-specify looks at what can still escape

A method or constructor body must not be able to throw a checked class `E` unless `E` is a subclass of some type in `throws`. A `try` statement can throw `E` only if the `try` block (or resource `close`) can throw `E` **and** `E` is not assignment-compatible with any `catch` of that `try`. Catching `Exception` makes every `Exception` subtype — including `IOException` — a handled result. See [[What happens if you neither catch nor declare a checked exception]] and [[How would you explain the throws clause for checked exceptions]].

That is the same subtype rule as `throws IOException` covering `FileNotFoundException` ([[Does throws IOException cover FileNotFoundException]]): a **supertype** in `catch` or `throws` covers the more specific checked type.

```d2
direction: down
body: "try { load(); }\nload throws IOException" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
catchEx: "catch (Exception e)" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
ok: "IOException does not escape\nno throws required" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
rte: "RuntimeException also caught" {
  width: 280
  height: 60
  style.fill: "#ffebee"
}
body -> catchEx
catchEx -> ok
catchEx -> rte
```

**Fig. 1.** One `catch (Exception)` discharges typical checked obligations and the run-time branch together.

```java
class Demo {
    static void load() throws java.io.IOException {}

    static void run() {
        try {
            load();
        } catch (Exception e) {
            log(e);
        }
    }

    static void log(Exception e) {}
}
```

**Listing 1.** `run` needs no `throws`. `catch (IOException e)` would also suffice and would not take `NullPointerException`.

`catch (Exception e)` is legal even when the `try` block cannot throw any checked type. The unreachable-`catch` rule for checked types does **not** apply when the catch type is `Exception` or a superclass of `Exception`. `catch (IOException e)` around a `try` that cannot throw `IOException` (or a related checked type) **is** a compile-time error.

```java
class Demo {
    static void emptyTry() {
        try {
            System.out.println("ok");
        } catch (Exception e) {
            // compiles
        }
    }
}
```

**Listing 2.** `Exception` is excluded from the “try must be able to throw this checked type” rule. Replace `Exception` with `java.io.IOException` and the same `try` does not compile.

> [!warning] Satisfying the compiler is not a precise handler
> `catch (Exception e)` also matches `RuntimeException` ([[Does catch Exception also catch RuntimeException]]). A block meant to handle I/O will swallow an NPE and then continue. Prefer the most specific checked type you intend to recover from.

> [!warning] Not every checked type is an `Exception`
> `Error` is not an `Exception` ([[Does catch Exception also catch Error]]). `Throwable` is itself a checked class; `catch (Exception)` does not catch a thrown `Throwable` or a custom `extends Throwable` that is not an `Exception`. Those still need `catch (Throwable)`, a matching `catch`, or `throws`.

> [!tip] Interview answer
> **Yes — `catch (Exception e)` covers `IOException` and other checked subclasses of `Exception`, so the method need not declare them. It is a blunt tool: it also catches `RuntimeException`, and `catch (Exception)` stays legal even when the `try` throws no checked type. Catch the specific checked type when that is what you mean.**
