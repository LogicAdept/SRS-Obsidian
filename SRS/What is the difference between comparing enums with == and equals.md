<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/HashCodeEquals #SRS

# What is the difference between comparing enums with `==` and `equals`?

> [!abstract] Short answer
> **For enum constants they agree on the result:** both are identity checks. The language permits `==` because each constant has one instance. Prefer `==` in practice: it is null-safe on either operand and rejects a cross-type compare at compile time. `equals` is `final` on `Enum` and still throws if the receiver is null.

## Why both mean identity

JLS §8.9.1: there is only one instance of each enum constant, so you may use `==` instead of `equals` when at least one reference is known to be an enum constant. The same section states that `Enum.equals` is `final` and performs an identity comparison (via `super.equals` / equivalent to `==`).

OpenJDK’s `Enum.equals` is literally:

```java
public final boolean equals(Object other) {
    return this == other;
}
```

**Listing 1.** Identity equality from `java.lang.Enum` (JDK 21). `hashCode` is also `final` and uses identity hashing.

You cannot override enum equality to mean “same name” or “same fields” — [[When should you override equals in Java]]. Cloning is blocked so the singleton property holds; see [[How does an enum provide a Singleton]].

```d2
direction: down
const: "Color.RED\n(one instance)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
eqEq: "a == b" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
eqMeth: "a.equals(b)" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
same: "Same boolean result\n(identity)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

const -> eqEq -> same
const -> eqMeth -> same
```

**Fig. 1.** Same constant ⇒ both true; different constants ⇒ both false. The differences are null-safety and typing, not value semantics.

```java
enum Color { RED, GREEN }

Color a = Color.RED;
Color b = Color.RED;
Color c = Color.GREEN;

a == b;          // true
a.equals(b);     // true
a == c;          // false
a.equals(c);     // false
```

**Listing 2.** Same-type constants: `==` and `equals` match.

## Where they diverge

| Situation | `==` | `equals` |
| --- | --- | --- |
| Left / receiver is `null` | `false` (no NPE) | `NullPointerException` |
| Two different enum types | Compile error | Compiles; returns `false` |
| Same constant after serialization / `valueOf` | Still the same instance | Same `true` |

```java
Color left = null;
Color right = Color.RED;

left == right;       // false
left.equals(right);  // NPE

enum Size { RED }
Color.RED.equals(Size.RED); // false — compiles (Object argument)
// Color.RED == Size.RED;   // compile error — incompatible types
```

**Listing 3.** Null-safety and cross-type typing are the practical differences. Cross-type `compareTo` also does not compile for distinct enum types; [[What is the difference between ordinal and compareTo on a Java enum]].

`Objects.equals(a, b)` is another null-safe option, but for enum-typed locals `==` is the usual style.

> [!warning] Do not treat enum `equals` like `String.equals`
> For `String`, `==` and `equals` can disagree. For enums they must not: equality is identity. Writing `name().equals(...)` to “be safe” adds no correctness over `==` on the constants themselves and can hide a wrong comparison (string vs enum).

> [!warning] Null receiver still breaks `equals`
> `someEnum.equals(Color.RED)` is only safe if `someEnum` is non-null. [[How would you explain someObj.equals(null)]] is the general null-argument rule; here the trap is a **null receiver**. Prefer `someEnum == Color.RED` when the left side may be null.

> [!tip] Interview answer
> **`==` and `Enum.equals` are both identity checks, and the JLS allows `==` because each constant is a singleton.** Prefer `==`: no NPE if one side is null, and different enum types fail at compile time. `equals` is `final` on `Enum`, so you cannot redefine enum equality.
