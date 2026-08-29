<!--
reps: 0
priority: 0
-->
#Java/Exceptions #SRS

# How do you handle exceptions in Java applications?

> [!abstract] Short answer
> **Catch what you can recover from; declare or wrap the rest.** Checked exceptions must be `catch`ed or listed in `throws`. Unchecked exceptions and `Error` need no `throws`. Use `try` / `catch` / `finally` or try-with-resources. Catch the **specific** types you handle — not `Exception` or `Throwable` as a default.

## Catch-or-specify, then the `try` forms

A method or constructor that can throw a **checked** exception must handle it or name it in `throws`. Omitting both is a compile-time error ([[What happens if you neither catch nor declare a checked exception]], [[Does catching Exception satisfy a checked exception obligation]]). `RuntimeException` and `Error` are unchecked: you may catch them, but you need not declare them ([[Can you catch an unchecked exception in Java]]).

**`try` / `catch`:** the first matching `catch` runs; later clauses for the same throw do not ([[How many catch blocks execute for one thrown exception]]). Multi-catch `catch (A | B e)` shares one body when the recovery is the same ([[Can one catch block handle multiple exception types in Java]]).

**`finally`:** always runs for cleanup, with or without `catch`. It does not swallow the exception unless it completes abruptly ([[Can you try-finally without catch]]).

**Try-with-resources:** `AutoCloseable` resources are closed after the body; `close` failures can be suppressed on the primary exception ([[How does the compiler translate try-with-resources]], [[What is a suppressed exception in try-with-resources]]).

If nothing catches the throw, the thread’s **uncaught exception handler** runs (default: stack trace on standard error), then that thread dies ([[Can main throw exceptions outward and where are they handled]]).

At a layer that cannot recover, wrap a checked exception in a `RuntimeException` (or a custom unchecked type) so callers are not forced to declare it — the cause stays on `getCause()` ([[Does wrapping a checked exception in RuntimeException require a throws clause]], [[How do you define your own exception class in Java]], [[How should you throw and handle exceptions in Java]]). Do not treat `Error` like `IOException`, and do not catch `Error` or `Throwable` as everyday recovery ([[Why should you not catch java.lang.Error]], [[Can you catch Throwable]], [[How would you explain exception]]).

```d2
direction: down
throwable: "exception thrown" {
  width: 260
  height: 50
}
match: "matching catch\n(recover or wrap)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
specify: "throws on the method" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
uncaught: "uncaught handler\nthen thread ends" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
throwable -> match
throwable -> specify
throwable -> uncaught
```

**Fig. 1.** Handle, declare, or let the thread’s uncaught handler take it. `finally` / close still run on the way out.

```java
class Demo {
    static String read(java.nio.file.Path p) throws java.io.IOException {
        try (var in = java.nio.file.Files.newBufferedReader(p)) {
            return in.readLine();
        }
    }

    static int parse(String s) {
        try {
            return Integer.parseInt(s);
        } catch (NumberFormatException e) {
            return 0;
        }
    }
}
```

**Listing 1.** Checked I/O: try-with-resources plus `throws`. Unchecked parse: a local `catch` of a specific type. `catch (Exception e)` would also take `RuntimeException` and is the wrong default.

> [!warning] `catch (Exception)` is not a strategy
> It satisfies checked obligations and also swallows `RuntimeException`. Catch the types you can fix; let the rest propagate or wrap with a cause.

> [!warning] `catch (Throwable)` also takes `Error`
> OOM and stack overflow are not application recovery. Leave `Error` to the uncaught handler unless you are at a last-resort process boundary.

> [!tip] Interview answer
> **Checked exceptions: catch or `throws`. Unchecked: optional catch, no `throws`.** Use specific `catch` types, `finally` or try-with-resources for cleanup, and wrap at a boundary if this layer cannot recover. Do not catch `Error` or `Throwable` as a default.
