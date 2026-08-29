<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/OOP/Initialization #SRS

# Can a static initializer throw a checked exception?

> [!abstract] Short answer
> **No.** In a named class or interface, if a `static { ... }` block or a static field initializer *can throw* a checked exception, that is a compile-time error. There is no `throws` clause on a static initializer. Catch the checked type **inside** the initializer, or wrap it in an unchecked throwable. Unchecked types are not banned at compile time.

## No `throws` on class initialization

A static initializer runs when the class is initialized, together with static field initializers, in textual order. Exception checking for both is the same rule: a checked type that can escape a static initializer or a class-variable initializer of a **named** class or interface is illegal. The initializer is not a method, so you cannot declare `throws IOException` on it.

```d2
direction: down
src: "static { ... } or\nstatic field initializer" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
check: "can throw checked E?" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
err: "compile-time error" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
ok: "catch E inside, or throw\nonly unchecked / Error" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
src -> check
check -> err: "yes, uncaught"
check -> ok: "no"
```

**Fig. 1.** Catch-or-specify has no `throws` target here, so the checked type must not be a possible result of the initializer. See [[What happens if you neither catch nor declare a checked exception]].

```java
import java.io.IOException;

class Config {
    static String load() throws IOException {
        throw new IOException("missing");
    }

    static {
        try {
            load();
        } catch (IOException e) {
            throw new ExceptionInInitializerError(e);
        }
    }
}
```

**Listing 1.** Legal: `IOException` is caught inside the block. `static { load(); }` and `static String s = load();` do not compile.

That is stricter than constructors and instance initializers. An instance initializer of a named class may throw a checked type if the class has at least one explicit constructor and **every** constructor names that type (or a supertype) in `throws` — see [[Can a constructor throw a checked exception]]. A lambda body is checked against the *target function type*, not banned outright — see [[Can a lambda throw a checked exception]].

> [!warning] Wrapping does not skip initialization failure
> If the initializer completes abruptly with a `RuntimeException` (or any throwable that is not an `Error`), class initialization replaces it with `ExceptionInInitializerError` whose argument is that exception. Throwing `ExceptionInInitializerError` yourself is already an `Error`, so it is not wrapped again. After a failed initialization, later use of the class raises `NoClassDefFoundError`. See [[Which exception is thrown when static class initialization fails]] and [[What happens if you use a class after ExceptionInInitializerError]].

> [!warning] The block must still be able to complete normally
> A static initializer that cannot complete normally is a compile-time error on its own (`return` is also illegal there). `static { throw new RuntimeException("fail"); }` is therefore illegal even though `RuntimeException` is unchecked. Catch-and-rethrow-unchecked still compiles when the `try` has a successful path.

> [!tip] Interview answer
> **No — a static initializer and a static field initializer of a named class cannot let a checked exception escape; there is no `throws` to attach. Catch it inside the block or wrap it in an unchecked throwable. An uncaught `RuntimeException` during class initialization still becomes `ExceptionInInitializerError`; an `Error` is not wrapped.**
