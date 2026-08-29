<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS

# How do checked exceptions work with method overriding?

> [!abstract] Short answer
> **An override may not declare more checked exceptions than the method it overrides.** It may repeat the parent types, replace them with subtypes, keep a subset, or declare none. Extra **unchecked** types are always allowed. Callers still follow the **compile-time** type’s `throws`, not the runtime override.

## The override may only shrink the checked set

The parent’s checked `throws` is the contract a caller using the superclass type is already forced to handle. The override must not add a checked class unless that class (or a supertype of it) already appears on the parent. Implementing an interface method follows the same rule ([[What happens if an override declares a broader checked exception than the parent]], [[How would you explain the throws clause for checked exceptions]]).

That permits:

- the same checked types as the parent
- **subtypes** (`throws IOException` on the parent, `throws FileNotFoundException` on the child) — [[Does throws IOException cover FileNotFoundException]]
- a **subset**, or no checked `throws` at all
- additional **unchecked** types (`RuntimeException`, `IllegalArgumentException`, …) even if the parent listed none ([[Can you override a RuntimeException throws clause with a checked exception]], [[Must you declare RuntimeException in a throws clause]])

It forbids a **new** checked class, a **supertype** of a parent checked type (`FileNotFoundException` on the parent, `IOException` or `Exception` on the child), or any checked `throws` when the parent declared none.

Order of types in `throws` does not matter; the rule is set membership, not list order.

```d2
direction: down
parent: "parent throws IOException" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
ok1: "child throws FileNotFoundException" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
ok2: "child throws nothing checked" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
bad: "child throws Exception\nor SQLException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
parent -> ok1
parent -> ok2
parent -> bad
```

**Fig. 1.** Narrow or drop checked `throws`; do not widen or add an unrelated checked type.

```java
import java.io.FileNotFoundException;
import java.io.IOException;

class Super {
    void read() throws IOException {}
}

class Narrow extends Super {
    @Override
    void read() throws FileNotFoundException {}
}

class Silent extends Super {
    @Override
    void read() {}
}
```

**Listing 1.** `Narrow` and `Silent` are legal. `void read() throws Exception` on a subclass of `Super` is a compile-time error.

```java
void caller(Super s) throws IOException {
    s.read();
}
```

**Listing 2.** The invocation is checked against `Super.read`. Even if `s` is a `Silent` at run time, the caller must still catch or declare `IOException` ([[Must every caller catch exceptions declared in a throws clause]]).

> [!warning] Dropping `throws` does not let the body throw the checked type
> If the override omits `throws IOException`, its body must catch that checked exception (or wrap it). Removing the clause only narrows the **signature**; it does not exempt the statements inside.

> [!warning] The superclass type still governs callers
> `Super s = new Silent(); s.read();` is compiled as `Super.read`. The caller is not allowed to ignore `IOException` just because this particular override declares none. That is why a wider checked `throws` on the child would break every `Super` client ([[How would you explain method overriding in Java]]).

> [!tip] Interview answer
> **The override’s checked `throws` must be the same types, subtypes, a subset, or empty — never a new or wider checked exception.** Unchecked `throws` can be added freely. Callers still handle whatever the compile-time type declared, even if the runtime method throws nothing checked.
