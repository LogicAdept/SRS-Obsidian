<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS

# What are common kinds of unchecked exceptions in Java?

> [!abstract] Short answer
> **Unchecked means `RuntimeException` and `Error` — no catch-or-specify.** Common run-time types: `NullPointerException`, `IllegalArgumentException`, `IllegalStateException`, `ClassCastException`, `ArithmeticException`, `IndexOutOfBoundsException` / `ArrayIndexOutOfBoundsException`, `NumberFormatException`, `UnsupportedOperationException`, `ConcurrentModificationException`. Common `Error`s: `OutOfMemoryError`, `StackOverflowError`. Contrast: `IOException` and `SQLException` are checked.

## Two unchecked families, many everyday types

`RuntimeException` (under `Exception`) and `Error` are exempt from compile-time checking ([[Is RuntimeException a subclass of Exception]], [[Are Error subclasses checked or unchecked]], [[Must you declare RuntimeException in a throws clause]]). You **may** catch them; you are not **required** to ([[Can you catch an unchecked exception in Java]]).

Typical **run-time** types in the JDK:

- **`NullPointerException`** — `null` used as an object ([[What is NullPointerException]])
- **`IllegalArgumentException` / `IllegalStateException`** — bad argument vs wrong receiver state ([[What is the difference between IllegalArgumentException and IllegalStateException]])
- **`NumberFormatException`** — failed numeric parse (a kind of `IllegalArgumentException`)
- **`ClassCastException`** — `cast` to a type the object is not
- **`ArithmeticException`** — integer `/` or `%` by zero ([[What is ArithmeticException]])
- **`ArrayIndexOutOfBoundsException`** — illegal array index ([[What is ArrayIndexOutOfBoundsException]])
- **`UnsupportedOperationException`** — optional mutator not implemented ([[How would you explain give when which collection UnsupportedOperationException]])
- **`ConcurrentModificationException`** — fail-fast collection / iterator ([[What is ConcurrentModificationException]])

Typical **error** types (still unchecked, not under `RuntimeException`): `OutOfMemoryError`, `StackOverflowError` ([[How would you explain OutOfMemoryError]]).

Checked counterparts such as `IOException` and `SQLException` **do** require `catch` or `throws` ([[What are common examples of checked exceptions in Java]], [[How would you explain the java.lang.Exception type hierarchy]]).

```d2
direction: down
uc: "unchecked" {
  width: 240
  height: 50
}
rte: "RuntimeException" {
  width: 280
  height: 50
}
err: "Error" {
  width: 240
  height: 50
}
npe: "NPE / IAE / CCE / ..." {
  width: 300
  height: 50
}
oom: "OOME / SOE" {
  width: 240
  height: 50
}
uc -> rte -> npe
uc -> err -> oom
```

**Fig. 1.** Interview “unchecked” as two subtrees, then name the everyday `RuntimeException`s.

```java
class Demo {
    static int boom(int n) {
        return 1 / n;
    }
}
```

**Listing 1.** `boom(0)` throws `ArithmeticException`, a `RuntimeException`. No `throws` is required.

> [!warning] `catch (Exception e)` still catches these run-time types
> They live under `Exception`. A wide I/O handler will swallow `NullPointerException` too.

> [!warning] “Modern stacks prefer unchecked” is not the language rule
> Recoverability is why a type is checked. Extending `RuntimeException` only to skip `throws` is not the criterion.

> [!tip] Interview answer
> **Unchecked exceptions are `RuntimeException` and `Error`.** Name `NullPointerException`, `IllegalArgumentException`, `ClassCastException`, and `ArithmeticException` for the run-time side, and `OutOfMemoryError` for `Error`. `IOException` is the usual checked contrast — the compiler forces `catch` or `throws`.
