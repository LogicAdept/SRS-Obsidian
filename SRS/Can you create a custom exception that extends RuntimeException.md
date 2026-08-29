<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Exceptions/Checked #SRS

# Can you create a custom exception that extends `RuntimeException`?

> [!abstract] Short answer
> **Yes.** `RuntimeException` is an ordinary class; a subclass is an **unchecked** exception. Callers need not `catch` or declare it. Extend `RuntimeException` when the client cannot reasonably recover. Do not extend it only to skip `throws`, and do not extend `Error` for application failures.

## A subclass is still unchecked

Any new class that extends `RuntimeException` (directly or indirectly) is an unchecked exception class. `throw new MyUnchecked(...)` compiles without `throws MyUnchecked` on the method ([[What is RuntimeException]], [[Must you declare RuntimeException in a throws clause]], [[Is RuntimeException a subclass of Exception]]). It is still an `Exception`, so `catch (Exception e)` will catch it; `catch (Error e)` will not.

You may instead extend `Exception` (not `RuntimeException`) to make a **checked** type: callers must `catch` or declare it. The documented split is recoverability, not fashion: if the client can reasonably recover, use checked; if not, use unchecked ([[When should a custom exception extend RuntimeException]]). Skipping `throws` is a **consequence** of unchecked, not the reason to pick `RuntimeException`.

`Error` is for serious VM or system failure. Application code should not invent business `Error` types ([[Why should you not catch java.lang.Error]], [[Are Error subclasses checked or unchecked]]). Wrapping a checked exception in a custom `RuntimeException` also removes the `throws` obligation ([[Does wrapping a checked exception in RuntimeException require a throws clause]]).

Name the type `…Exception`. Provide constructors that delegate to `super` (message, cause, or both) so the stack and cause chain stay intact.

```d2
direction: down
th: "Throwable" {
  width: 200
  height: 40
}
ex: "Exception" {
  width: 200
  height: 40
}
rte: "RuntimeException" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
mine: "YourUncheckedException" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
err: "Error (not for business)" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
th -> ex
th -> err
ex -> rte
rte -> mine
```

**Fig. 1.** A custom unchecked type hangs under `RuntimeException`, not under `Error`.

```java
class InvalidOrderException extends RuntimeException {
    InvalidOrderException(String message) {
        super(message);
    }

    InvalidOrderException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

**Listing 1.** A legal custom unchecked exception. Methods that `throw new InvalidOrderException(...)` need no `throws` clause. Extending `Exception` instead would make the same shape **checked**.

> [!warning] Unchecked is not a license to skip design
> Extending `RuntimeException` so callers never write `throws` is allowed, but the language’s criterion is whether recovery is reasonable — not whether signatures look cleaner.

> [!warning] Do not extend `Error` for domain failures
> `Error` is the VM/system branch. A custom `Error` is still an `Error`: `catch (Exception e)` misses it, and clients are not expected to recover.

> [!tip] Interview answer
> **Yes — extend `RuntimeException` and you have a custom unchecked exception; no `throws` needed.** Use that when the caller cannot recover. If they can, extend `Exception` instead. Do not extend `Error` for business errors.
