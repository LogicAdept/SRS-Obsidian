<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/OOP/Initialization #SRS

# Which exception is thrown when static class initialization fails?

> [!abstract] Short answer
> **`ExceptionInInitializerError` when a `static` initializer or static field initializer throws a non-`Error` exception.** If that code throws an `Error` (for example `OutOfMemoryError`), that `Error` is **rethrown as-is**, not wrapped. Later use of the failed class throws `NoClassDefFoundError`. Checked exceptions cannot escape a `static { }` at compile time.

## Wrap `Exception`, rethrow `Error`, then `NoClassDefFoundError`

Class initialization runs static field initializers and `static { }` blocks as one block. If that work completes by throwing `E`, the VM records the `Class` as erroneous:

- If `E` is **not** an `Error`, the VM throws `ExceptionInInitializerError` with `E` as the cause (`getCause()`, also the older `getException()`).
- If `E` **is** an `Error` (`OutOfMemoryError`, `AssertionError`, …), that same `Error` is thrown. If wrapping would itself run out of heap, you get `OutOfMemoryError` instead.

`ExceptionInInitializerError` is a `LinkageError` ([[What is LinkageError]], [[How would you explain the java.lang.Error type hierarchy]], [[What is java.lang.Error]]). After a failed initialization, any later use of the class throws **`NoClassDefFoundError`**, not a second `ExceptionInInitializerError` ([[What happens if you use a class after ExceptionInInitializerError]], [[What is the difference between ClassNotFoundException and NoClassDefFoundError]]). Failed initialization is sticky: the class does not “try again” in the same loader.

If a **superclass** (or a required superinterface with default methods) fails first, that same exception is what this class’s initialization throws; this class is still marked erroneous.

A static initializer **cannot** declare `throws`. A checked exception must be caught (or wrapped) in the block ([[Can a static initializer throw a checked exception]], [[How would you explain static initializer blocks in Java]]).

Instance initializers `{ }` and instance field initializers run **after** the superclass constructor, as part of constructing **this** object. They do **not** go through class initialization. A throw from `{ }` comes out of `new` / the constructor unwrapped — not `ExceptionInInitializerError` ([[Can a constructor throw a checked exception]]).

`ThreadDeath` is an `Error`, so a static initializer that threw it would rethrow that `Error` ([[What is ThreadDeath]]).

```d2
direction: down
kind: "which initializer?" {
  width: 280
  height: 50
}
st: "static { } / static field" {
  width: 300
  height: 50
}
inst: "instance { } / instance field" {
  width: 300
  height: 50
}
wrap: "ExceptionInInitializerError\nunless E is already Error" {
  width: 320
  height: 70
  style.fill: "#fff8e1"
}
raw: "throw E as-is from new" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
kind -> st -> wrap
kind -> inst -> raw
```

**Fig. 1.** Class init wraps non-`Error` throws. Instance `{ }` does not. Later use of a failed class is `NoClassDefFoundError`.

```java
class Demo {
    static {
        throw new IllegalStateException("static");
    }
}

class InstanceFail {
    {
        throw new IllegalStateException("instance");
    }
}
```

**Listing 1.** First use of `Demo` throws `ExceptionInInitializerError` whose cause is the `IllegalStateException`. `new InstanceFail()` throws the `IllegalStateException` itself.

> [!warning] `catch (Exception)` misses the static-init failure
> `ExceptionInInitializerError` is an `Error`. The cause may be a `RuntimeException`, but the object you catch at the use site is the wrapper. Do not keep looking for `ExceptionInInitializerError` on every use after the class has already failed.

> [!warning] `{ }` in an instance is not this path
> A throw from an instance initializer comes out of the constructor, unwrapped. `ThreadDeath` is an `Error`: if it escaped a static initializer, the spec rethrows that `Error`, not a silent skip.

> [!tip] Interview answer
> **Static init that throws a non-`Error` becomes `ExceptionInInitializerError`.** An `Error` from that code is rethrown as itself. After that, using the class throws `NoClassDefFoundError`. Instance `{ }` failure is just that exception coming out of construction.
