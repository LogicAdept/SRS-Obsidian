<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# Does control return to the try block after a catch handles an exception?

> [!abstract] Short answer
> **No.** The code that caused the exception is never resumed. The rest of that `try` block is skipped. The first matching `catch` runs, then `finally` if present, then execution continues **after the whole `try` statement**.

## Abrupt completion leaves the `try` block

Throwing completes the `try` block **abruptly**. Control transfers to the nearest enclosing `catch` that can handle the thrown object. Matching is the first (leftmost) `catch` whose type is assignment-compatible with the thrown value. That `catch` block then runs. If it completes normally, the `try` statement completes normally — which means the next statement **after** `try`/`catch`/`finally`, not the next line inside the `try`. See [[How many catch blocks execute for one thrown exception]].

If `finally` is present, it runs after the chosen `catch` (or after the `try` if no `catch` matched), then the same rule applies: a normally completing `finally` lets the `try` statement complete normally, or completes abruptly and discards the prior reason ([[Is a finally block always executed in Java]]).

```d2
direction: down
tryb: "try { a(); throw; b(); }" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
skip: "b() never runs" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
catchb: "first matching catch" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
after: "next statement after\nthe try statement" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
tryb -> skip
tryb -> catchb
catchb -> after
```

**Fig. 1.** Handling an exception does not resume the `try` block. Remaining statements in that block are gone.

```java
class Demo {
    static void work() {
        throw new IllegalStateException("boom");
    }

    static void run() {
        try {
            work();
            System.out.println("not reached");
        } catch (RuntimeException e) {
            System.out.println("caught");
        }
        System.out.println("after try");
    }
}
```

**Listing 1.** Output is `caught` then `after try`. `"not reached"` is skipped. There is no slot to put a statement “between” `catch` and the following code except by placing it after the whole statement ([[Can you place statements between try catch and finally]]).

If no `catch` matches, the rest of the `try` is still skipped. `finally` still runs, then the `try` statement completes abruptly by rethrowing that same value ([[What happens if no catch matches and a finally block is present]]).

> [!warning] Retry is a new attempt, not a resume
> To run the same work again, put the `try` in a loop or call the method again. A `catch` cannot “continue” the failed `try` at the next statement. A `catch` that itself throws still does not return to the original `try`; `finally` runs, then that new reason propagates.

> [!tip] Interview answer
> **No. After a throw, the rest of the `try` block is skipped and is never resumed. The matching `catch` runs, then `finally` if any, then the statement after the whole `try`. If nothing catches, `finally` still runs and the exception keeps propagating.**
