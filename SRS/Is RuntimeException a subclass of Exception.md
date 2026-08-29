<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS

# Is `RuntimeException` a subclass of `Exception`?

> [!abstract] Short answer
> **Yes.** `RuntimeException` extends `Exception` (which extends `Throwable`). It is **not** a sibling of `Exception` under `Throwable`. Unchecked application exceptions sit on the `RuntimeException` branch; other `Exception` subclasses are the checked branch. `catch (Exception e)` therefore matches `NullPointerException` and the rest of that branch.

## Under `Exception`, still unchecked

The API declaration is `public class RuntimeException extends Exception`. `Throwable` splits into `Error` and `Exception`. `RuntimeException` hangs off **`Exception`**, not off `Throwable` beside it ([[What is RuntimeException]], [[What is the difference between RuntimeException and Error]], [[Do checked exceptions inherit Throwable directly]]).

Compile-time checking still treats `RuntimeException` and its subclasses as **unchecked**: they need not appear in `throws` ([[Must you declare RuntimeException in a throws clause]], [[What is the difference between checked and unchecked exceptions]], [[Can you catch an unchecked exception in Java]]). That is a checking rule, not a different superclass.

Because the run-time type is a subtype of `Exception`, `catch (Exception e)` also catches `RuntimeException` (including `NullPointerException`). It does **not** catch `Error` ([[Does catch Exception also catch RuntimeException]], [[Does catch Exception also catch Error]]).

```d2
direction: down
t: "Throwable" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
err: "Error" {
  width: 200
  height: 50
  style.fill: "#fff8e1"
}
ex: "Exception" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
rte: "RuntimeException\n(unchecked)" {
  width: 240
  height: 60
  style.fill: "#ffebee"
}
ch: "other Exception\n(checked)" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
t -> err
t -> ex
ex -> rte
ex -> ch
```

**Fig. 1.** `RuntimeException` is a child of `Exception`. `Error` is the other child of `Throwable` ([[Are Error subclasses checked or unchecked]], [[Is AssertionError a subclass of Exception]]).

```java
class Demo {
    static void assign() {
        Exception e = new RuntimeException("x");
        throw (RuntimeException) e;
    }

    static void catches() {
        try {
            throw new NullPointerException();
        } catch (Exception e) {
            System.out.println(e.getClass().getName());
        }
    }
}
```

**Listing 1.** An `Exception` variable can hold a `RuntimeException`. `catch (Exception)` matches `NullPointerException`. Neither line needs `throws`. Custom unchecked types extend `RuntimeException` ([[When should a custom exception extend RuntimeException]]).

> [!warning] Diagrams that put `RuntimeException` next to `Exception`
> Some slides draw `Throwable` → `Error` | `Exception` | `RuntimeException`. That is wrong. `RuntimeException` is **inside** `Exception`. `Error` is the sibling of `Exception`.

> [!warning] `catch (Exception)` is not “checked only”
> It is assignment-compatible with every `Exception`, including unchecked ones. If you meant “not `Error` and not runtime,” catch a more specific type (or do not catch `Exception` at all).

> [!tip] Interview answer
> **Yes — `RuntimeException` extends `Exception`, so it is not a sibling of `Exception` under `Throwable`.** It is still unchecked. `catch (Exception)` therefore also catches `NullPointerException` and other runtime exceptions.
