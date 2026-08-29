<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Language/Assert #SRS

# What is the difference between an exception and a validation error?

> [!abstract] Short answer
> **Java has exceptions (`Throwable`). It does not have a separate “validation error” type.** A bad argument to a method is still an exception — usually unchecked `IllegalArgumentException` or `NullPointerException`. A form that collects field messages is an application pattern, not a second JVM mechanism.

## Contract failures are still exceptions

An exception is an object used for a non-local transfer of control when a semantic constraint fails ([[How would you explain exception]], [[How should you throw and handle exceptions in Java]]). “Validation error” is interview wording, not a class in `java.lang`.

**Method-contract validation** in the JDK **is** throwing:

- `NullPointerException` for a forbidden `null` (`Objects.requireNonNull`)
- `IllegalArgumentException` for a non-null value that is still illegal
- `IllegalStateException` when the object is not in a state to accept the call

Those are unchecked. Callers are not forced to `catch` them ([[Should you throw NullPointerException or IllegalArgumentException for a null argument]], [[What is the difference between IllegalArgumentException and IllegalStateException]], [[What does Objects.requireNonNull do]]).

**`assert`** is not that channel. Assertions may be disabled; they must not be the only check on a public argument ([[Why should you not use assert to validate public method arguments]]).

**Recoverable I/O or JDBC** is a different story: checked `IOException` / `SQLException` when the caller can retry or degrade — not “the user typed a bad email” ([[What are examples where checked exceptions are a good fit]]).

Collecting many field errors and returning them (or a result type) is a **library/UI** choice. It does not replace `throw` for a broken API contract, and it is not a `catch (ValidationError)` built into the language.

```d2
direction: down
bad: "bad value" {
  width: 240
  height: 50
}
api: "public method contract" {
  width: 280
  height: 50
}
ui: "user form / many fields" {
  width: 280
  height: 50
}
iae: "throw IAE / NPE" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
list: "return error list (app)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
bad -> api -> iae
bad -> ui -> list
```

**Fig. 1.** Same English “invalid.” The JDK method contract still `throw`s. A form’s error list is not a language type.

```java
class Demo {
    static void setPort(int port) {
        if (port < 1 || port > 65535) {
            throw new IllegalArgumentException("port");
        }
    }
}
```

**Listing 1.** Out-of-range `port` is a contract failure: `IllegalArgumentException`, not a silent “validation object.”

> [!warning] “Don’t use exceptions for validation” is not a Java SE rule
> The platform validates public arguments by throwing. What you should not do is `assert` on those arguments, or `catch (Exception)` as your validator.

> [!warning] There is no `java.lang.ValidationError`
> A custom `extends RuntimeException` named `ValidationException` is just another unchecked type. It does not change catch-or-specify.

> [!tip] Interview answer
> **An exception is the language’s failure object. “Validation error” is not a second kind of throwable.** Bad method arguments are `IllegalArgumentException` or `NullPointerException`. `assert` is not for public checks. A UI that lists field errors is an application design, not a JVM type.
