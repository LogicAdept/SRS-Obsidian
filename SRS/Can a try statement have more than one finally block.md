<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# Can a try statement have more than one finally block?

> [!abstract] Short answer
> **No.** One `try` statement has at most one `finally` clause. You may write several `catch` clauses on that same statement, but not several `finally` blocks. Extra cleanup goes inside that single `finally`, or in a nested `try` that has its own `finally`.

## One `finally` per `try`, not per method

The statement is `try` + `catch`(es), `try` + optional `catch`(es) + one `finally`, or try-with-resources. `finally` appears at most once in each of those forms. `catch` is the part that repeats. See [[Can a try block exist without catch and finally]] and [[Can you try-finally without catch]].

```d2
direction: down
stmt: "one try statement" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
catches: "zero or more catch" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
fin: "at most one finally" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
nested: "nested try\n= another statement\n= another finally" {
  width: 260
  height: 80
  style.fill: "#f3e5f5"
}
stmt -> catches
stmt -> fin
stmt -> nested
```

**Fig. 1.** Multiple `finally` blocks mean nested (or sequential) `try` statements, not one statement with two `finally` clauses.

```java
class Demo {
    static void work() {}
    static void innerCleanup() {}
    static void outerCleanup() {}

    static void nested() {
        try {
            try {
                work();
            } finally {
                innerCleanup();
            }
        } finally {
            outerCleanup();
        }
    }
}
```

**Listing 1.** Two `finally` blocks, two `try` statements. `try { work(); } finally { innerCleanup(); } finally { outerCleanup(); }` does not parse.

There is no slot for statements between `try`, `catch`, and `finally` — they are pieces of one statement ([[Can you place statements between try catch and finally]]).

## Try-with-resources still has only one `finally`

An *extended* try-with-resources statement may add `catch` clauses and/or a `finally`. That is still a single `finally`. The statement is defined as a basic try-with-resources (automatic `close`) nested inside an ordinary `try`/`catch`/`finally`. Resources are closed, or closing is attempted, **before** that `finally` runs.

```java
class Handle implements AutoCloseable {
    @Override
    public void close() {}
}

class Demo {
    static void work() {}
    static void extra() {}

    static void use() {
        try (Handle h = new Handle()) {
            work();
        } finally {
            extra();
        }
    }
}
```

**Listing 2.** One explicit `finally`. `close()` has already been attempted when `extra()` runs. See [[What is try-with-resources]] and [[Is a finally block always executed in Java]].

> [!warning] Automatic close is not a second `finally` you can write
> Try-with-resources injects closing in the translation; you still cannot write `finally { ... } finally { ... }` on that statement. If `close()` throws and `finally` also throws, the `finally` exception wins and the close exception is not the one that propagates from this outer `try` — same abrupt-completion rule as any `try`/`finally`.

> [!tip] Interview answer
> **No — a single `try` statement may have many `catch` clauses but at most one `finally`. Put several cleanup steps in that block, or nest another `try`/`finally`. Try-with-resources may add one explicit `finally`, which runs after automatic `close`, and that is still only one `finally`.**
