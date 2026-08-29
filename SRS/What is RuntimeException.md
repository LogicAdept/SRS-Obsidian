<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Exceptions/Hierarchy #SRS

# What is `RuntimeException`?

> [!abstract] Short answer
> **The superclass of Java’s application unchecked exceptions — types the compiler does not force you to catch or declare.** It sits **under** `Exception`, not beside it under `Throwable`. `Error` is also unchecked, but it is a sibling of `Exception`, not a `RuntimeException`.

## Under `Exception`, exempt from catch-or-declare

`RuntimeException` is a direct subclass of `Exception`. Together with its subclasses it is the **run-time exception** set. Compile-time checking skips those types **and** the `Error` branch. You may still catch them, and you may list them in `throws`; neither is required ([[Is RuntimeException a subclass of Exception]], [[Must you declare RuntimeException in a throws clause]], [[Can you catch an unchecked exception in Java]]).

`catch (Exception e)` matches `RuntimeException` because it is an `Exception`. It does **not** match `Error` ([[Does catch Exception also catch RuntimeException]], [[Does catch Exception also catch Error]], [[What is java.lang.Error]], [[Are Error subclasses checked or unchecked]], [[What is the difference between RuntimeException and Error]]).

Typical subclasses: `NullPointerException`, `IllegalArgumentException`, `ClassCastException`, `ArithmeticException`, `ArrayIndexOutOfBoundsException`, `NumberFormatException`. Wrapping a checked exception in `RuntimeException` also needs no `throws` for the checked type ([[Does wrapping a checked exception in RuntimeException require a throws clause]], [[What are common kinds of unchecked exceptions in Java]]).

```d2
direction: down
throwable: Throwable {
  width: 200
  height: 40
}
ex: Exception {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
err: Error {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
rte: RuntimeException {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
npe: NullPointerException {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
throwable -> ex
throwable -> err
ex -> rte
rte -> npe
```

**Fig. 1.** `RuntimeException` is under `Exception`. `Error` is the other unchecked branch.

```java
class Demo {
    static int divide() {
        return 10 / 0;
    }

    static void wrap() {
        throw new RuntimeException("unchecked wrapper");
    }
}
```

**Listing 1.** `divide` throws `ArithmeticException` (a `RuntimeException`). `wrap` throws `RuntimeException` itself. Neither method needs `throws` ([[What is ArithmeticException]], [[What is NullPointerException]]).

> [!warning] `RuntimeException` is not a sibling of `Exception`
> Whiteboard diagrams that hang both off `Throwable` are wrong. `Exception` → `RuntimeException`. The sibling of `Exception` is `Error`.

> [!warning] Unchecked is two branches
> Dumps say “unchecked = `RuntimeException`.” `Error` is unchecked too, and is **not** a `RuntimeException`. `OutOfMemoryError` is not a subclass of this type ([[What is java.lang.Error]]).

> [!tip] Interview answer
> **`RuntimeException` is the parent of application unchecked exceptions, and it extends `Exception`.** The compiler does not require `catch` or `throws`. `Error` is the other unchecked family, beside `Exception` under `Throwable`, not under `RuntimeException`.
