<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS

# How would you explain the Java exception type hierarchy?

> [!abstract] Short answer
> **Everything you can `throw` is a `Throwable`.** `Exception` and `Error` sit as **siblings** under it. `RuntimeException` is under `Exception`, not beside it. **Checked** types are `Throwable` minus `RuntimeException` and minus `Error`. `catch (Exception)` is meant to miss `Error`.

## One root, two recovery stories

Only `Throwable` (and its subclasses) may be thrown or caught. `Exception` is the superclass of conditions ordinary programs may recover from. `Error` is the superclass of conditions they are **not** ordinarily expected to recover from — that split exists so `catch (Exception e)` can skip errors ([[What is java.lang.Error]], [[Does catch Exception also catch Error]], [[Can you throw an object that is not a Throwable]]).

`RuntimeException` is a **direct subclass of `Exception`**. It and its subclasses are the **run-time exception classes**. Together with the error classes, they are **unchecked**: no catch-or-specify. Everything else in the `Throwable` tree is **checked**, including `Throwable` itself and a custom class that extends `Throwable` directly ([[Is RuntimeException a subclass of Exception]], [[Does catch Exception also catch RuntimeException]], [[Are Error subclasses checked or unchecked]], [[Do checked exceptions inherit Throwable directly]], [[What happens if you neither catch nor declare a checked exception]]).

`IOException` is a typical checked type under `Exception`. `VirtualMachineError` (`OutOfMemoryError`, `StackOverflowError`) sits under `Error`, not under `Exception` ([[What is VirtualMachineError]], [[How would you explain exception]], [[How would you explain the java.lang.Exception type hierarchy]], [[Is Throwable a checked exception]]). You do not need a fifth “base” for `IOException` or `NullPointerException`; those are ordinary subclasses.

```d2
direction: down
throwable: "Throwable" {
  width: 220
  height: 50
}
ex: "Exception" {
  width: 240
  height: 50
}
err: "Error" {
  width: 240
  height: 50
}
rte: "RuntimeException\n(unchecked)" {
  width: 260
  height: 70
}
chk: "IOException\n(checked)" {
  width: 260
  height: 70
}
vme: "VirtualMachineError" {
  width: 260
  height: 50
}
throwable -> ex
throwable -> err
ex -> rte
ex -> chk
err -> vme
```

**Fig. 1.** `Error` is not a kind of `Exception`. `RuntimeException` is.

```java
class Demo {
    static void show(Throwable t) {
        System.out.println(t instanceof Exception);
        System.out.println(t instanceof Error);
        System.out.println(t instanceof RuntimeException);
    }
}
```

**Listing 1.** A `NullPointerException` is both `Exception` and `RuntimeException`. An `OutOfMemoryError` is neither.

> [!warning] Do not draw `RuntimeException` as a sibling of `Exception`
> Unchecked is a **compiler rule**, not a third fork under `Throwable`. `catch (Exception)` still catches `RuntimeException`.

> [!warning] `extends Throwable` is checked
> “Checked means extends `Exception`” is incomplete. A direct `Throwable` subclass is checked and is **not** caught by `catch (Exception)`.

> [!tip] Interview answer
> **`Throwable` is the root; `Exception` and `Error` are the two branches.** `RuntimeException` lives under `Exception` and is unchecked, as is every `Error`. Checked types are the rest of the tree. `catch (Exception)` is built to recover from ordinary exceptions without catching `Error`.
