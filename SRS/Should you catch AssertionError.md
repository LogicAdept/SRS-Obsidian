<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #Java/Exceptions/Error #SRS

# Should you catch `AssertionError`?

> [!abstract] Short answer
> **You can, but you should not.** `AssertionError` extends `Error` and is unchecked, so a `catch` compiles. A failed `assert` means a programmer invariant is already false; catching it hides that and lets the method continue in a broken state. `catch (Exception e)` does not catch it.

## Legal to catch, intended not to

`AssertionError` is an `Error`, not an `Exception`. It is unchecked: no `throws` is required. Any `Error` may be caught the same way as an unchecked exception — that is allowed, not encouraged ([[Is AssertionError a subclass of Exception]], [[Are Error subclasses checked or unchecked]], [[Can you catch an unchecked exception in Java]], [[Can you catch and handle java.lang.Error like normal exceptions]]).

A failed enabled `assert` completes by throwing a new `AssertionError`. That is meant to abort the path that depended on the boolean being true, not to be a handled condition ([[What happens when a Java assert statement fails]], [[What is the purpose of the assert keyword in Java]]). If assertions are disabled, the `assert` does nothing and there is nothing to catch ([[How do you enable Java assertions at runtime]], [[Why are Java assertions disabled by default]]).

```d2
direction: down
fail: "assert cond : msg\n(cond is false)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
ae: "AssertionError" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
ok: "propagate (intended)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
bad: "catch and continue\nhides a broken invariant" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
fail -> ae
ae -> ok
ae -> bad
```

**Fig. 1.** Catching `AssertionError` is possible; continuing afterward is the defect.

```java
class Demo {
    static void notRecommended(int x) {
        try {
            assert x > 10 : x;
        } catch (AssertionError e) {
            System.out.println("caught — still running");
        }
    }

    static void intended(int x) {
        assert x > 10 : x;
    }
}
```

**Listing 1.** `notRecommended` compiles and, with assertions on, prints then proceeds. `intended` lets the error stop the caller. `catch (Exception e)` around either method would miss `AssertionError` entirely ([[Does catch Exception also catch Error]]).

Do not use `assert` for public-argument checks you then “handle”; that is the wrong tool and the wrong throwable ([[Why should you not use assert to validate public method arguments]], [[When is it appropriate to use Java assertions]]).

> [!warning] Catching it can hide a failed invariant
> After `assert` fails, the rest of the method assumed `x > 10`. Swallowing `AssertionError` and continuing uses that bad state. The same reason you should not casually catch `Error` applies here ([[Why should you not catch java.lang.Error]]).

> [!warning] Interview wording may say “exception”
> The hierarchy type is `Error`. A `try` that only catches `Exception` will not see a failed `assert`. Saying you “caught the assertion exception” is the wrong name and often the wrong `catch`.

> [!tip] Interview answer
> **It is legal because `AssertionError` is an unchecked `Error`, but you should not catch it.** A failed `assert` means an invariant is already false; catching it lets the program limp on. `catch (Exception)` will not see it.
