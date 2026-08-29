<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/Exceptions/Hierarchy #SRS

# What is `java.lang.Error`?

> [!abstract] Short answer
> **`Error` is a direct subclass of `Throwable` and a sibling of `Exception`.** It marks serious problems a reasonable application should not try to catch. Typical examples: `OutOfMemoryError`, `StackOverflowError`, `VirtualMachineError`, `AssertionError`. It is **unchecked**: no `throws` clause is required.

## Sibling of `Exception`, not a recoverable `Exception`

`Throwable` has two usual branches. `Exception` is for conditions ordinary programs may recover from. `Error` is the superclass of conditions they are **not** ordinarily expected to recover from. That split is why `catch (Exception e)` does not catch `Error` ([[Does catch Exception also catch Error]], [[Why is Error a sibling of Exception rather than a subclass]], [[What is the difference between java.lang.Error and java.lang.Exception]]).

`Error` and all its subclasses are unchecked, together with `RuntimeException`. A method need not declare `throws Error`. Catching `Error` (or `Throwable`) is still legal; the API and language still tell you not to treat it as a normal recovery path ([[Are Error subclasses checked or unchecked]], [[Can you catch and handle java.lang.Error like normal exceptions]], [[Why should you not catch java.lang.Error]]).

`VirtualMachineError` covers resource limits such as stack overflow and heap exhaustion. `AssertionError` is also an `Error`, not an `Exception` ([[What is VirtualMachineError]], [[How do you produce a StackOverflowError]], [[Is AssertionError a subclass of Exception]]).

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
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
vme: VirtualMachineError {
  width: 220
  height: 40
  style.fill: "#ffebee"
}
ae: AssertionError {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
throwable -> ex
throwable -> err
ex -> rte
err -> vme
err -> ae
```

**Fig. 1.** `Error` sits beside `Exception` under `Throwable`.

```java
class Demo {
    static void mayFail() {
        throw new OutOfMemoryError("simulated");
    }

    static void catcher() {
        try {
            mayFail();
        } catch (Exception e) {
            // does not run for Error
        } catch (Error e) {
            // legal, but not a recovery strategy
        }
    }
}
```

**Listing 1.** `mayFail` needs no `throws`. `catch (Exception)` misses `Error`; `catch (Error)` compiles. `OutOfMemoryError` here is only to show the type — a real OOME means the VM is already in trouble.

> [!warning] Legal to catch ≠ meant to recover
> `catch (Error e)` compiles. Dumps still treat `Error` as abnormal. Swallowing `OutOfMemoryError` or `StackOverflowError` hides a broken VM, not a business failure.

> [!warning] `catch (Exception)` is not “everything throwable”
> `Error` is not a subclass of `Exception`. Interview snippets that “handle all failures” with `catch (Exception)` leave the `Error` branch uncaught ([[Does catch Exception also catch Error]]).

> [!tip] Interview answer
> **`Error` is a `Throwable` sibling of `Exception` for serious problems a reasonable app should not catch.** Examples are `OutOfMemoryError`, `StackOverflowError`, and `AssertionError`. It is unchecked — no `throws` — and `catch (Exception)` does not catch it.
