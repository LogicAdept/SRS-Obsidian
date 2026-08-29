<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS

# Should you throw `NullPointerException` or `IllegalArgumentException` for a null argument?

> [!abstract] Short answer
> **Prefer `NullPointerException` for a forbidden `null` argument.** That is what `Objects.requireNonNull` throws, and it matches “illegal use of `null`.” Use `IllegalArgumentException` for a non-null argument that is still wrong (empty string, negative count, unsupported enum). Throwing `IAE` for `null` is legal; it is just not the JDK parameter-validation idiom.

## `null` is an NPE; other bad values are IAE

`NullPointerException` is thrown when code uses `null` where an object is required. Applications are also expected to throw it for other illegal uses of `null` ([[What is NullPointerException]], [[How do you prevent a NullPointerException]]). `Objects.requireNonNull(arg)` (and the overloads with a message) exist for **parameter validation** and always throw `NPE`, never `IAE` ([[What does Objects.requireNonNull do]]).

`IllegalArgumentException` means the method received an illegal or inappropriate argument. That covers values that are present but invalid. It is the usual type for “this `int` must be ≥ 0,” not for “this reference must not be null” ([[What is the difference between IllegalArgumentException and IllegalStateException]]).

Both types are unchecked `RuntimeException`s: no `throws` is required ([[Must you declare RuntimeException in a throws clause]], [[Can you catch an unchecked exception in Java]]). Do not use `assert` to validate public arguments ([[Why should you not use assert to validate public method arguments]]).

```d2
direction: down
arg: "incoming argument" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
npe: "null where object required\nNullPointerException" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
iae: "non-null but illegal value\nIllegalArgumentException" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
arg -> npe
arg -> iae
```

**Fig. 1.** Split by *kind* of bad argument: missing object vs wrong value.

```java
import java.util.Objects;

class Demo {
    static void greet(String name) {
        Objects.requireNonNull(name, "name");
        System.out.println(name.length());
    }

    static void times(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("n < 0: " + n);
        }
    }
}
```

**Listing 1.** `greet` fails on `null` with `NPE`. `times` fails on a present but illegal `int` with `IAE`.

> [!warning] `requireNonNull` is never `IAE`
> `Objects.requireNonNull` documents that it throws `NullPointerException` if the reference is `null`. Wrapping that in `catch` and rethrowing `IAE` only confuses callers who already expect NPE from JDK-style APIs.

> [!warning] `IAE` for `null` is not a compile error
> Some codebases throw `IllegalArgumentException("name is null")`. That is a consistent house rule, not a language rule. Interview answers that follow the JDK helpers still pick **NPE for null** and **IAE for other illegal values**.

> [!tip] Interview answer
> **Throw `NullPointerException` for a forbidden null argument — typically `Objects.requireNonNull`.** Use `IllegalArgumentException` when the argument is present but still illegal. Both are unchecked; `requireNonNull` never throws `IAE`.
