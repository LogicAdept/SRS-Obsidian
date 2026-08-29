<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch/TryWithResources #SRS

# What happens if a try-with-resources resource is null?

> [!abstract] Short answer
> **Automatic `close` is skipped.** The generated close path null-checks each resource. `close()` is not called on `null`, so automatic close does not throw `NullPointerException`. Using that null reference **inside the `try` body** is still an ordinary NPE.

## Null-tolerant close, not a null-tolerant body

A resource is closed only if it initialized to a **non-null** value. The compiler translation is `if (r != null) { r.close(); … }` ([[How does the compiler translate try-with-resources]], [[What is try-with-resources]]).

That is different from a **throwing** initializer. `null` as the initializer **completes normally**: the `try` block **does** run. A later constructor that throws never enters the body and still closes earlier non-null resources ([[What happens if a later try-with-resources constructor throws]]).

An existing effectively-final variable in `try (r)` is the same: if `r` is null, close is skipped.

```d2
direction: down
init: "resource initializer = null" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
body: "try body still runs" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
skip: "generated close skipped" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
npe: "r.use() in the body\nNullPointerException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
init -> body
body -> skip
body -> npe
```

**Fig. 1.** Null-tolerance is only the automatic close. Your code still sees `null`.

```java
class Demo {
    static void skippedClose() throws Exception {
        try (AutoCloseable r = null) {
            // no generated close(); no NPE from TWR
        }
    }

    static void bodyNpe() throws Exception {
        try (AutoCloseable r = null) {
            r.close();
        }
    }
}
```

**Listing 1.** `skippedClose` completes normally. `bodyNpe` throws `NullPointerException` because **you** invoked an instance method on `null`, not because of generated close ([[What is NullPointerException]], [[How do you prevent a NullPointerException]]). If a non-null sibling resource’s `close` throws after a successful body, that is a different path ([[What happens if close throws after a try-with-resources body succeeds]]).

If a null resource is a bug, fail at the factory with `Objects.requireNonNull` before the `try` ([[What does Objects.requireNonNull do]]). Close exceptions from other resources still use `addSuppressed` when a primary exception exists ([[What is a suppressed exception in try-with-resources]]).

> [!warning] Null-tolerance is only for automatic close
> `try (var in = openOrNull()) { in.read(); }` still NPEs on `read`. TWR will not NPE on the way out if `in` is null.

> [!warning] `null` is not “initializer failed”
> A throwing constructor is abrupt completion. A null result is successful initialization of a null variable. The body runs; reverse-close simply ignores that slot.

> [!tip] Interview answer
> **If a try-with-resources resource is null, the generated close is skipped, so close does not NPE.** The try body still runs; using the resource there is a normal `NullPointerException`. Null is not the same as a constructor that throws.
