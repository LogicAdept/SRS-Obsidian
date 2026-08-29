<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# What happens if `finally` returns after `try` throws an exception?

> [!abstract] Short answer
> **The method returns; the exception is discarded.** `return` in `finally` is abrupt completion that **replaces** the pending throw. The caller sees a normal return, not a thrown exception and not a stack trace for that failure. The same swallow happens if `catch` threw or `return`ed and then `finally` returns. It is legal, warned by `javac -Xlint:finally`, and almost always a bug.

## Abrupt `finally` wins; the throw is forgotten

If `try` (or `catch`) completes abruptly for reason `R` (including a throw), `finally` still runs. If `finally` then completes abruptly for reason `S` — a `return` with or without a value — the `try` statement completes for **`S`**. Reason `R` is discarded ([[How would you explain the finally block in Java]], [[Is a finally block always executed in Java]], [[What happens if no catch matches and a finally block is present]]).

From the caller’s side that looks like a **normal** method completion: a value comes back (or a `void` method returns). Nothing propagates. A `throw` **in** `finally` is also `S`, but then the caller **does** see an exception — the new one, not the original ([[What happens if try and finally both throw an exception]]). `return` in `finally` is the complete swallow.

This is not the “saved `V` then mutate the local” rule. A `return` **from** `finally` replaces that saved completion entirely ([[What happens if finally mutates a local after try returns it]], [[How would you explain try-catch-finally]]).

```d2
direction: down
try: "try throws V" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
fin: "finally { return x; }" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
gone: "V discarded" {
  width: 260
  height: 50
  style.fill: "#eceff1"
}
ok: "caller gets a normal return" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
try -> fin -> gone
fin -> ok
```

**Fig. 1.** `return` in `finally` is a new completion reason. The pending throw does not resume afterward.

```java
class Demo {
    static int swallow() {
        try {
            throw new IllegalStateException("try");
        } finally {
            return 0;
        }
    }

    static int catchThenFinally() {
        try {
            throw new NullPointerException();
        } catch (NullPointerException e) {
            return 1;
        } finally {
            return 0;
        }
    }
}
```

**Listing 1.** `swallow()` returns `0`; the `IllegalStateException` never reaches the caller. `catchThenFinally()` also returns `0`, not `1`. `javac -Xlint:finally` warns that this `finally` cannot complete normally. It is not a compile error ([[Is a finally block always executed in Java]]).

> [!warning] `throw` in `finally` vs `return` in `finally`
> `throw` in `finally` **replaces** the original exception with a new one (the first is lost unless you added it as a suppressed/cause yourself). `return` in `finally` **hides** the failure completely: no exception at all.

> [!warning] Not a compile error
> The language allows `return` in `finally`. Rely on `-Xlint:finally` (and reviews), not on the compiler rejecting it.

> [!tip] Interview answer
> **If `finally` returns, the exception from `try` is discarded and the method returns normally.** The caller never sees that throw. `throw` in `finally` replaces the original exception instead of swallowing it. Don’t return from `finally`.
