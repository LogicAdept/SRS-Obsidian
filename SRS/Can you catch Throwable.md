<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #Java/Exceptions/TryCatch #SRS

# Can you catch `Throwable`?

> [!abstract] Short answer
> **Yes.** `catch (Throwable t)` compiles: `Throwable` is a class, and a catch type may be `Throwable` or a subclass. **Prefer not to** as a recovery strategy — it also catches `Error` (`OutOfMemoryError`, `StackOverflowError`), which ordinary programs are not expected to recover from. Catch the specific types you can handle.

## The root of everything throwable

Every catch parameter type must be `Throwable` or a subclass. `Throwable` is a **class**, not an interface, so it is a legal catch type ([[Is Throwable a class or an interface]], [[Is Throwable a checked exception]]).

`Exception` and `Error` both extend `Throwable`. `catch (Exception e)` therefore misses `Error`. `catch (Throwable t)` takes **both** branches: checked and unchecked `Exception`s **and** `Error`s ([[Does catch Exception also catch Error]], [[What is the difference between Throwable and Exception]], [[Can you catch and handle java.lang.Error like normal exceptions]]).

Because `Throwable` is itself a checked type, `catch (Throwable t)` also satisfies a checked-exception obligation for the `try` block — the same way `catch (Exception e)` does, but wider ([[Does catching Exception satisfy a checked exception obligation]]).

That width is the problem. `Error` means a serious failure; after OOM or stack overflow the handler may not be able to allocate or call. `AssertionError` is an `Error` too. A “never crash” `catch (Throwable)` that swallows the value hides those conditions ([[Why should you not catch java.lang.Error]], [[What is java.lang.Error]]).

If you catch `Throwable` at a thread or process boundary, log and rethrow or abort. Do not continue as if it were `IOException`.

```d2
direction: down
th: "Throwable" {
  width: 200
  height: 50
}
ex: "Exception" {
  width: 200
  height: 50
}
err: "Error" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}
catchT: "catch (Throwable)" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
th -> ex
th -> err
th -> catchT
ex -> catchT
err -> catchT
```

**Fig. 1.** `catch (Throwable)` is the union of the `Exception` and `Error` trees.

```java
class Demo {
    static void catcher() {
        try {
            throw new OutOfMemoryError("simulated");
        } catch (Exception e) {
            // does not run — Error is not an Exception
        } catch (Throwable t) {
            // compiles; also catches Error
        }
    }
}
```

**Listing 1.** `catch (Throwable)` is legal and wider than `catch (Exception)`. Swallowing `t` hides VM failures.

> [!warning] Legal ≠ a good default
> Interviewers want: yes, you can; no, you should not use it as everyday recovery. Catch specific types; leave `Error` to the uncaught handler unless you are at a last-resort boundary.

> [!warning] Order still matters
> `catch (Exception e)` then `catch (Throwable t)` is legal: the second clause is reachable for `Error`. `catch (Throwable t)` then `catch (Exception e)` is an unreachable catch.

> [!tip] Interview answer
> **Yes — `catch (Throwable t)` is allowed because every thrown object is a `Throwable`.** It also catches `Error`, including OOM and stack overflow, so it is a poor default. Catch the exceptions you can recover from; do not treat `Throwable` as a synonym for `Exception`.
