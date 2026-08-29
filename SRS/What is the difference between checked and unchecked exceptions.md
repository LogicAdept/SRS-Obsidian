<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/Exceptions/Unchecked #SRS

# What is the difference between checked and unchecked exceptions?

> [!abstract] Short answer
> **Checked: the compiler requires `catch` or `throws`. Unchecked: it does not.** Unchecked types are **`RuntimeException` and `Error`** (and their subclasses). Checked is the rest of the `Throwable` tree — typically `Exception` minus `RuntimeException`, but also `Throwable` itself.

## Compiler obligation vs type set

| | Checked | Unchecked |
| --- | --- | --- |
| Rule | `catch` or `throws` or the program does not compile | neither is required |
| Types | `Throwable` except `RuntimeException*` and `Error*` | `RuntimeException` subtree and `Error` subtree |
| Typical use | recoverable I/O, JDBC, interrupt | bugs (`NPE`, `IAE`) and VM failure (`OOME`) |

`RuntimeException` is still an `Exception`. Unchecked is not a third child of `Throwable` ([[Is RuntimeException a subclass of Exception]], [[How would you explain the Java exception type hierarchy]], [[Is Throwable a checked exception]]).

A method that can throw `IOException` must specify or catch it ([[What happens if you neither catch nor declare a checked exception]], [[How would you explain the throws clause for checked exceptions]], [[What are common examples of checked exceptions in Java]], [[What are examples where checked exceptions are a good fit]]). `throws RuntimeException` is optional documentation ([[Must you declare RuntimeException in a throws clause]]).

The language exempts `Error` because recovery is not ordinary and declaring them would clutter APIs. It exempts run-time exceptions because a compiler cannot generally prove they will not occur (for example `NullPointerException`). Checked types are for conditions a caller can reasonably be expected to handle.

Common unchecked names: `NullPointerException`, `IllegalArgumentException`, `IllegalStateException`, `ArithmeticException`, `ClassCastException`, `IndexOutOfBoundsException`, `ConcurrentModificationException`, `NumberFormatException` ([[What is ArrayIndexOutOfBoundsException]], [[What is ArithmeticException]], [[What is ConcurrentModificationException]], [[What are common kinds of unchecked exceptions in Java]]). `Error` is unchecked too; do not treat catching it as recovery ([[Are Error subclasses checked or unchecked]], [[Why should you not catch java.lang.Error]]).

```d2
direction: right
chk: "checked\ncatch or throws" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
uc: "unchecked\nRTE + Error" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
```

**Fig. 1.** The difference that matters in an interview is the compiler rule, then which types sit in each bucket.

```java
class Demo {
    static void checked() throws java.io.IOException {
        throw new java.io.IOException("io");
    }

    static void unchecked() {
        throw new NullPointerException();
    }
}
```

**Listing 1.** Drop `throws` from `checked()` and it fails to compile. `unchecked()` compiles with no `throws`.

> [!warning] “Checked means extends `Exception`” is incomplete
> That misses `Error` (unchecked) and a custom `extends Throwable` (checked, not caught by `catch (Exception)`).

> [!warning] `catch (Exception)` is not “the checked handler”
> It also catches `RuntimeException`. The difference is not “`Exception` vs everything else.” `Error` is a `Throwable` that simply does not participate in catch-or-specify.

> [!tip] Interview answer
> **Checked exceptions must be caught or declared; unchecked ones need not.** Unchecked is `RuntimeException` plus `Error`. `IOException` is checked; `NullPointerException` and `OutOfMemoryError` are not. `RuntimeException` still extends `Exception`.
