<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS

# Must every caller catch exceptions declared in a `throws` clause?

> [!abstract] Short answer
> **No.** A caller of a method that `throws` a **checked** type must **catch or specify** — catch it, or declare `throws` for that type or a superclass. Unchecked types listed in `throws` (`RuntimeException`, `Error`) do not force callers to do either. `main` may declare `throws` and never catch.

## Specify is as legal as catch

A method invocation **can throw** the checked types in that method’s `throws` clause (and what the argument expressions can throw). For each such checked type, **this** method’s body must catch it or mention it (or a superclass) in **its** `throws` ([[What happens if you neither catch nor declare a checked exception]], [[How would you explain the throws clause for checked exceptions]], [[If calling method A will throw an exception what should you do]]).

Propagating is normal: B calls A, B declares the same `throws`, C catches at the boundary ([[How do you propagate an exception up the call stack in Java]], [[How would you explain Java exception handling try catch and propagation]]). `main` may `throws IOException`; an uncaught throw still hits the uncaught-exception handler ([[Can main throw exceptions outward and where are they handled]]).

`throws RuntimeException` on A does **not** require B to catch or declare anything. Wrapping a checked exception in `RuntimeException` inside A also means B sees only the unchecked wrapper ([[Does wrapping a checked exception in RuntimeException require a throws clause]]).

A lambda is not a “caller” that inherits the enclosing method’s `throws`; it is limited by the **function type** ([[Can a lambda throw a checked exception]]).

```d2
direction: down
a: "A throws IOException" {
  width: 280
  height: 50
}
b: "B's choice" {
  width: 260
  height: 50
}
catch: "catch IOException" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
spec: "throws IOException" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
a -> b
b -> catch
b -> spec
```

**Fig. 1.** Every caller must **deal** with a checked `throws`. Catching is only one of the two legal deals.

```java
class Demo {
    static void a() throws java.io.IOException {
        throw new java.io.IOException("fail");
    }

    static void b() throws java.io.IOException {
        a();
    }

    static void c() {
        try {
            a();
        } catch (java.io.IOException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

**Listing 1.** `b` does not catch. `c` does. Both compile. A third method that calls `a()` with neither `catch` nor `throws` does not.

> [!warning] `throws Exception` on A still is not “must catch”
> Callers can `throws Exception` too. That only postpones the decision; it does not require a `catch` at every level.

> [!warning] Unchecked names in `throws` look mandatory and are not
> They document. They do not create a catch-or-specify obligation.

> [!tip] Interview answer
> **No. Callers must catch or declare checked exceptions from `throws`, not necessarily catch.** Unchecked types in `throws` do not force anything. `main` can declare `throws` and let the default uncaught handler run.
