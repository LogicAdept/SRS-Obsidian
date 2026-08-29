<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS

# What are common examples of checked exceptions in Java?

> [!abstract] Short answer
> **Interview lists usually name `IOException`, `FileNotFoundException`, `ClassNotFoundException`, `InterruptedException`, `SQLException`, and `ParseException`.** They are checked: not under `RuntimeException` or `Error`, so a method that can throw them must catch or declare. Opening a missing file with `FileInputStream` is the stock example (`FileNotFoundException`, an `IOException`).

## Checked API types you are expected to name

A checked exception class is `Throwable` or a subclass that is not in the `RuntimeException` or `Error` families. The body must catch it or name it (or a supertype) in `throws` ([[What is the difference between checked and unchecked exceptions]], [[Is Throwable a checked exception]], [[How would you explain the throws clause for checked exceptions]], [[What happens if you neither catch nor declare a checked exception]]).

Typical examples:

- **`IOException`** / **`FileNotFoundException`** — I/O. `FileNotFoundException` extends `IOException`. `FileInputStream(String)` throws the subclass; `throws IOException` covers it ([[Does throws IOException cover FileNotFoundException]], [[Do checked exceptions inherit Throwable directly]]).
- **`ClassNotFoundException`** — load-by-name (`Class.forName`, `ClassLoader.loadClass`). It extends `ReflectiveOperationException`, which extends `Exception`.
- **`InterruptedException`** — a blocking call (`Thread.sleep`, `Object.wait`, …) was interrupted. It extends `Exception` ([[How would you explain InterruptedException in Java threads]]).
- **`SQLException`** — JDBC (`java.sql`). Checked `Exception`.
- **`ParseException`** (`java.text`) — a parse failed; extends `Exception`.

These are not the unchecked NPE / `IllegalArgumentException` / `Error` set ([[What are common kinds of unchecked exceptions in Java]], [[What are examples where checked exceptions are a good fit]]).

```d2
direction: down
ex: "Exception (checked)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
io: "IOException" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
fnf: "FileNotFoundException" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
roe: "ReflectiveOperationException" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
cnf: "ClassNotFoundException" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
ie: "InterruptedException" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
err: "Error (unchecked)" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
ncd: "NoClassDefFoundError" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
ex -> io -> fnf
ex -> roe -> cnf
ex -> ie
err -> ncd
```

**Fig. 1.** Stock checked types under `Exception`. `NoClassDefFoundError` is an `Error`, not a checked twin of `ClassNotFoundException`.

```java
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

class Demo {
    static FileInputStream open(String path) throws FileNotFoundException {
        return new FileInputStream(path);
    }

    static void openAndRead(String path) throws IOException {
        try (FileInputStream in = new FileInputStream(path)) {
            in.read();
        }
    }
}
```

**Listing 1.** The constructor throws `FileNotFoundException`. Try-with-resources can also throw `IOException` from `close`, so `openAndRead` declares the supertype ([[What is try-with-resources]]).

> [!warning] `FileNotFoundException` is not a second I/O branch
> Listing both `IOException` and `FileNotFoundException` is a parent/child pair. Catch the subclass first, or declare only the supertype. `throws IOException` already covers `FileNotFoundException`.

> [!warning] `ClassNotFoundException` is not `NoClassDefFoundError`
> `ClassNotFoundException` is checked. `NoClassDefFoundError` extends `LinkageError` (`Error`) and is unchecked. A class that was present at compile time and missing at run time is the `Error`, not the checked type ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

> [!warning] Swallowing `InterruptedException` drops the interrupt
> Catching it is required if you do not declare it, but the API says to rethrow or call `Thread.currentThread().interrupt()` before continuing. Empty `catch` is a common interview miss.

> [!tip] Interview answer
> **Common checked examples are `IOException` / `FileNotFoundException`, `ClassNotFoundException`, `InterruptedException`, `SQLException`, and `ParseException`.** They must be caught or declared. `FileNotFoundException` is an `IOException`; `NoClassDefFoundError` is an `Error`, not a checked class-not-found.
