<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/Exceptions/TryCatch #SRS

# If calling method A will throw an exception what should you do?

> [!abstract] Short answer
> **If A’s exception is checked, you must `catch` it or declare `throws` — the compiler will not compile a third option.** Catch only if this method can recover. Otherwise propagate with `throws` so the caller decides. Unchecked exceptions (`RuntimeException`) do not require that choice; catching them is optional and should still be a real recovery.

## Catch if you can recover; otherwise specify

Calling A can throw whatever A’s `throws` clause (and body) allow. For a **checked** type, this method is in the catch-or-specify rule: a matching `catch`, or `throws` naming that class or a superclass ([[What happens if you neither catch nor declare a checked exception]], [[How would you explain the throws clause for checked exceptions]], [[How would you explain Java exception handling try catch and propagation]]).

**Catch here** when this layer can do something useful: retry, a fallback, a user-facing message, close a resource. Prefer the actual type A throws, not `Exception`, so you do not swallow `RuntimeException` ([[How would you catch an exception in your application]], [[How do you handle exceptions in Java applications]], [[How should you throw and handle exceptions in Java]]).

**Propagate** when this method has no policy: `throws` the same type (or a documented wrapper). Wrapping in `RuntimeException` is a different contract — callers then cannot `catch` the original checked type ([[How do you propagate an exception up the call stack in Java]], [[Does wrapping a checked exception in RuntimeException require a throws clause]]).

If A throws only an unchecked type, the compiler does not force a `catch`. You still may catch it if recovery is real ([[Can you catch an unchecked exception in Java]]). Do not catch `Error` as a way to “handle” A ([[Why should you not catch java.lang.Error]]).

```d2
direction: down
call: "call A" {
  width: 240
  height: 50
}
kind: "checked?" {
  width: 240
  height: 50
}
must: "catch or throws" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
opt: "catch only if you recover" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
call -> kind
kind -> must: "yes"
kind -> opt: "no"
```

**Fig. 1.** The compiler only forces a decision for checked exceptions. Recovery is still the real test.

```java
class Demo {
    static void mustDeal() throws java.io.IOException {
        java.nio.file.Files.readString(java.nio.file.Path.of("x"));
    }

    static String recover() {
        try {
            return java.nio.file.Files.readString(java.nio.file.Path.of("x"));
        } catch (java.io.IOException e) {
            return "";
        }
    }
}
```

**Listing 1.** `mustDeal` specifies. `recover` handles. An empty `catch` with no fallback would be the wrong third option.

> [!warning] Empty `catch (Exception e) {}` is not “handling”
> The compiler is satisfied. The failure is gone. Callers cannot retry or log the real type.

> [!warning] Do not add `throws` only to avoid thinking
> `throws Exception` on every method pushes the problem to `main` and hides which failures are expected.

> [!tip] Interview answer
> **If A throws a checked exception, catch it when this method can recover; otherwise declare `throws`.** There is no legal third path for checked types. Unchecked exceptions do not need `throws`, but you still catch them only when you have a real response.
