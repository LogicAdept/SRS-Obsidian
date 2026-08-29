<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS

# How would you explain the `throws` clause for checked exceptions?

> [!abstract] Short answer
> **It is the compile-time contract that this method or constructor may complete by throwing those checked types (or their subclasses).** For every checked exception the body can throw, `throws` must name that class or a **superclass**. Unchecked types may appear in `throws` but never have to. Catching the exception is the other legal alternative.

## Catch or specify — `throws` is the specify half

A checked exception that can leave a method or constructor must be handled: a matching `catch`, or a `throws` clause that mentions the type or a superclass ([[What happens if you neither catch nor declare a checked exception]], [[How would you explain Java exception handling try catch and propagation]], [[How do you propagate an exception up the call stack in Java]]). `throws IOException` covers `FileNotFoundException`; the reverse does not ([[Does throws IOException cover FileNotFoundException]]).

The names in `throws` must be subtypes of `Throwable`. Constructors use the same rule as methods ([[Can a constructor throw a checked exception]]). `main` may declare `throws`; an uncaught throw still hits the thread’s uncaught-exception handler ([[Can main throw exceptions outward and where are they handled]]).

Unchecked classes (`RuntimeException`, `Error`) are exempt. Listing them in `throws` is allowed and does **not** replace catching a checked type. Wrapping a checked exception in `RuntimeException` and throwing the wrapper also needs no `throws` for the cause ([[Does wrapping a checked exception in RuntimeException require a throws clause]]).

An override may not add checked types the parent is not allowed to throw ([[Can you override a RuntimeException throws clause with a checked exception]], [[What happens if an override declares a broader checked exception than the parent]]). A lambda’s `throws` comes from the **function type**, not from the enclosing method ([[Can a lambda throw a checked exception]]). A `static {}` block has no `throws` at all ([[Can a static initializer throw a checked exception]]).

```d2
direction: down
body: "body can throw checked E" {
  width: 300
  height: 50
}
choice: "catch E, or throws E (or super)" {
  width: 320
  height: 50
}
ok: "compiles" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
body -> choice -> ok
```

**Fig. 1.** `throws` documents which checked types callers must still deal with.

```java
class Demo {
    static void read() throws java.io.IOException {
        throw new java.io.FileNotFoundException("missing");
    }
}
```

**Listing 1.** The body throws a subclass. `throws IOException` is enough. Callers of `read` must catch or declare `IOException` (or a further superclass).

> [!warning] `throws Exception` is a wide contract
> It compiles, and it forces every caller to handle `Exception` — including `RuntimeException` if they catch that type at the call site. Prefer the specific checked types you actually throw.

> [!warning] `throws` is not a runtime filter
> The JVM still throws whatever object you `throw`. `throws` only satisfies the compiler. An override cannot “open” a parent that declared no checked exceptions.

> [!tip] Interview answer
> **`throws` is how a method advertises checked exceptions it does not catch.** Name the type or a superclass; `throws IOException` covers `FileNotFoundException`. Unchecked exceptions need no `throws`, and an override must not declare more checked types than the method it overrides.
