<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #Java/Exceptions/Checked #SRS

# How would you explain Java exception handling try catch and propagation?

> [!abstract] Short answer
> **`throw` completes the current work abruptly. The JVM looks for the innermost matching `catch`. A match runs that handler and does not resume the `try`. No match means the exception leaves the method — that is propagation — after any `finally` runs.** Checked types must be caught or declared; unchecked types may propagate with no `throws`.

## Catch handles here; otherwise the caller sees the throw

A `try` statement groups work that may complete abruptly. Each `catch` names a type. The first clause whose type is the thrown object’s class or a superclass runs; later clauses are skipped. Control never returns to the rest of the `try` ([[Does control return to the try block after a catch handles an exception]], [[How would you catch an exception in your application]]).

If no clause matches, the `try` statement itself completes abruptly with the same exception. That is **propagation**: the throw is re-raised at the call site, then the caller’s `try` statements are searched, and so on ([[How do you propagate an exception up the call stack in Java]]). A `finally` on the way out still runs. A plain `try` needs `catch`, `finally`, or a resource list ([[Can a try block exist without a catch in Java]]).

**Catch-or-specify** applies to checked exceptions (`Exception` minus `RuntimeException`): catch them, or list them in `throws` so callers must do the same. Unchecked exceptions (`RuntimeException`, `Error`) may propagate with no declaration. If nothing on the stack catches the throw, the thread’s uncaught-exception handler runs ([[What happens if you neither catch nor declare a checked exception]], [[Can main throw exceptions outward and where are they handled]]).

```d2
direction: down
throw: "throw in try" {
  width: 240
  height: 50
}
match: "matching catch?" {
  width: 260
  height: 50
}
handle: "run catch\nthen after try" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
prop: "propagate to caller\n(finally still runs)" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
throw -> match
match -> handle: "yes"
match -> prop: "no"
```

**Fig. 1.** Matching `catch` stops the search. Otherwise the exception leaves the method.

```java
class Demo {
    static void inner() throws java.io.IOException {
        throw new java.io.IOException("fail");
    }

    static void outer() {
        try {
            inner();
        } catch (java.io.IOException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

**Listing 1.** `inner` propagates a checked exception with `throws`. `outer` stops it with a matching `catch`.

> [!warning] `catch (Exception e)` is a wide net
> It satisfies checked types under `Exception`, and it also swallows `RuntimeException`. Prefer the type you can actually recover from.

> [!warning] `finally` can hide the original throw
> If `finally` throws or `return`s, that completion replaces the exception that was propagating.

> [!tip] Interview answer
> **`try`/`catch` is the local handler: the first matching `catch` runs, and the rest of the `try` is skipped.** If nothing matches, the exception **propagates** to the caller after `finally`. Checked exceptions must be caught or declared; unchecked ones may travel with no `throws`.
