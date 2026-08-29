<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS

# What information does a `Throwable` carry?

> [!abstract] Short answer
> **A message, a stack snapshot, an optional cause, and any suppressed throwables.** `getMessage()` is the detail string. `getStackTrace()` / `printStackTrace()` show frames captured **when the object was created**. `getCause()` is the chained exception. `getSuppressed()` is what try-with-resources (or `addSuppressed`) attached. Only `Throwable` instances can be thrown or caught.

## Four pieces of state

`Throwable` is a class (`implements Serializable`). Every error and exception is one ([[Is Throwable a class or an interface]], [[What is the difference between Throwable and Exception]], [[Can you throw an object that is not a Throwable]]).

- **Message** — `getMessage()` / `getLocalizedMessage()`. Constructors take a `String`, or derive one from `cause.toString()`.
- **Stack trace** — a snapshot of the current thread’s frames **at construction** (via `fillInStackTrace()`). `printStackTrace()` writes it; `getStackTrace()` returns `StackTraceElement[]`. Creating the object in one place and throwing it later still shows the **construction** site unless you call `fillInStackTrace()` again.
- **Cause** — `getCause()`. Set with a cause constructor or `initCause` **at most once** (and never if a cause constructor already set it). A throwable cannot be its own cause. Wrapping stores the original failure here ([[Does wrapping a checked exception in RuntimeException require a throws clause]]).
- **Suppressed** — `getSuppressed()` / `addSuppressed()`. Typically filled by try-with-resources when `close` fails after a primary exception. Cause and suppressed can both be present ([[What is a suppressed exception in try-with-resources]], [[How does the compiler translate try-with-resources]]).

A protected constructor can disable suppression and/or make the stack trace non-writable (used by some VM-created errors). JVM-generated `NullPointerException` may also fill a verbose `getMessage()` from bytecode ([[What did Java 14 change about NullPointerException messages]]).

```d2
direction: down
t: "Throwable" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
m: "message" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
st: "stack at construction" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
c: "cause chain" {
  width: 220
  height: 50
  style.fill: "#fff8e1"
}
s: "suppressed list" {
  width: 260
  height: 50
  style.fill: "#f3e5f5"
}
t -> m
t -> st
t -> c
t -> s
```

**Fig. 1.** Cause is “this happened because of that.” Suppressed is “this other failure happened on the way out.”

```java
class Demo {
    static void show() {
        RuntimeException e = new RuntimeException("msg", new IllegalStateException("cause"));
        try {
            throw e;
        } catch (RuntimeException caught) {
            System.out.println(caught.getMessage());
            System.out.println(caught.getCause());
            caught.printStackTrace();
            System.out.println(caught.getSuppressed().length);
        }
    }
}
```

**Listing 1.** Message and cause come from the constructor. The printed frames are from `new RuntimeException(...)`, which here is the same stack as the `throw`. `getSuppressed()` is empty unless TWR or `addSuppressed` ran.

> [!warning] Stack traces are captured at `new`, not at `throw`
> `Throwable t = new RuntimeException(); /* later */ throw t;` still points at the `new` line. Call `fillInStackTrace()` before throw if you need the throw site. Some VMs may omit frames.

> [!warning] `initCause` is one-shot
> If you used `Throwable(String, Throwable)` or `Throwable(Throwable)`, `initCause` throws `IllegalStateException`. A second `initCause` does the same. Setting `cause == this` throws `IllegalArgumentException`.

> [!tip] Interview answer
> **A `Throwable` carries a message, a stack snapshot from construction, an optional cause, and suppressed exceptions.** `printStackTrace` shows the stack; `getCause` is wrapping; `getSuppressed` is try-with-resources extras. The stack is filled when the object is created, not when it is thrown.
