<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# Can a try block exist without a catch in Java?

> [!abstract] Short answer
> **Yes.** A `try` may have `finally` and no `catch`, or it may be try-with-resources with neither. A **bare** `try { ... }` with no `catch`, no `finally`, and no resource list is a compile-time error.

## `catch` is optional when something else completes the `try`

A non-resource `try` must attach at least one of: one or more `catch` clauses, or a `finally` block. `try`/`finally` without `catch` is legal. The `finally` block still runs if the `try` block completes abruptly; the exception is not swallowed just because there is no handler ([[What happens if no catch matches and a finally block is present]], [[Can a try block exist without catch and finally]]).

Try-with-resources (`try (` resources `)`) may omit `catch` and `finally`. Automatic `close` is not a `catch`. You can still add `catch` or `finally` after the resource `try` ([[How does the compiler translate try-with-resources]], [[What happens if close throws after a try-with-resources body succeeds]]).

There is only one `finally` per `try`. Nothing may sit between `try`, `catch`, and `finally` ([[Can a try statement have more than one finally block]], [[Can you place statements between try catch and finally]]).

```d2
direction: down
q: "try without catch?" {
  width: 240
  height: 50
}
fin: "try { } finally { }\nlegal" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
twr: "try (r) { }\nlegal" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
bare: "try { }\nillegal" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
q -> fin
q -> twr
q -> bare
```

**Fig. 1.** Missing `catch` is fine with `finally` or resources. A lone `try` block is not.

```java
class Demo {
    static int tryFinally(boolean fail) {
        try {
            if (fail) {
                throw new IllegalStateException();
            }
            return 1;
        } finally {
            // runs; the IllegalStateException still propagates
        }
    }

    static void tryResources() throws java.io.IOException {
        try (java.io.StringWriter w = new java.io.StringWriter()) {
            w.write("ok");
        }
    }
}
```

**Listing 1.** `try`/`finally` and a basic try-with-resources have no `catch`. `try { }` alone does not compile.

> [!warning] No `catch` does not mean the exception is gone
> `try`/`finally` still lets the exception leave the statement after `finally` completes. Only a matching `catch` handles it.

> [!warning] Do not confuse this with a bare `try`
> “Without a `catch`” is allowed. “Without `catch` **and** without `finally` **and** without resources” is not ([[Can a try block exist without catch and finally]]).

> [!tip] Interview answer
> **Yes: `try`/`finally` and try-with-resources both omit `catch`.** A `try` by itself does not compile. Skipping `catch` does not swallow the exception; `finally` still runs, then the throw continues unless a handler matches.
