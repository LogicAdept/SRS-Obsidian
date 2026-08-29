<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS

# What happens if you neither catch nor declare a checked exception?

> [!abstract] Short answer
> **The code does not compile.** If a method or constructor body can throw a checked type `E`, `E` (or a supertype) must appear in `throws`, or a `catch` must handle it. Typical compiler wording: unreported exception … must be caught or declared to be thrown. `RuntimeException` and `Error` do **not** trigger this error.

## Catch or declare — at compile time

Checked exception classes are `Throwable` and its subclasses except the `RuntimeException` and `Error` families ([[Is Throwable a checked exception]], [[What are common examples of checked exceptions in Java]]). For each checked `E` the body can throw, the compiler requires a handler or a `throws` mention of `E` or a superclass of `E` ([[How would you explain the throws clause for checked exceptions]], [[Does throws IOException cover FileNotFoundException]], [[Does catching Exception satisfy a checked exception obligation]]).

`FileInputStream(String)` can throw `FileNotFoundException`. Using it in `main` (or any method) with no `try`/`catch` and no `throws` is the usual illustration. Adding `throws FileNotFoundException` / `throws IOException` or a matching `catch` makes the same code compile.

`throws` on `main` satisfies the compiler. If that exception still escapes at run time, the thread’s uncaught handler runs (typically a stack trace) ([[Must every caller catch exceptions declared in a throws clause]]).

Unchecked types (`RuntimeException`, `Error`) may be thrown without `throws` or `catch` ([[Must you declare RuntimeException in a throws clause]]). Wrapping a checked exception in `RuntimeException` also removes the obligation for the **wrapper** ([[Does wrapping a checked exception in RuntimeException require a throws clause]]).

Static initializers cannot declare `throws`; a checked throw there is always a compile error. A lambda may throw a checked type only if the targeted function type lists it ([[Can a static initializer throw a checked exception]], [[Can a lambda throw a checked exception]], [[Can a constructor throw a checked exception]]).

```d2
direction: down
body: "body can throw IOException" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
err: "no catch and no throws\ncompile-time error" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
ok: "catch or throws IOException\ncompiles" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
body -> err
body -> ok
```

**Fig. 1.** The failure is compile-time. Unchecked throws never take this path.

```java
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

class Demo {
    static void bad() {
        new FileInputStream("missing"); // compile-time error
    }

    static void declared() throws FileNotFoundException {
        new FileInputStream("missing");
    }

    static void caught() {
        try {
            new FileInputStream("missing");
        } catch (IOException e) {
            System.out.println(e);
        }
    }
}
```

**Listing 1.** `bad` is rejected. `declared` and `caught` compile. `catch (IOException)` covers `FileNotFoundException`.

> [!warning] Unchecked types never need this pair of remedies
> You can throw `NullPointerException` or `AssertionError` with no `throws`. The “must be caught or declared” rule is **checked-only**.

> [!warning] `throws` is not “the JVM will catch it”
> Declaring `throws` on `main` only silences the compiler. If nobody catches it, the process still fails at run time with an uncaught exception.

> [!tip] Interview answer
> **It is a compile error — a checked exception must be caught or declared in `throws`.** `FileInputStream` / missing file is the usual example. `RuntimeException` and `Error` do not need that. `throws` on `main` compiles; if it still escapes, you get a stack trace, not a second compile error.
