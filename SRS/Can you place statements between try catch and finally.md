<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# Can you place statements between try, catch, and finally?

> [!abstract] Short answer
> **No.** `try`, its `catch` clauses, and its `finally` are pieces of **one** statement. There is no grammatical slot for another statement between the `try` block, a `catch`, or `finally`. Extra work goes *inside* a block, or in a nested `try`.

## One statement, glued clauses

A `try` statement is `try` Block plus `catch` clauses, or that form plus one `finally`, or try-with-resources with the same optional `catch`/`finally`. Each `catch` is `catch (` parameter `)` Block, consecutive if there are several. `finally` is `finally` Block. Nothing in that shape is a free-standing statement you can insert `log(...)` into.

If the parser has already finished a complete `try`/`catch`, a following `finally` is not attached — `finally` is not a statement by itself. See [[Can a try block exist without catch and finally]] and [[Can a try statement have more than one finally block]].

```d2
direction: down
stmt: "one try statement" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
tryb: "try { ... }" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
catches: "catch { ... } catch { ... }" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
fin: "finally { ... }" {
  width: 220
  height: 50
  style.fill: "#f3e5f5"
}
stmt -> tryb
stmt -> catches
stmt -> fin
```

**Fig. 1.** Clauses of one `try` sit next to each other. Code between them is not in this statement.

```java
class Demo {
    static void work() {}
    static void handle(RuntimeException e) {}
    static void cleanup() {}
    static void log(String m) {}

    static void legal() {
        try {
            work();
        } catch (RuntimeException e) {
            handle(e);
        } finally {
            cleanup();
        }
    }
}
```

**Listing 1.** The only legal order: `try` block, then zero or more `catch` blocks, then at most one `finally`, with no other statements in between.

```java
class Demo {
    static void work() {}
    static void handle(RuntimeException e) {}
    static void cleanup() {}
    static void log(String m) {}

    static void nested() {
        try {
            try {
                work();
            } catch (RuntimeException e) {
                handle(e);
            }
            log("still in the outer try block");
        } finally {
            cleanup();
        }
    }
}
```

**Listing 2.** `log` is a statement *inside* the outer `try` block, after a nested `try`/`catch`. That is not “between” the outer `try` and `finally`.

> [!warning] A finished `try`/`catch` cannot grow a `finally` later
> `try { work(); } catch (RuntimeException e) { handle(e); } log("x"); finally { cleanup(); }` does not compile. The first `try`/`catch` is already a complete statement; `finally` cannot start the next one. Put `log` inside `try`, inside `catch`, inside `finally`, or after the whole `try` statement ([[Can you try-finally without catch]]).

> [!tip] Interview answer
> **No — `try`, `catch`, and `finally` form a single statement, so you cannot put other statements between those blocks. Nested `try` statements inside a block are fine; that is inner code, not a gap between sibling clauses. If you need work after `catch` but still covered by `finally`, keep it in the `try` block or nest another `try`.**
