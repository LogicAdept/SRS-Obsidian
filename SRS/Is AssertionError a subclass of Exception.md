<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #Java/Exceptions/Hierarchy #Java/Exceptions/Error #SRS

# Is `AssertionError` a subclass of `Exception`?

> [!abstract] Short answer
> **No.** `AssertionError` extends `Error`, not `Exception`. Like other `Error` types it is **unchecked**: you do not declare `throws AssertionError`. A failed `assert` (assertions enabled, condition `false`) throws it. `catch (Exception e)` does not catch it.

## Sibling of `Exception`, under `Error`

`Throwable` has two usual branches: `Exception` and `Error`. `AssertionError` is declared `public class AssertionError extends Error`. It is thrown to indicate that an assertion has failed ([[What is java.lang.Error]], [[Are Error subclasses checked or unchecked]], [[Do checked exceptions inherit Throwable directly]]).

People still call the failure “an exception” in casual speech. The type is an **error**. `catch (Exception e)` therefore misses it; you would need `catch (AssertionError)`, `catch (Error)`, or `catch (Throwable)` — and catching it is generally the wrong idea ([[Does catch Exception also catch Error]], [[Should you catch AssertionError]]).

Because it is an `Error`, a method that throws `new AssertionError(...)` needs no `throws` clause ([[What is the difference between RuntimeException and Error]]).

```d2
direction: down
t: "Throwable" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
ex: "Exception" {
  width: 200
  height: 50
  style.fill: "#eceff1"
}
err: "Error" {
  width: 200
  height: 50
  style.fill: "#fff8e1"
}
ae: "AssertionError" {
  width: 220
  height: 50
  style.fill: "#ffebee"
}
t -> ex
t -> err
err -> ae
```

**Fig. 1.** `AssertionError` is not on the `Exception` branch.

When an enabled `assert` evaluates to `false`, the statement completes abruptly by throwing a newly created `AssertionError` (with the optional detail expression as the message). Disabled asserts do nothing ([[What happens when a Java assert statement fails]], [[What is the purpose of the assert keyword in Java]], [[How do you enable Java assertions at runtime]]).

```java
class Demo {
    static void fail() {
        assert false : "broken";
    }

    static void noThrowsNeeded() {
        throw new AssertionError("manual");
    }

    static void missed() {
        try {
            fail();
        } catch (Exception e) {
            System.out.println("not this");
        }
    }
}
```

**Listing 1.** `noThrowsNeeded` compiles with no `throws`. `missed` does not handle `AssertionError`. `fail` throws only if assertions are enabled.

> [!warning] “Assertion exception” is the wrong name
> Interview dumps often say the JVM “generates an exception `java.lang.AssertionError`.” The class name contains `Error` because it **is** an `Error`. Treating it as a checked `Exception` (or expecting `catch (Exception)` to log it) is a common miss.

> [!warning] It is intended not to be caught
> The language treats a failed assert as a broken programmer assumption, not a recoverable condition. Swallowing `AssertionError` in a `try` hides tests that should abort ([[Why should you not catch java.lang.Error]]).

> [!tip] Interview answer
> **No — `AssertionError` extends `Error`, so it is unchecked and not a subclass of `Exception`.** `catch (Exception)` will not see it. A failed `assert` throws it only when assertions are enabled.
