<!--
reps: 0
priority: 0
-->
#Java/Exceptions #SRS

# What error handling approaches exist in Java?

> [!abstract] Short answer
> **The language approach is exceptions: `throw`, `try`/`catch`/`finally`, `throws`, and try-with-resources.** Checked types force catch-or-specify. Unchecked types do not. If nothing catches, the thread’s uncaught-exception handler runs. Magic return codes such as `-1` are the style Java’s `throw` was meant to replace.

## Exceptions, not “funny” return values

A failure is a `Throwable`. **Catch** when this layer can recover; **propagate** with `throws` when it cannot; **wrap** only when the API should speak a different type ([[How would you explain Java exception handling try catch and propagation]], [[How do you handle exceptions in Java applications]], [[How should you throw and handle exceptions in Java]]).

**Checked** exceptions (`IOException`, …) must be caught or declared. That is a compile-time approach, not optional documentation ([[What happens if you neither catch nor declare a checked exception]], [[What is the difference between checked and unchecked exceptions]]). **Unchecked** (`RuntimeException`, `Error`) skip that obligation; catching `Error` is still not recovery ([[Why should you not catch java.lang.Error]]).

**`finally`** and **try-with-resources** are cleanup approaches: always-on-the-way-out vs automatic `AutoCloseable.close` with suppression ([[What is try-with-resources]]).

If no `catch` on the stack handles the throw, the thread dies after its **uncaught-exception handler** (default: print the stack trace). `main` may `throws` and still end that way ([[Can main throw exceptions outward and where are they handled]]).

`assert` is a separate, optional check that throws `AssertionError` when enabled — not a substitute for validating a public API.

```d2
direction: down
fail: "failure" {
  width: 240
  height: 50
}
catch: "catch and recover" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
prop: "throws / wrap" {
  width: 260
  height: 50
}
uncaught: "uncaught handler" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
fail -> catch
fail -> prop -> uncaught
```

**Fig. 1.** Recover locally, declare it upward, or let the thread’s uncaught handler run.

```java
class Demo {
    static int oldStyle(boolean fail) {
        return fail ? -1 : 1;
    }

    static int withThrow(boolean fail) throws java.io.IOException {
        if (fail) {
            throw new java.io.IOException("fail");
        }
        return 1;
    }
}
```

**Listing 1.** `-1` can be ignored. `throws IOException` cannot: callers must catch or specify.

> [!warning] Returning `-1` is still easy to ignore
> That is why `throw` exists as the default failure channel. Mixing both in one API hides which values are real.

> [!warning] Empty `catch` is not an “approach”
> It satisfies the compiler for checked types and deletes the failure. Catch-or-specify expected a policy, not a no-op.

> [!tip] Interview answer
> **Java’s error handling is exceptions: catch if you can recover, otherwise `throws`, with `finally` or try-with-resources for cleanup.** Checked types force that choice. If nothing handles the throw, the uncaught-exception handler runs. Sentinel return values are the old style `throw` replaced.
