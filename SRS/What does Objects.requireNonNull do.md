<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS

# What does `Objects.requireNonNull` do?

> [!abstract] Short answer
> **It fail-fasts on `null`.** `Objects.requireNonNull(obj)` throws `NullPointerException` if the reference is `null`; otherwise it **returns the same reference**. The message and `Supplier<String>` overloads do the same check with a detail string. It is the usual JDK parameter check. It never throws `IllegalArgumentException`.

## Check, then return for assignment

`Objects.requireNonNull` is built for validating parameters in methods and constructors. If `obj` is non-null, the result is `obj`, so this compiles and documents the contract:

`this.name = Objects.requireNonNull(name, "name");`

If `obj` is `null`, it throws `NullPointerException` (optionally with your message). That is unchecked: no `throws` is required ([[What is NullPointerException]], [[Must you declare RuntimeException in a throws clause]], [[How do you prevent a NullPointerException]]).

Overloads:

- `requireNonNull(T obj)` — no message
- `requireNonNull(T obj, String message)` — message used if `obj` is null
- `requireNonNull(T obj, Supplier<String> messageSupplier)` — the supplier runs **only** if the check fails, so you do not build a string on the success path

`requireNonNullElse` / `requireNonNullElseGet` are different: they **return a fallback** instead of throwing when the first argument is null (the fallback itself must be non-null) ([[How do you avoid NullPointerException when unboxing a Map value]]).

```d2
direction: down
in: "requireNonNull(obj)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
ok: "return obj" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
npe: "NullPointerException" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
in -> ok
in -> npe
```

**Fig. 1.** Same reference or NPE. Not `IllegalArgumentException`.

```java
import java.util.Objects;

class Demo {
    private final String name;

    Demo(String name) {
        this.name = Objects.requireNonNull(name, "name");
    }

    static String label(String s) {
        return Objects.requireNonNullElse(s, "");
    }
}
```

**Listing 1.** Constructor fails fast on `null`. `label` substitutes `""` instead of throwing. Prefer this over `assert name != null` for public arguments ([[Why should you not use assert to validate public method arguments]], [[Should you throw NullPointerException or IllegalArgumentException for a null argument]]).

The NPE is constructed in Java code (`new NullPointerException(...)`), so Java 14’s JVM bytecode “helpful NPE” text does not apply to this throw. The stack frame and your message are the diagnosis ([[What did Java 14 change about NullPointerException messages]]).

> [!warning] It is NPE, not `IllegalArgumentException`
> House style that uses `IAE` for every bad argument will look inconsistent next to `requireNonNull`. The method’s contract is `NullPointerException` only.

> [!warning] `requireNonNullElse` does not fail fast
> `requireNonNullElse(map.get(k), 0)` treats missing-or-null as a default. That is coalescing, not a null-forbidden API. If both arguments are null, that method throws NPE because the fallback must be non-null.

> [!tip] Interview answer
> **`Objects.requireNonNull(x)` throws `NullPointerException` if `x` is null and otherwise returns `x`, so you can assign it in a constructor.** Use the message overload to name the parameter. `requireNonNullElse` returns a default instead of throwing. It is never `IllegalArgumentException`.
