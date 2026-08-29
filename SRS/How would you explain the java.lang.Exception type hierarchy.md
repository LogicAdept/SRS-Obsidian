<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #Java/Exceptions/Checked #Java/Exceptions/Unchecked #SRS

# How would you explain the `java.lang.Exception` type hierarchy?

> [!abstract] Short answer
> **`Exception` is the recovery branch under `Throwable`, a sibling of `Error`.** It holds **two** compiler stories: **checked** types (`IOException`, `SQLException`, `InterruptedException`, …) and **`RuntimeException`** (unchecked: `NullPointerException`, `IllegalArgumentException`, …). `catch (Exception)` matches **both**. It does **not** match `Error`.

## Recovery branch, not “checked only”

`Exception` is the superclass of conditions ordinary programs may wish to recover from. `Error` sits beside it, not under it ([[How would you explain the Java exception type hierarchy]], [[How would you explain the java.lang.Error type hierarchy]], [[What is the difference between RuntimeException and Error]], [[Does catch Exception also catch Error]]).

`RuntimeException` is a **direct subclass of `Exception`**. It and its subclasses are the run-time exception classes — **unchecked**. The rest of the `Exception` tree is **checked**: catch or declare ([[Is RuntimeException a subclass of Exception]], [[Does catch Exception also catch RuntimeException]], [[Does catching Exception satisfy a checked exception obligation]], [[What happens if you neither catch nor declare a checked exception]]).

Typical checked children (often not direct): `IOException` / `FileNotFoundException`, `SQLException`, `InterruptedException`, `ReflectiveOperationException` (`ClassNotFoundException`). Typical run-time children: `NullPointerException`, `IllegalArgumentException`, `IllegalStateException`, `ArithmeticException`, `UnsupportedOperationException`, `ConcurrentModificationException` ([[What are common examples of checked exceptions in Java]], [[What are common kinds of unchecked exceptions in Java]], [[How would you explain InterruptedException in Java threads]]).

New types follow the same split: extend `Exception` (not `RuntimeException`) for a checked type; extend `RuntimeException` for an unchecked one. Extending `Throwable` directly is checked and **misses** `catch (Exception)` ([[How do you define your own exception class in Java]], [[Do checked exceptions inherit Throwable directly]]).

```d2
direction: down
ex: "Exception" {
  width: 240
  height: 50
}
rte: "RuntimeException\nunchecked" {
  width: 280
  height: 70
}
chk: "checked children" {
  width: 280
  height: 50
}
npe: "NPE / IAE / ISE" {
  width: 280
  height: 50
}
io: "IOException / SQLException\nInterruptedException" {
  width: 300
  height: 70
}
ex -> rte
ex -> chk
rte -> npe
chk -> io
```

**Fig. 1.** Unchecked is a **subtree** of `Exception`, not a third fork under `Throwable`.

```java
class Demo {
    static void kinds(Exception e) {
        System.out.println(e instanceof Error);
        System.out.println(e instanceof RuntimeException);
    }
}
```

**Listing 1.** An `IOException` is an `Exception` and not a `RuntimeException`. A `NullPointerException` is both `Exception` and `RuntimeException`. An `OutOfMemoryError` never arrives here.

> [!warning] `catch (Exception e)` is not “checked only”
> It swallows `RuntimeException`. Use `catch (RuntimeException)` when you mean only the unchecked subtree.

> [!warning] “`Exception` means checked” is false
> Checked means “not `RuntimeException` and not `Error`.” Many `Exception`s are unchecked because they extend `RuntimeException`.

> [!tip] Interview answer
> **`Exception` is the recover-from branch under `Throwable`.** Draw `RuntimeException` **inside** it — that subtree is unchecked; the rest is checked (`IOException`, and so on). `catch (Exception)` hits both, and it never hits `Error`.
