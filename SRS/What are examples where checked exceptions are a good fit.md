<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS

# What are examples where checked exceptions are a good fit?

> [!abstract] Short answer
> **When the caller can reasonably recover — retry, a fallback, or a user-facing choice — and you want the compiler to force that decision.** Classic JDK fits: **`IOException` / `FileNotFoundException`**, **`SQLException`**, **`InterruptedException`**, **`ClassNotFoundException`** on reflective load. Programming bugs (`NullPointerException`) and VM collapse (`Error`) are not this category.

## Recoverable, expected at the API boundary

Checked types are the exception classes other than `RuntimeException` and `Error`. `throws` is part of the method contract: callers must catch or specify ([[What are common examples of checked exceptions in Java]], [[How would you explain the throws clause for checked exceptions]], [[How do you define your own exception class in Java]]).

That contract is a **good fit** when failure is a normal outcome of talking to the world, and a competent caller has a response:

- **I/O** — `IOException` / `FileNotFoundException`: another path, create the file, degrade, or tell the user. The compiler stops a `read` from vanishing into an empty method ([[How can you avoid being forced to handle checked IOException]]).
- **JDBC** — `SQLException`: retry, fail the request, or close the connection. Not the same as a null dereference in your SQL string handling.
- **Interruption** — `InterruptedException`: blocking `sleep`/`wait`/`join` noticed `interrupt()`. Catch and restore the flag or rethrow; swallowing loses cancellation ([[How would you explain InterruptedException in Java threads]]).
- **Reflective load by name** — `ClassNotFoundException`: optional plugin missing. Contrast `NoClassDefFoundError`, which is an `Error` after a linkage / init failure ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

A **custom** checked type is the same test: extend `Exception` (not `RuntimeException`) when callers should be forced to notice. If they cannot recover, use unchecked instead ([[When should a custom exception extend RuntimeException]], [[Can you create a custom exception that extends RuntimeException]], [[How would you explain criticisms of checked exceptions in Java]]).

```d2
direction: down
fail: "operation can fail" {
  width: 280
  height: 50
}
rec: "caller can recover?" {
  width: 280
  height: 50
}
chk: "checked Exception" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
uc: "RuntimeException / Error" {
  width: 300
  height: 50
}
fail -> rec
rec -> chk: "yes"
rec -> uc: "no"
```

**Fig. 1.** Checked is for recoverable API failure, not for “I don’t want to think about `throws`.”

```java
class Demo {
    static String load(java.nio.file.Path path) throws java.io.IOException {
        return java.nio.file.Files.readString(path);
    }
}
```

**Listing 1.** Missing or unreadable file is an expected I/O outcome. Callers must catch or declare `IOException`.

> [!warning] Wrapping everything in `RuntimeException` is not a “modern” exemption
> It compiles. It also deletes the catch-or-specify signal that I/O and JDBC were designed around.

> [!warning] Checked is a bad fit for programmer mistakes
> `null` arguments, bad casts, and `1/0` are `RuntimeException`. Forcing `throws NullPointerException` would not make callers more correct.

> [!tip] Interview answer
> **Checked exceptions fit when the caller can recover and you want the compiler to require a decision.** `IOException`, `SQLException`, `InterruptedException`, and `ClassNotFoundException` are the usual JDK examples. Use `RuntimeException` for bugs and `Error` for VM failure — not because `throws` is inconvenient.
