<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS

# Why should you not catch `java.lang.Error`?

> [!abstract] Short answer
> **Because an `Error` means a serious problem a reasonable application should not try to recover from.** After `OutOfMemoryError` or `StackOverflowError` the VM is already out of heap or stack; catching and continuing is usually worse than letting the thread (or process) die. Catching `Error` is **legal**, just not a recovery strategy.

## VM failure, not a business exception

`Error` is the `Throwable` branch for conditions ordinary programs are not expected to recover from. That is why it sits **beside** `Exception`: `catch (Exception e)` skips it on purpose ([[What is java.lang.Error]], [[Why is Error a sibling of Exception rather than a subclass]], [[Does catch Exception also catch Error]], [[Are Error subclasses checked or unchecked]]).

`VirtualMachineError` covers resource collapse: `OutOfMemoryError` (cannot allocate), `StackOverflowError` (stack used up). The heap or stack is already in a bad state. Code in `catch` that logs, allocates a string, or “retries” often needs those same resources and can fail again ([[What is VirtualMachineError]], [[How do you reproduce an OutOfMemoryError in Java]], [[How do you produce a StackOverflowError]]).

`AssertionError` is also an `Error`: catching it hides a failed invariant ([[Should you catch AssertionError]]). Linkage `Error`s (`NoClassDefFoundError`) mean the type system is already inconsistent for that class.

Handling is **not forbidden**. `catch (Error e)` and `catch (Throwable t)` compile. Sophisticated code may log or clean up at a process boundary. That is last-resort shutdown, not “handle like `IOException`” ([[Can you catch and handle java.lang.Error like normal exceptions]], [[What is the difference between RuntimeException and Error]]).

```d2
direction: down
err: "Error (OOME, SOE, ...)" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
catch: "catch (Error) and continue" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
die: "thread/process dies (usual)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
bad: "catch allocates / retries\n→ often fails again" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
err -> die
err -> catch
catch -> bad
```

**Fig. 1.** Legal catch versus a VM that has already run out of resources.

```java
class Demo {
    static void catcher() {
        try {
            throw new OutOfMemoryError("simulated");
        } catch (Exception e) {
            // does not run
        } catch (Error e) {
            // compiles; not a recovery plan
        }
    }
}
```

**Listing 1.** `catch (Exception)` misses `Error`. `catch (Error)` compiles. After a **real** `OutOfMemoryError`, even building the log line in that handler may allocate. Prefer letting the uncaught handler terminate the thread.

> [!warning] “Can you catch?” is not “should you catch?”
> Unchecked includes `Error`. Catch is optional and **allowed**. The design is: do not treat VM collapse as an application exception ([[Can you catch and handle java.lang.Error like normal exceptions]]).

> [!warning] `catch (Throwable)` is the wide net
> It catches `Exception` **and** `Error`. A top-level “never crash” handler that swallows `Throwable` will hide OOM and stack overflow.

> [!tip] Interview answer
> **Do not catch `Error` because it marks a serious VM or system failure, not a recoverable business condition.** After OOM or stack overflow the runtime is already out of resources, so continuing is usually worse than dying. Catching is legal; `catch (Exception)` does not see `Error` at all.
