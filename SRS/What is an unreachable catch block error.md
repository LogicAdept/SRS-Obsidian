<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# What is an unreachable catch block error?

> [!abstract] Short answer
> **A compile-time error: a later `catch` can never run because an earlier one already handles that type.** Catches are tried top-down; the first matching clause wins. A parent type must come **after** its subclasses. Unrelated types may appear in any order. Only one `catch` of that `try` runs for a given throw.

## Parent before child is dead code

Handlers are considered left to right. The first clause whose type is assignment-compatible with the thrown object is selected; later siblings of the same `try` are skipped ([[How many catch blocks execute for one thrown exception]], [[How would you explain try-catch-finally]]).

If an earlier `catch` can catch `E1` or a **superclass** of `E1`, a later `catch` for `E1` is unreachable. Classic case: `catch (IOException)` then `catch (FileNotFoundException)` — `FileNotFoundException` is already handled ([[In what order should catch blocks appear for IOException and FileNotFoundException]], [[Does throws IOException cover FileNotFoundException]]). The same for `catch (Exception)` then `catch (RuntimeException)` ([[Does catch Exception also catch RuntimeException]]).

Unrelated checked types (`IOException` and `InterruptedException`) have no parent/child relation, so either order compiles.

A **multi-catch** `A | B` is a different error if `A` is a subclass of `B`: the alternatives must not be nested types, not “unreachable catch” ([[Why can multi-catch exception types not share a parent-child relationship]], [[Can one catch block handle multiple exception types in Java]]).

A separate rule: a `catch` of a **checked** type that the `try` cannot throw is also a compile-time error, unless the catch type is `Exception` or a superclass of `Exception` (`Throwable`). `catch (Exception)` / `catch (Throwable)` stay legal even when the body throws nothing checked ([[Does catching Exception satisfy a checked exception obligation]], [[Does catch Exception also catch Error]]).

```d2
direction: down
bad: "catch (IOException)\nthen catch (FileNotFoundException)" {
  width: 340
  height: 70
  style.fill: "#ffebee"
}
ok: "catch (FileNotFoundException)\nthen catch (IOException)" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
u: "child catch never runs" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
bad -> u
```

**Fig. 1.** Specific first, then general. Unrelated types: any order.

```java
import java.io.FileNotFoundException;
import java.io.IOException;

class Demo {
    static void unreachable() throws IOException {
        try {
            throw new FileNotFoundException();
        } catch (IOException e) {
            System.out.println("io");
        } catch (FileNotFoundException e) { // compile-time error
            System.out.println("fnf");
        }
    }

    static void specificFirst() {
        try {
            throw new FileNotFoundException();
        } catch (FileNotFoundException e) {
            System.out.println("fnf");
        } catch (IOException e) {
            System.out.println("io");
        }
    }
}
```

**Listing 1.** `unreachable` does not compile. `specificFirst` does: the first matching `catch` runs and the second is skipped at run time, not rejected.

> [!warning] Multi-catch is not this error
> `catch (FileNotFoundException | IOException e)` fails because the alternatives are parent and child, even though there is only one `catch` clause. That is not “unreachable catch.”

> [!warning] Broader catch after a more specific one can still warn
> `catch (FileNotFoundException)` then `catch (IOException)` is **reachable** in the language sense. If the `try` can throw only `FileNotFoundException`, compilers are encouraged to **warn** that the second clause is redundant, but it is not the unreachable-catch error.

> [!tip] Interview answer
> **Unreachable catch is a compile error when a later `catch` is a subtype of an earlier one — parent types must come last.** Unrelated types can be in any order. Only one catch runs. Multi-catch of parent `|` child is a different compile error.
