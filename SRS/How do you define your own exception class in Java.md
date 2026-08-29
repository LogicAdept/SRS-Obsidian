<!--
reps: 0
priority: 0
-->
#Java/Exceptions #SRS

# How do you define your own exception class in Java?

> [!abstract] Short answer
> **Subclass `Exception` (checked) or `RuntimeException` (unchecked), name it `…Exception`, and add constructors that call `super` with a message and/or cause.** Use a new type when the platform types do not say what failed. Do not extend `Error` for application failures.

## Pick a superclass, then delegate to `Throwable`

Write your own class if you need a type the Java SE API does not already provide, if callers should distinguish your failures from other libraries, or if related failures should share a package-level parent ([[What are common examples of checked exceptions in Java]], [[What information does a Throwable carry]]).

- **`extends Exception`** (and not `RuntimeException`) → **checked**. Callers must `catch` or declare `throws`. Typical when the client can recover.
- **`extends RuntimeException`** → **unchecked**. No `throws` required. Typical when the client cannot reasonably recover ([[Can you create a custom exception that extends RuntimeException]], [[When should a custom exception extend RuntimeException]], [[Is RuntimeException a subclass of Exception]], [[What is RuntimeException]]).

`Error` is for serious VM or system failure, not domain errors ([[Why should you not catch java.lang.Error]]). Wrapping another throwable is done by passing it as the **cause** ([[Does wrapping a checked exception in RuntimeException require a throws clause]]).

Append `Exception` to the class name. Provide at least message and message+cause constructors that call `super(...)` so `getMessage()`, `getCause()`, and the stack trace stay those of `Throwable`. You do not override `printStackTrace` to invent a type.

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
}
chk: "YourCheckedException" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
unc: "YourUncheckedException" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
err: "Error (not for domain types)" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
th -> ex
th -> err
ex -> rte
ex -> chk
rte -> unc
```

**Fig. 1.** Custom types hang under `Exception` or `RuntimeException`, not under `Error`.

```java
class InvalidOrderException extends Exception {
    InvalidOrderException(String message) {
        super(message);
    }

    InvalidOrderException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

**Listing 1.** A checked custom exception. Change the superclass to `RuntimeException` for an unchecked type with the same constructors. `throw new InvalidOrderException("empty cart")` then follows the usual catch-or-specify rules for that branch.

> [!warning] Empty subclasses are still a choice of checked vs unchecked
> `class MyEx extends Exception {}` is legal and checked. The constructors you omit are the ones callers cannot use (`new MyEx("msg")` needs a matching constructor).

> [!warning] Reuse first
> Prefer `IllegalArgumentException`, `IOException`, or `IllegalStateException` when they already match. A new class is for a **new** failure kind, not a new name for `RuntimeException`.

> [!tip] Interview answer
> **Extend `Exception` or `RuntimeException`, name it `SomethingException`, and pass message and cause to `super`.** Checked vs unchecked is the superclass you pick. Do not extend `Error` for business errors.
