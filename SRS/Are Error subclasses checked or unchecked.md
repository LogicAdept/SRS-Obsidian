<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/Exceptions/Checked #Java/Exceptions/Unchecked #SRS

# Are `Error` subclasses checked or unchecked?

> [!abstract] Short answer
> **Unchecked.** `Error` and every subclass (`OutOfMemoryError`, `StackOverflowError`, `VirtualMachineError`, `AssertionError`, …) are **error classes**: the compiler does not require `catch` or `throws` for them, the same compile-time rule as for `RuntimeException`.

## Where they sit in the hierarchy

```d2
direction: down
Throwable: "Throwable" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
Error: "Error\n(error classes → unchecked)" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
Exception: "Exception" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
Runtime: "RuntimeException\n(run-time → unchecked)" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
Checked: "other Exception subclasses\n(checked)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
Throwable -> Error
Throwable -> Exception
Exception -> Runtime
Exception -> Checked
```

**Fig. 1.** Unchecked = error classes **or** run-time exception classes; everything else under `Throwable` is checked (including `Throwable` and `Exception` themselves).

JLS: the **unchecked** exception classes are the run-time exception classes (`RuntimeException` and subclasses) **and** the error classes (`Error` and subclasses). Checked classes are `Throwable` and all other subclasses outside those two trees. Java SE `Error` API: a method need not declare subclasses of `Error` in `throws` — they are regarded as unchecked for compile-time checking.

```java
void mayFail() {
    // no throws needed for Error or RuntimeException
    if (Math.random() < 0) {
        throw new AssertionError("unreachable");
    }
    throw new OutOfMemoryError("demo");
}

void caller() {
    mayFail(); // compiles: Error is unchecked
}
```

**Listing 1.** Throwing or propagating `Error` subclasses does not force a `throws` clause.

## Checked means the other branch

Checked types are **not** “everything under `Exception`.” They are every `Throwable` subtype **except** `RuntimeException`/`Error` and their children. Typical checked examples: `IOException`, `SQLException`. `catch (Exception e)` deliberately **misses** `Error` — that is why `Error` is a sibling of `Exception`, not a child. See [[What is the difference between RuntimeException and Error]] and [[Why is Error a sibling of Exception rather than a subclass]].

```java
try {
    mayFail();
} catch (Exception e) {
    // does not catch OutOfMemoryError / AssertionError
} catch (Error e) {
    // legal; API still advises ordinary apps not to recover from most Errors
}
```

**Listing 2.** Language allows `catch (Error)`; it is not the same as “must declare `throws Error`.”

> [!warning] Unchecked ≠ RuntimeException-only
> Interview shorthand that “unchecked = `RuntimeException`” is incomplete. **`Error` is unchecked and is not a `RuntimeException`.** `catch (RuntimeException e)` never sees an `Error`.

> [!warning] “Error cannot be caught”
> False as a language rule. You may write `catch (Error)` or `catch (Throwable)`. The platform guidance is that a **reasonable application should not try to catch** most `Error`s because recovery is usually not possible — that is advice, not a compile-time ban.

> [!tip] Interview answer
> **`Error` and its subclasses are unchecked — same compile-time exemption as `RuntimeException`: no required `catch`/`throws`. They are siblings of `Exception` under `Throwable`, so they are not runtime exceptions. Checked exceptions are the remaining `Throwable` types outside those two unchecked trees.**
