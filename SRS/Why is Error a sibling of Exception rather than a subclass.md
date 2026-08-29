<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #Java/Exceptions/Error #SRS

# Why is `Error` a sibling of `Exception` rather than a subclass?

> [!abstract] Short answer
> **So `catch (Exception e)` can take recoverable application failures without also catching JVM-level `Error`s such as `OutOfMemoryError` or `StackOverflowError`.** Ordinary programs are not expected to recover from that branch. `Error` stays a `Throwable`; catching it is legal, just not the point of the tree.

## The `catch (Exception e)` idiom

`Throwable` has two usual children: `Exception` and `Error`. `Exception` is the superclass of conditions ordinary programs may wish to recover from. `Error` is the superclass of conditions they are **not** ordinarily expected to recover from ([[What sits at the root of every Java exception]], [[What is java.lang.Error]], [[What is the difference between Throwable and Exception]]).

If `Error` extended `Exception`, then `catch (Exception e)` would also match `OutOfMemoryError` and `StackOverflowError`. The sibling split exists so that one clause can mean “everything we might handle” without also meaning “the VM is dying” ([[Does catch Exception also catch Error]], [[What is the difference between RuntimeException and Error]], [[What is VirtualMachineError]]).

`RuntimeException` **is** under `Exception`, so `catch (Exception e)` **does** catch NPE and friends. The split is `Error` versus `Exception`, not checked versus unchecked. Both `Error` and `RuntimeException` are unchecked ([[Are Error subclasses checked or unchecked]], [[What is RuntimeException]], [[Does catch Exception also catch RuntimeException]]).

Catching `Error` (or `Throwable`) still compiles. Recoverability is a convention, not a language ban ([[Why should you not catch java.lang.Error]], [[Can you catch and handle java.lang.Error like normal exceptions]]).

```d2
direction: down
throwable: Throwable {
  width: 200
  height: 40
}
ex: Exception {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
err: Error {
  width: 220
  height: 40
  style.fill: "#ffebee"
}
rte: RuntimeException {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
oome: OutOfMemoryError {
  width: 240
  height: 40
  style.fill: "#ffebee"
}
throwable -> ex
throwable -> err
ex -> rte
err -> oome
```

**Fig. 1.** `catch (Exception)` follows the blue branch only.

```java
class Demo {
    static void catcher() {
        try {
            throw new OutOfMemoryError("simulated");
        } catch (Exception e) {
            // does not run
        }
    }
}
```

**Listing 1.** `OutOfMemoryError` is an `Error`, not an `Exception`. If `Error` were a subclass of `Exception`, this `catch` would run. `catch (Throwable t)` would match both branches.

> [!warning] Sibling is not “illegal to catch”
> `catch (Error e)` and `catch (Throwable t)` are valid. The tree is there so you are not **forced** to handle VM failures when you write `catch (Exception)`.

> [!warning] Unchecked is two branches
> `RuntimeException` is still an `Exception`. Dumps that say “unchecked sits beside Exception” are drawing `Error`, not `RuntimeException`.

> [!tip] Interview answer
> **`Error` is a sibling of `Exception` so `catch (Exception e)` can handle recoverable failures without catching JVM `Error`s.** Ordinary code is not expected to recover from `OutOfMemoryError` or `StackOverflowError`. You can still catch `Error`; the split is about that idiom, not a ban.
