<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/Exceptions/TryCatch #SRS

# Can you catch and handle `java.lang.Error` like normal exceptions?

> [!abstract] Short answer
> **You can catch it; you should not treat it like a normal exception.** `catch (Error e)` and `catch (Throwable t)` compile. `Error` is unchecked, so methods need no `throws Error`. Recovery the way you recover from `IOException` is not what `Error` is for.

## Legal to catch, not designed as recovery

`Error` is a `Throwable`. A `catch` whose parameter is `Error`, a subclass (`OutOfMemoryError`), or `Throwable` can handle it. `catch (Exception e)` does **not** — `Error` is a sibling of `Exception`, not a subclass ([[Does catch Exception also catch Error]], [[What is java.lang.Error]], [[Why is Error a sibling of Exception rather than a subclass]]).

Because `Error` is unchecked, the compiler does not require `catch` or `throws` ([[Are Error subclasses checked or unchecked]], [[Can you catch an unchecked exception in Java]]). That is the same exemption as `RuntimeException`, not a claim that catching is a good idea.

The language still allows sophisticated programs to catch some of these conditions (log at a process boundary, last-resort cleanup). That is not the same as “handle like `IOException`”: after `VirtualMachineError` (`OutOfMemoryError`, `StackOverflowError`) the heap or stack is already exhausted, so the `catch` body often cannot run usefully ([[Why should you not catch java.lang.Error]], [[What is VirtualMachineError]], [[Should you catch AssertionError]]).

```d2
direction: down
err: "throw Error" {
  width: 240
  height: 50
}
exc: "catch (Exception)" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
er: "catch (Error) / Throwable" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
miss: "misses" {
  width: 200
  height: 40
}
ok: "compiles; not recovery" {
  width: 260
  height: 50
}
err -> exc -> miss
err -> er -> ok
```

**Fig. 1.** Catching `Error` is allowed. Catching `Exception` is not catching `Error`.

```java
class Demo {
    static void catchError() {
        try {
            throw new OutOfMemoryError("simulated");
        } catch (Exception e) {
            // does not run
        } catch (Error e) {
            // compiles — same syntax as any catch
        }
    }
}
```

**Listing 1.** `catch (Error)` uses the same `try`/`catch` machinery as `Exception`. After a real `OutOfMemoryError`, even this handler may be unable to allocate. Prefer not to continue as if it were a business exception.

> [!warning] Can ≠ should
> Interviewers often want both: syntax allows it; a reasonable application should not try to catch `Error` as a recovery strategy ([[Why should you not catch java.lang.Error]]).

> [!warning] `catch (Throwable)` looks like a universal handler
> It also takes `Error`. Swallowing `Throwable` to “never crash” hides OOM, stack overflow, and `AssertionError`.

> [!tip] Interview answer
> **Yes, `catch (Error)` compiles — `Error` is an unchecked `Throwable`.** `catch (Exception)` misses it. You still should not handle `Error` like `IOException`: it marks a serious failure, often with no resources left to recover.
