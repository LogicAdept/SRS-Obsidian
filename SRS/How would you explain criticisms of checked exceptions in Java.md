<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/Exceptions/Unchecked #SRS

# How would you explain criticisms of checked exceptions in Java?

> [!abstract] Short answer
> **Catch-or-specify is a compile-time contract: every checked exception must be `catch`ed or named in `throws`.** Critics call that signature noise, a poor fit for interfaces and lambdas, and a push toward empty `catch`, `catch (Exception)`, or wrap-in-`RuntimeException`. The language’s own answer is still recoverability — not “make everything unchecked to skip `throws`.”

## What the rule costs, and why it exists

A method that can throw a checked exception must handle it or declare it. That `throws` list is part of the **contract** with callers. Callers who cannot recover must declare it too, so `IOException` (and similar) tends to appear on many layers ([[What happens if you neither catch nor declare a checked exception]], [[How can you avoid being forced to handle checked IOException]], [[How do you handle exceptions in Java applications]]).

That is the usual criticism: **boilerplate and leaky `throws`**. An override cannot add a checked type the parent did not declare, so an adapter that hits I/O must wrap or catch inside ([[How do checked exceptions work with method overriding]]). A lambda whose target type has no matching `throws` cannot let a checked exception out ([[Can a lambda throw a checked exception]]).

People then **sidestep** the rule: empty `catch`, `catch (Exception e)`, or wrap in `RuntimeException` / `UncheckedIOException` so callers see no checked type ([[Does wrapping a checked exception in RuntimeException require a throws clause]], [[When should a custom exception extend RuntimeException]], [[Can you create a custom exception that extends RuntimeException]]). Wrapping keeps the cause; it does not make the failure disappear. Empty `catch` compiles and is not recovery.

The designers already refused to apply catch-or-specify to **every** throwable. `Error` would clutter `throws` pointlessly. `RuntimeException` is exempt because many operations can throw it and the compiler cannot prove (for example) that a `NullPointerException` cannot occur, even when the programmer knows a structure is never null. Forcing those onto every method would be an **irritation**, not a proof of correctness.

The remaining official split: if the **client can reasonably recover**, use checked; if not, use unchecked. Do not subclass `RuntimeException` only to avoid specifying exceptions ([[How do you define your own exception class in Java]]).

```d2
direction: down
chk: "checked IOException" {
  width: 280
  height: 50
}
spec: "throws all the way up" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
escape: "wrap / catch Exception\n(sidesteps specify)" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
chk -> spec
chk -> escape
```

**Fig. 1.** The controversy is the cost of `throws` versus the workarounds that dodge it.

```java
class Demo {
    static String specify(java.nio.file.Path p) throws java.io.IOException {
        return java.nio.file.Files.readString(p);
    }

    static String wrap(java.nio.file.Path p) {
        try {
            return java.nio.file.Files.readString(p);
        } catch (java.io.IOException e) {
            throw new java.io.UncheckedIOException(e);
        }
    }
}
```

**Listing 1.** `specify` is catch-or-specify. `wrap` is the common escape — callers need no `throws IOException`. The tutorial treats “unchecked only so I need not specify” as skipping the intent of the rule.

> [!warning] “Everything should be unchecked” is not the platform rule
> Recoverability still decides checked vs `RuntimeException`. Wrapping is a boundary translation, not a license to invent `Error` types or to swallow.

> [!warning] `catch (Exception)` is the other dodge
> It satisfies the compiler and also swallows `RuntimeException`. That is a handling bug, not a fix for signature clutter.

> [!tip] Interview answer
> **Critics say checked exceptions force `throws` up the stack, fight interfaces and lambdas, and tempt empty catches or wrappers.** Java still wants checked when the caller can recover. Unchecked exists because declaring every `RuntimeException` or `Error` would not make programs more correct — it would just irritate.
