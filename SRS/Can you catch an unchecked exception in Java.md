<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Exceptions/TryCatch #SRS

# Can you catch an unchecked exception in Java?

> [!abstract] Short answer
> **Yes.** Unchecked means the compiler does **not require** a `catch` or `throws` — not that `catch` is illegal. `catch (RuntimeException e)`, `catch (NullPointerException e)`, and `catch (Error e)` are all valid. Catching is optional; it is not forbidden.

## Optional handler, not a banned handler

The unchecked classes are the run-time exception classes (`RuntimeException` and subclasses) and the error classes (`Error` and subclasses). They are exempt from compile-time exception checking: a method need not declare them, and a caller need not catch them ([[Must you declare RuntimeException in a throws clause]], [[Are Error subclasses checked or unchecked]]).

A `catch` clause may name `Throwable` or any subclass. Matching at run time is assignment compatibility: the first `catch` whose type is the thrown object's class or a superclass of it handles the throw. That rule does not distinguish checked from unchecked.

The “unreachable catch” rule applies to **checked** types (with `Exception` and its superclasses carved out). You may `catch (NullPointerException)` around a `try` that the compiler does not treat as throwing NPE. The same pattern with `IOException` is often a compile-time error.

```d2
direction: down
throw: "throw / NPE / CCE / Error" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
compile: "throws / catch not required" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
catch: "catch still legal\nand does run if types match" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
throw -> compile
throw -> catch
```

**Fig. 1.** Unchecked exemption is about *obligation*, not about whether a `catch` may appear. See [[Is RuntimeException a subclass of Exception]].

```java
class Demo {
    static int parseOrZero(String s) {
        try {
            return Integer.parseInt(s);
        } catch (NumberFormatException e) {
            return 0;
        }
    }

    static void catchEvenIfUnlikely() {
        try {
            System.out.println("ok");
        } catch (NullPointerException e) {
            // compiles: NPE is unchecked
        }
    }
}
```

**Listing 1.** Specific unchecked `catch` is legal. `parseOrZero` recovers from a well-known conversion failure; that is a real handler, not a required one.

> [!warning] `catch (Exception e)` also takes `RuntimeException`
> `RuntimeException` is a subclass of `Exception`. A handler written for I/O or other checked types will also swallow `NullPointerException`, `IllegalArgumentException`, and the rest of the run-time tree. Catch the most specific type you mean to handle. See [[Does catch Exception also catch RuntimeException]]. It still **misses** `Error` — [[Can you catch and handle java.lang.Error like normal exceptions]], [[Can you catch Throwable]].

> [!warning] Optional is not “must swallow”
> A `catch` that logs and continues after an unexpected NPE hides the bug. Recovery can be appropriate (`NumberFormatException` on user input). Empty `catch (Exception ignored)` is legal and usually wrong. Error classes remain catchable; the platform still treats most of them as conditions ordinary code should not try to recover from.

> [!tip] Interview answer
> **Yes — you can catch unchecked exceptions; “unchecked” only means the compiler does not force `catch` or `throws`. `catch (RuntimeException)` or `catch (NullPointerException)` is valid. `catch (Exception)` also matches those types, which is how a broad handler accidentally swallows an NPE.**
