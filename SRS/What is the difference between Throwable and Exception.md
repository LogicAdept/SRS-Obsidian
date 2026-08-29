<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS

# What is the difference between `Throwable` and `Exception`?

> [!abstract] Short answer
> **`Throwable` is the root of everything that can be thrown or caught.** **`Exception` is one of its two usual branches** — conditions a program may recover from. The other branch is `Error`. `catch (Exception e)` therefore misses `Error`. `RuntimeException` still sits under `Exception`.

## Root versus the recoverable branch

Only instances of `Throwable` (or a subclass) may appear in `throw` or `catch`. `Throwable` is a **class**, a direct subclass of `Object`. Its two direct subclasses are `Exception` and `Error` ([[What sits at the root of every Java exception]], [[Is Throwable a class or an interface]], [[Can you throw an object that is not a Throwable]], [[What information does a Throwable carry]]).

`Exception` is the superclass of conditions ordinary programs may wish to recover from. `Error` is the superclass of serious problems they are not ordinarily expected to recover from. That split is why `catch (Exception e)` does not catch `OutOfMemoryError` — you need `catch (Throwable t)` (or `Error`) for both branches ([[Does catch Exception also catch Error]], [[What is java.lang.Error]], [[Can you catch Throwable]]).

`RuntimeException` is a subclass of `Exception`, so it **is** an `Exception` even though it is unchecked. Saying “all exceptions extend `Exception`” is false for `Error` and for `Throwable` itself ([[What is RuntimeException]], [[What is the difference between RuntimeException and Error]], [[Do checked exceptions inherit Throwable directly]], [[Is Throwable a checked exception]]).

```d2
direction: down
throwable: Throwable {
  width: 200
  height: 40
}
ex: Exception {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
err: Error {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
rte: RuntimeException {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
throwable -> ex
throwable -> err
ex -> rte
```

**Fig. 1.** `Exception` is a branch of `Throwable`, not the whole tree.

```java
class Demo {
    static void catcher() {
        try {
            throw new OutOfMemoryError("simulated");
        } catch (Exception e) {
            // does not run — Error is not an Exception
        }
    }
}
```

**Listing 1.** `catch (Exception)` misses `Error`. The thrown object is still a `Throwable`. `catch (Throwable t)` would match.

> [!warning] “Every exception extends `Exception`” is false
> `Error` does not. `Throwable` does not extend `Exception`; `Exception` extends `Throwable`. `RuntimeException` *does* extend `Exception`.

> [!warning] `catch (Exception)` is not “everything throwable”
> That is the reason `Error` is a sibling. Interview snippets that “handle all failures” with `Exception` leave the VM-failure branch uncaught.

> [!tip] Interview answer
> **`Throwable` is the root of throw and catch.** **`Exception` is the recoverable branch under it; `Error` is the other branch.** `catch (Exception)` therefore misses `Error`. `RuntimeException` is still an `Exception`.
