<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #Java/Runtime #SRS

# Is a `finally` block always executed in Java?

> [!abstract] Short answer
> **No.** `finally` runs whenever the `try` (or a matching `catch`) **completes** — normally or abruptly, including `return` and `throw`. It does **not** run when that completion never happens: `System.exit` / `Runtime.exit` / `Runtime.halt`, a VM crash or kill, an infinite loop or deadlock inside `try`/`catch`, or a `try` that was never entered.

## Completes → `finally`. Does not complete → no `finally`

A `finally` clause is scheduled after the `try` block and after any `catch` that ran, **however** those blocks finish ([[How would you explain the finally block in Java]], [[What happens if no catch matches and a finally block is present]], [[Can you try-finally without catch]]). If that completion never happens, the clause is not reached.

`System.exit` and `Runtime.exit` terminate the VM and do not return **or throw**. `Runtime.halt` does the same and skips shutdown hooks. The `try` therefore never completes, so `finally` on that path does not run — and a `catch` around `exit` does not run either. If another thread exits the process, remaining threads are not unwound: their `finally` blocks are skipped too, including daemon threads when the last non-daemon thread ends ([[Can main throw exceptions outward and where are they handled]]).

An infinite loop, livelock, or deadlock in `try` or `catch` has the same effect: `finally` waits for a completion that never comes. If control never enters the `try` statement at all (an earlier `return` or throw), that `finally` is not part of the path.

`return` from `try` or `catch` still runs `finally`. If `finally` itself `return`s or `throw`s, that new completion **replaces** whatever was pending ([[What happens if finally returns after try throws an exception]], [[What happens if try and finally both throw an exception]]).

```d2
direction: down
try: "try / catch running" {
  width: 280
  height: 50
}
done: "block completes?" {
  width: 300
  height: 50
}
fin: "finally runs" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
skip: "finally skipped" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
try -> done
done -> fin: "yes (return, throw, …)"
done -> skip: "no (exit, halt, hang, crash)"
```

**Fig. 1.** `finally` is tied to completion of `try`/`catch`, not to “the process is still alive.”

```java
class Demo {
    static void skip() {
        try {
            System.exit(0);
        } finally {
            System.out.println("not printed");
        }
    }
}
```

**Listing 1.** `System.exit` does not complete the `try`, so `finally` does not run. A `return` in the same `try` would still run it.

> [!warning] `return` still runs `finally`
> Interview traps often claim `return` skips cleanup. It does not. Process death and non-completion are the real gaps.

> [!warning] Interrupt is not a skip, and other threads die without `finally`
> `Thread.interrupt` sets a status or throws `InterruptedException`. Unwinding still runs `finally`. Do not treat interrupt like `System.exit`. `exit` from one thread starts shutdown; remaining threads do not complete their current methods.

> [!tip] Interview answer
> **`finally` is not an absolute guarantee.** It runs whenever `try` or `catch` actually finishes, including on `return` and `throw`. It fails to run when that finish never happens: `System.exit` / `halt`, a killed VM, or a hang in `try`. Other threads can lose their `finally` when the process exits.
