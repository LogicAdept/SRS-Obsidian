<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/Exceptions/Unchecked #Java/Exceptions/Hierarchy #SRS

# What is the difference between `RuntimeException` and `Error`?

> [!abstract] Short answer
> **Both are unchecked — no required `catch` or `throws`.** **`RuntimeException` is under `Exception`:** programming defects you can often prevent or handle (`NullPointerException`, `ArithmeticException`, bounds errors). **`Error` is a sibling of `Exception` under `Throwable`:** serious JVM / environment failures ordinary code should not try to recover from (`OutOfMemoryError`, `StackOverflowError`). `Error` is **not** a `RuntimeException`.

## Same checking rule, different branches

The unchecked classes are the **run-time exception** classes (`RuntimeException` and subclasses) **and** the **error** classes (`Error` and subclasses). Neither family needs catch-or-declare ([[Must you declare RuntimeException in a throws clause]], [[Are Error subclasses checked or unchecked]], [[Can you catch an unchecked exception in Java]]).

`RuntimeException` is a direct subclass of `Exception`. Recovery from many of these is still possible; they often come from expression evaluation (divide by zero, null as an object, a bad index) ([[What is RuntimeException]], [[Is RuntimeException a subclass of Exception]], [[What is ArithmeticException]], [[Does catch Exception also catch RuntimeException]]).

`Error` is a direct subclass of `Throwable`, **beside** `Exception`. Ordinary programs are not expected to recover. That split exists so `catch (Exception e)` can take recoverable failures without also taking VM failures ([[What is java.lang.Error]], [[Does catch Exception also catch Error]], [[Why should you not catch java.lang.Error]], [[How do you produce a StackOverflowError]]).

`catch (RuntimeException e)` therefore misses every `Error`. `catch (Exception e)` also misses `Error`. Only `Throwable` (or `Error` itself) matches both unchecked families.

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
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
npe: NullPointerException {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
oome: OutOfMemoryError {
  width: 220
  height: 40
  style.fill: "#ffebee"
}
throwable -> ex
throwable -> err
ex -> rte
rte -> npe
err -> oome
```

**Fig. 1.** Two unchecked branches. `Error` is not under `RuntimeException`.

```java
class Demo {
    static int appDefect() {
        return 10 / 0;
    }

    static void catcher() {
        try {
            appDefect();
        } catch (RuntimeException e) {
            // ArithmeticException lands here
            // OutOfMemoryError does not
        }
    }
}
```

**Listing 1.** `appDefect` throws `ArithmeticException` (`RuntimeException`). `catch (RuntimeException)` does not handle `Error`. Neither method needs `throws`.

> [!warning] `Error` is not a “runtime exception”
> Dumps use “runtime” for anything unchecked. `Error` is unchecked, but it is **not** a subclass of `RuntimeException`. `AssertionError` and `OutOfMemoryError` are `Error`s.

> [!warning] `catch (RuntimeException)` is not “all unchecked”
> It misses the entire `Error` branch. `catch (Exception)` misses it too. That is the point of hanging `Error` beside `Exception`.

> [!tip] Interview answer
> **Both `RuntimeException` and `Error` are unchecked, but they sit in different places.** `RuntimeException` is under `Exception` for programming defects you might handle. `Error` is a sibling of `Exception` for JVM failures you should not recover from. Catching `RuntimeException` never catches `Error`.
