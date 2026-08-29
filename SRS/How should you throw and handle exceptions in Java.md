<!--
reps: 0
priority: 0
-->
#Java/Exceptions #SRS

# How should you throw and handle exceptions in Java?

> [!abstract] Short answer
> **Throw a specific `Throwable` that names the failure; catch only what you can recover from.** Use `throw` with an `Exception` (checked if the client can recover, `RuntimeException` if not). Do not throw `Error` for application problems. Handle with specific `catch` types, `throws`, or a wrap-with-cause — not `catch (Exception)` / `catch (Throwable)` as a default.

## Throw a real type, then catch-or-specify

Only `Throwable` instances can be thrown. `throw` evaluates its operand; if that value is `null`, a `NullPointerException` is thrown instead ([[Can you throw an object that is not a Throwable]], [[What information does a Throwable carry]]).

Throw **`Exception`** subtypes for application failures. The VM throws **`Error`** for linking and other hard failures; ordinary programs typically neither throw nor catch `Error` ([[Why should you not catch java.lang.Error]], [[Can you catch Throwable]]).

Pick the branch by **recoverability**: if the caller can reasonably recover, use a checked type (`extends Exception`, not `RuntimeException`) and `throws` or `catch`. If they cannot, use unchecked (`RuntimeException` or a subclass such as `IllegalArgumentException` / `EmptyStackException`) ([[When should a custom exception extend RuntimeException]], [[How do you define your own exception class in Java]], [[Should you throw NullPointerException or IllegalArgumentException for a null argument]]). A new type is for a failure the platform types do not already name — constructors should pass message and **cause** to `super`.

**Handle** at the layer that can fix it: a matching `catch`, try-with-resources / `finally` for cleanup, or propagate with `throws`. Wrapping a checked exception in a `RuntimeException` (cause set) is how a boundary stops declaring `throws` without losing the original ([[How do you handle exceptions in Java applications]], [[How do you propagate an exception up the call stack in Java]], [[Does wrapping a checked exception in RuntimeException require a throws clause]]). Catch the **specific** types you handle. `catch (Exception e)` also takes `RuntimeException`; `catch (Throwable t)` also takes `Error`.

```d2
direction: down
fail: "failure in your code" {
  width: 280
  height: 50
}
thr: "throw specific Exception" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
err: "do not throw Error" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
hnd: "catch specific / throws / wrap" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
fail -> thr -> hnd
fail -> err
```

**Fig. 1.** Application code throws `Exception` types. Handling is specific catch, declaration, or wrap — not a catch-all.

```java
class Demo {
    static Object pop(int size, Object[] stack) {
        if (size == 0) {
            throw new java.util.EmptyStackException();
        }
        return stack[size - 1];
    }

    static String read(java.nio.file.Path p) {
        try {
            return java.nio.file.Files.readString(p);
        } catch (java.io.IOException e) {
            throw new java.io.UncheckedIOException(e);
        }
    }
}
```

**Listing 1.** `pop` throws a specific unchecked type (no `throws`). `read` cannot recover from I/O here, so it wraps with cause instead of an empty `catch` or `catch (Exception e)`.

> [!warning] `throw null` is a `NullPointerException`
> You cannot throw the null reference. The language throws NPE. Always `throw new SomeException("why")` (and a cause when wrapping).

> [!warning] Do not throw or catch `Error` as API design
> `Error` is for VM/system failure. Catching `Throwable` to “never crash” hides OOM. Swallowing with an empty `catch` is not handling.

> [!tip] Interview answer
> **Throw a specific exception that describes the problem — checked if the caller can recover, unchecked if not — and never `Error` for business logic.** Handle with a matching `catch`, `throws`, or wrap with a cause. Catch-all `Exception` or `Throwable` is the wrong default.
