<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/Exceptions/Unchecked #SRS

# Can you override a `RuntimeException` throws clause with a checked exception?

> [!abstract] Short answer
> **No.** An override may not declare **more checked** exceptions than the method it overrides. `throws RuntimeException` names an unchecked type, so the parent's *checked* set is empty. `throws IOException` or `throws Exception` on the override is a compile-time error.

## Only checked types are constrained

An override (or a method that implements an interface method) may not be declared to throw more checked exceptions than the overridden method. If the override lists any checked type `E`, the parent must have a `throws` clause, and `E` or a **supertype** of `E` must appear in that clause (after erasure). Unchecked types (`RuntimeException`, `Error`, and subclasses) do not expand that set. It is permitted, but not required, to mention them on either declaration — see [[Must you declare RuntimeException in a throws clause]].

A caller typed as the parent is only prepared for checked types the parent declared. If the override could throw `IOException`, that contract would break. The same rule is why a parent with no `throws` at all also forbids a checked `throws` on the child ([[What happens if an override declares a broader checked exception than the parent]], [[How do checked exceptions work with method overriding]]).

```d2
direction: down
parent: "Parent.m() throws RuntimeException\nchecked set: empty" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
childOk: "Child.m()\nor throws ArithmeticException" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
childBad: "Child.m() throws IOException\nor throws Exception" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
parent -> childOk: "narrower / unchecked"
parent -> childBad: "compile-time error"
```

**Fig. 1.** `RuntimeException` in `throws` is not a license to add `Exception` or `IOException`.

```java
import java.io.IOException;

class Parent {
    void m() throws RuntimeException {
        throw new ArithmeticException("fail");
    }
}

class ChildBad extends Parent {
    @Override
    void m() throws IOException { // compile-time error
        throw new IOException("io");
    }
}

class ChildOk extends Parent {
    @Override
    void m() {
        throw new IllegalStateException("still unchecked");
    }
}
```

**Listing 1.** `ChildBad` does not compile. `ChildOk` may omit `throws` or declare other unchecked types. The body still cannot throw a checked type unless it is caught or wrapped.

```java
class ChildWrap extends Parent {
    @Override
    void m() {
        try {
            throw new java.io.IOException("io");
        } catch (java.io.IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```

**Listing 2.** Wrapping is a body-level workaround, not a change to the override rule — see [[Does wrapping a checked exception in RuntimeException require a throws clause]].

> [!warning] `throws Exception` is not “compatible” with `throws RuntimeException`
> `Exception` is a **checked** superclass of `RuntimeException`. Listing it on the override adds a checked type the parent did not permit. Callers of `Parent` catch only what `Parent` declared; they need not catch `Exception`. The direction that is legal is the opposite: a parent `throws Exception` may be overridden with `throws IOException` (a checked subtype) or with no checked `throws` at all.

> [!warning] Removing `throws` does not let the body throw checked
> If you drop `throws IOException` so the override compiles, an uncaught `throw new IOException()` in the body is then a different compile-time error: the method can throw a checked type not named in *its own* `throws`. Catch it, wrap it, or do not throw it.

> [!tip] Interview answer
> **No. You cannot override `throws RuntimeException` with `throws IOException` or `throws Exception`. Unchecked names in `throws` are optional documentation and do not create a checked contract, so the child's checked set must stay empty. Wrap the checked exception in a `RuntimeException`, or catch it inside the override.**
