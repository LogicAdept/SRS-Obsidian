<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# How many catch blocks execute for one thrown exception?

> [!abstract] Short answer
> **At most one `catch` clause of that `try` statement.** Handlers are tried in source order; the first whose catchable type is assignment-compatible with the thrown object runs. Later sibling `catch` clauses of the same `try` are skipped. `finally` still runs after that single handler.

## First match wins; siblings do not share the throw

A `try` with several `catch` clauses considers them left to right. If the `try` block throws a value `V`, the **first (leftmost)** `catch` whose type can accept `V` is selected. `V` is assigned to that clause’s parameter and **only that** block runs. If the selected `catch` completes normally, the `try` statement completes normally (then `finally`, if present). Control does not fall through to the next `catch` ([[Does control return to the try block after a catch handles an exception]], [[In what order should catch blocks appear for IOException and FileNotFoundException]]).

If no clause of that `try` matches, the throw continues out of the statement (after `finally`, if any). An **enclosing** `try` is a different statement and may select **its** first matching `catch` for the same `V` ([[What happens if no catch matches and a finally block is present]], [[How would you explain try-catch-finally]]).

A multi-`catch` (`A | B`) is still **one** clause: one parameter, one block ([[Can one catch block handle multiple exception types in Java]]). A later sibling that could never be first match is unreachable at compile time ([[What is an unreachable catch block error]]).

```d2
direction: down
throw: "try block throws V" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
first: "first matching catch runs" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
skip: "later sibling catch clauses\nare not entered" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
fin: "finally still runs" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
throw -> first
first -> skip
first -> fin
```

**Fig. 1.** One throw, one selected handler on that `try`, then `finally`.

```java
class Demo {
    static void run(boolean firstKind) {
        try {
            if (firstKind) {
                throw new IllegalArgumentException("a");
            }
            throw new IllegalStateException("b");
        } catch (IllegalArgumentException e) {
            System.out.println("arg");
            throw new NullPointerException();
        } catch (IllegalStateException e) {
            System.out.println("state");
        } finally {
            System.out.println("finally");
        }
    }
}
```

**Listing 1.** For one throw from the `try` block, exactly one of the two `catch` clauses runs. A `NullPointerException` thrown from the first `catch` is **not** handled by the sibling `IllegalStateException` (or by a sibling `RuntimeException` of the same `try`). `finally` still executes ([[Does catch Exception also catch RuntimeException]]).

> [!warning] A throw from `catch` is a new throw
> Sibling `catch` clauses of the **same** `try` never see it. Only an **enclosing** `try` (or the thread’s uncaught handler) can handle it. `finally` of the original `try` still runs, and if `finally` throws, that reason replaces the one from `catch`.

> [!warning] Broader `catch` first steals every subclass
> `catch (Exception e)` before `catch (IOException e)` makes the second clause unreachable. Order is “more specific first,” but still only one block runs for a given throw.

> [!tip] Interview answer
> **At most one `catch` of that `try` runs — the first type that matches the thrown object, in source order.** Later siblings are skipped. An exception thrown from inside `catch` is not caught by those siblings; `finally` still runs.
