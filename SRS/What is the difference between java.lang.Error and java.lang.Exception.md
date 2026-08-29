<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/Exceptions/Hierarchy #SRS

# What is the difference between `java.lang.Error` and `java.lang.Exception`?

> [!abstract] Short answer
> **They are siblings under `Throwable`, not parent and child.** `Exception` is the recover-from branch (checked types plus `RuntimeException`). `Error` is the not-ordinarily-recoverable branch and is **unchecked**. `catch (Exception)` never matches an `Error`.

## Recovery vs serious failure

`Exception` is the superclass of conditions ordinary programs may wish to recover from. `Error` is the superclass of conditions they are **not** ordinarily expected to recover from. That split is why `catch (Exception e)` is a legal idiom that skips `Error` ([[Why is Error a sibling of Exception rather than a subclass]], [[Does catch Exception also catch Error]], [[What is java.lang.Error]], [[How would you explain the Java exception type hierarchy]]).

`Error` and every subclass are **unchecked**. `Exception` is mixed: `IOException` is checked; `RuntimeException` (still an `Exception`) is not ([[Are Error subclasses checked or unchecked]], [[Is RuntimeException a subclass of Exception]], [[How would you explain the java.lang.Exception type hierarchy]], [[What is the difference between RuntimeException and Error]]).

Catching `Error` compiles. It is not a recovery strategy after resource collapse ([[Why should you not catch java.lang.Error]]).

```d2
direction: down
th: "Throwable" {
  width: 240
  height: 50
}
ex: "Exception\nrecover" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
err: "Error\nnot ordinary recover" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
th -> ex
th -> err
```

**Fig. 1.** `Error` is not a kind of `Exception`. `catch (Exception)` follows the left branch only.

```java
class Demo {
    static void kinds(Throwable t) {
        System.out.println(t instanceof Exception);
        System.out.println(t instanceof Error);
    }
}
```

**Listing 1.** `IOException` prints `true` then `false`. `OutOfMemoryError` prints `false` then `true`.

> [!warning] `Exception` is not “every throwable”
> `catch (Exception)` misses `Error` and a custom class that extends `Throwable` directly.

> [!warning] `RuntimeException` is not `Error`
> Both are unchecked. Only `RuntimeException` is an `Exception`. `catch (Exception)` swallows NPE and misses OOME.

> [!tip] Interview answer
> **`Exception` and `Error` sit side by side under `Throwable`.** `Exception` is for recovery (including checked I/O and unchecked `RuntimeException`). `Error` is for serious VM/linkage failure and is unchecked. `catch (Exception)` is built to skip `Error`.
