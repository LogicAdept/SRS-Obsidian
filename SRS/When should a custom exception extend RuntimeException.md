<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Exceptions/Checked #SRS

# When should a custom exception extend `RuntimeException`?

> [!abstract] Short answer
> **When the caller cannot reasonably recover — typically a programming error or a contract/validation failure.** Unchecked types do not force `throws` on every method. If the caller **can** be expected to handle a recoverable condition, extend `Exception` (checked) instead. Do **not** extend `RuntimeException` just to dodge catch-or-declare.

## Recoverable vs programming problem

`RuntimeException` and its subclasses are unchecked: callers need not catch or declare them ([[What is RuntimeException]], [[Must you declare RuntimeException in a throws clause]], [[Can you catch an unchecked exception in Java]]).

Use a custom `RuntimeException` when the failure is in the same family as the built-in run-time types: the caller used the API incorrectly, broke a precondition, or hit a defect the client cannot usefully repair. Illegal arguments and illegal state are the stock JDK pattern ([[Should you throw NullPointerException or IllegalArgumentException for a null argument]], [[What is the difference between IllegalArgumentException and IllegalStateException]]).

If a client can reasonably recover, make the type **checked** (`extends Exception`, not `RuntimeException`). Then every method that does not handle it must list it in `throws` ([[What happens if you neither catch nor declare a checked exception]], [[How do checked exceptions work with method overriding]]).

The language still expects most **new** exception types that benefit from compile-time checking to be checked. Creating a `RuntimeException` subclass only so you never write `throws` sidesteps that design.

Do **not** extend `Error` for business failures. `Error` is for serious VM/system conditions ordinary code should not recover from ([[What is java.lang.Error]], [[Why should you not catch java.lang.Error]]). Wrapping a checked exception in `RuntimeException` is a separate trick so a method can stay free of `throws` for the checked type ([[Does wrapping a checked exception in RuntimeException require a throws clause]]).

A custom unchecked exception **can** still be caught. Unchecked means the compiler does not **require** a handler, not that `catch` is illegal.

```d2
direction: down
q: "Can the caller reasonably recover?" {
  width: 320
  height: 50
}
yes: "extends Exception (checked)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
no: "extends RuntimeException" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
q -> yes
q -> no
```

**Fig. 1.** Recoverable expected condition versus programming/contract failure.

```java
class InvalidQuantityException extends RuntimeException {
    InvalidQuantityException(String message) { super(message); }
}

class ExportFailedException extends Exception {
    ExportFailedException(String message) { super(message); }
}

class Demo {
    static void place(int qty) {
        if (qty <= 0) {
            throw new InvalidQuantityException("qty");
        }
    }

    static void export() throws ExportFailedException {
        throw new ExportFailedException("disk");
    }
}
```

**Listing 1.** `place` needs no `throws`. `export` must declare the checked type. Catching `InvalidQuantityException` is legal; the compiler will not require it.

> [!warning] Unchecked is not a shortcut around API design
> If every custom failure is a `RuntimeException` so `javac` stays quiet, callers lose the catch-or-declare contract. Use unchecked when recovery is not a realistic client duty.

> [!warning] `Error` is not your domain exception
> Business “fatal” is still an `Exception` or `RuntimeException`. `OutOfMemoryError` territory is the VM, not an order-service failure.

> [!tip] Interview answer
> **Extend `RuntimeException` when the caller cannot reasonably recover — a programming error or a broken contract — so you do not force `throws`.** If the caller should handle a recoverable condition, extend `Exception`. Do not use `RuntimeException` only to avoid the compiler, and do not extend `Error` for application failures.
