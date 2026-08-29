<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/Concurrency/Threads #SRS

# What is `ThreadDeath`?

> [!abstract] Short answer
> **An `Error` that a victim thread used to throw when `Thread.stop()` was called.** `Thread.stop` has been **removed**. `ThreadDeath` itself is **deprecated for removal**. It is not an `Exception`. `catch (Exception)` never caught it.

## Old `stop()`, not a recoverable `Exception`

`ThreadDeath` extends `Error`. It is unchecked. Ordinary application code was never supposed to treat it like a business exception ([[What is java.lang.Error]], [[Are Error subclasses checked or unchecked]], [[What is the difference between RuntimeException and Error]], [[Does catch Exception also catch Error]]).

`Thread` originally specified `stop()` to inject `ThreadDeath` into the victim. That API was unsafe. `stop` is gone; the `ThreadDeath` type remains only as a leftover, marked for removal.

Dumps still show `run()` calling `stop()`, catching `ThreadDeath`, and printing that the thread “has died.” Catching it (or catching `Error`) could let the thread continue after `stop()` as if it were still a normal worker. That is why interview books said: if you catch it, **rethrow** it. `catch (Exception)` did **not** swallow it, which is why the type is an `Error` rather than `Exception` ([[Why should you not catch java.lang.Error]], [[Can you catch and handle java.lang.Error like normal exceptions]]).

A static initializer that throws `ThreadDeath` does **not** get a special wrap. Like any `Error`, it is not wrapped in `ExceptionInInitializerError` (that wrap is for non-`Error` throwables) ([[What happens if you use a class after ExceptionInInitializerError]]).

```d2
direction: down
err: Error {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
td: "ThreadDeath (deprecated, for removal)" {
  width: 320
  height: 50
  style.fill: "#ffebee"
}
ex: Exception {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
err -> td
```

**Fig. 1.** `ThreadDeath` is an `Error`, not under `Exception`.

```java
class Demo {
    @SuppressWarnings("removal")
    static void throwDeath() {
        throw new ThreadDeath();
    }

    static void catcher() {
        try {
            throwDeath();
        } catch (Exception e) {
            // does not run
        }
    }
}
```

**Listing 1.** You can still construct `ThreadDeath` (deprecated). There is no `Thread.stop()` to call. `catch (Exception)` misses it. Do not write new code that throws or catches this type.

> [!warning] `Thread.stop()` is not on modern JDKs
> Interview dumps still pair `stop()` with `ThreadDeath`. The method has been removed. The class is a deprecated leftover. Do not design cancellation around either.

> [!warning] It is not a “runtime exception”
> Unchecked, yes. Subclass of `RuntimeException`, no. `catch (RuntimeException)` misses it the same way it misses `OutOfMemoryError` ([[What is RuntimeException]]).

> [!tip] Interview answer
> **`ThreadDeath` is an `Error` that `Thread.stop()` used to throw in the victim thread.** `stop` is gone and `ThreadDeath` is deprecated for removal. It is not an `Exception`, so `catch (Exception)` never handled it. Do not catch it to “keep the thread alive.”
