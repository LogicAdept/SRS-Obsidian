<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS

# Can you throw an object that is not a `Throwable`?

> [!abstract] Short answer
> **No.** A `throw` expression must have a type assignable to `Throwable`, or be `null`. `throw "msg"`, `throw new Object()`, and throwing any other non-`Throwable` type are compile-time errors. `throw null` compiles, but at run time a `NullPointerException` is created and thrown instead of `null`.

## Only the `Throwable` hierarchy

Every exception object is an instance of the class `Throwable` (a direct subclass of `Object`) or of one of its subclasses. The two direct branches under it are `Exception` and `Error`. There is no interface you can throw: no interface type is assignable to `Throwable`, and a subclass of `Throwable` cannot be generic. See [[Is Throwable a class or an interface]] and [[What sits at the root of every Java exception]].

A `catch` parameter is under the same restriction: each type in the `catch` must be `Throwable` or a subclass. You cannot `catch (String e)`.

```d2
direction: down
throwable: "Throwable (class)" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
exc: "Exception" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
err: "Error" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}
other: "String, Object, interfaces\nnot throwable" {
  width: 260
  height: 70
  style.fill: "#eeeeee"
}
throwable -> exc
throwable -> err
```

**Fig. 1.** Only types under `Throwable` may appear in `throw` or `catch`. `Exception` and `Error` are siblings — [[Why is Error a sibling of Exception rather than a subclass]].

```java
class Demo {
    static void ok() {
        throw new IllegalStateException("allowed");
    }

    static void throwNull() {
        throw null;
    }
}
```

**Listing 1.** A `RuntimeException` is a `Throwable`. `throw null` compiles; evaluation produces a `NullPointerException`, not a null exception object.

```java
class Demo {
    static void illegal() {
        throw new String("no"); // compile-time error
    }
}
```

**Listing 2.** Conceptual: `String` is not assignable to `Throwable`.

By convention, application types should extend `Exception` (checked) or `RuntimeException` (unchecked), not `Throwable` itself ([[What is the difference between Throwable and Exception]]).

> [!warning] `throw null` is not “throwing a non-Throwable”
> The `null` reference is allowed as the `throw` expression. The JVM still throws a `Throwable` — a newly created `NullPointerException`. Catch `NullPointerException` or `RuntimeException`, not “null.”

> [!warning] A direct `Throwable` subclass is checked and misses `catch (Exception)`
> `class Weird extends Throwable {}` is a checked type (it is neither a run-time exception nor an error class). `throw new Weird()` needs `throws Weird` or an inner catch. `catch (Exception e)` and `catch (Error e)` both miss it; you need `catch (Weird)` or `catch (Throwable)` ([[Can you catch Throwable]], [[Do checked exceptions inherit Throwable directly]]).

> [!tip] Interview answer
> **No — you can throw only `Throwable` and its subclasses. `String` and `Object` will not compile. The one oddity is `throw null`, which compiles and becomes `NullPointerException` at run time. Declare custom types as `Exception` or `RuntimeException` subclasses, not as a direct `Throwable`.**
