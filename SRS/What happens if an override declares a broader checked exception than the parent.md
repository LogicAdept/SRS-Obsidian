<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS

# What happens if an override declares a broader checked exception than the parent?

> [!abstract] Short answer
> **A compile-time error.** An override may not declare more checked exceptions than the method it overrides. Parent `throws FileNotFoundException` with child `throws IOException`, parent `throws IOException` with child `throws Exception`, or parent `throws IOException` with child `throws SQLException` are all illegal. A `Super`-typed call only has to handle the parent’s checked types, so a wider child `throws` could leak a type those callers never declared.

## The child’s checked set must be a subset (or narrower)

For every checked type `E` on the override, the parent must already list `E` or a **supertype** of `E`. That allows the same type, a **subtype** (`IOException` on the parent, `FileNotFoundException` on the child), a subset, or no checked `throws` at all. It forbids a **supertype** of a parent checked type, and any **unrelated** checked class ([[How do checked exceptions work with method overriding]], [[Does throws IOException cover FileNotFoundException]], [[How would you explain the throws clause for checked exceptions]]).

Implementing an interface method follows the same rule. The compile-time type of the reference still governs callers: `Super s = new Sub(); s.read();` is checked as `Super.read` ([[Must every caller catch exceptions declared in a throws clause]], [[How would you explain method overriding in Java]]).

`Exception` is broader than `IOException` even though both are checked. `Throwable` is broader still ([[Is Throwable a checked exception]]). Extra **unchecked** types on the override (`RuntimeException`, `IllegalArgumentException`, …) are allowed ([[Can you override a RuntimeException throws clause with a checked exception]], [[Must you declare RuntimeException in a throws clause]]). Return types may narrow independently ([[Can you declare a narrower return type when overriding a method]]).

```d2
direction: down
p: "parent throws FileNotFoundException" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
ok: "child throws FNF, a subtype, or nothing" {
  width: 340
  height: 50
  style.fill: "#e8f5e9"
}
bad: "child throws IOException, Exception,\nor SQLException — compile error" {
  width: 360
  height: 70
  style.fill: "#ffebee"
}
p -> ok
p -> bad
```

**Fig. 1.** Widen or add an unrelated checked type and the override does not compile.

```java
import java.io.FileNotFoundException;
import java.io.IOException;
import java.sql.SQLException;

class Super {
    void read() throws FileNotFoundException {}
}

class Wider extends Super {
    @Override
    void read() throws IOException {} // compile-time error
}

class Unrelated extends Super {
    @Override
    void read() throws SQLException {} // compile-time error
}

class Narrower {
    void read() throws IOException {}
}

class Ok extends Narrower {
    @Override
    void read() throws FileNotFoundException, IllegalArgumentException {}
}
```

**Listing 1.** `Wider` and `Unrelated` do not compile. `Ok` may **narrow** checked `throws` and add unchecked types.

> [!warning] `Exception` is not a harmless “more general IOException”
> Both are checked. `throws Exception` on the child is wider than `throws IOException` on the parent. Callers of `Super` who only catch `IOException` would miss a plain `Exception`.

> [!warning] Unchecked extras are not “more checked”
> `throws FileNotFoundException, RuntimeException` on the child is legal when the parent listed `FileNotFoundException`. The rule is checked-only. Dropping `throws` on the override still forbids throwing that checked type from the body unless you catch it.

> [!tip] Interview answer
> **It is a compile error — the override cannot declare a broader or unrelated checked exception.** `IOException` is broader than `FileNotFoundException`; `Exception` is broader than `IOException`; `SQLException` is unrelated. Extra `RuntimeException` types are allowed. Callers using the parent type only agreed to the parent’s checked `throws`.
