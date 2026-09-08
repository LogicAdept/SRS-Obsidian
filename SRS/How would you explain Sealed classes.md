<!--
reps: 0
priority: 0
-->
#Java/Language #Java/Versions/17 #SRS

# How would you explain Sealed classes?

> [!abstract] Short answer
> A **sealed** class or interface names every **direct** subtype that may extend or implement it. After `extends` / `implements` you write `permits Circle, Square`. Those types must live in the **same named module**, or the **same package** if the sealed type is in the unnamed module. Each permitted type is exactly one of `final`, `sealed`, or `non-sealed`. Standard from **Java 17** (JEP 409). That closed list is what later lets a pattern `switch` be exhaustive without `default`.

## `permits` closes the next layer, not the whole tree

```d2
direction: down
root: "sealed class Shape\npermits Circle, Square, Rectangle" {
  width: 340
  height: 70
  style.fill: "#e3f2fd"
}
fin: "final class Circle\nno further subclasses" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
open: "non-sealed class Square\nunknown subclasses allowed" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
again: "sealed class Rectangle\npermits FilledRectangle" {
  width: 280
  height: 60
  style.fill: "#fff8e1"
}
root -> fin
root -> open
root -> again
```

**Fig. 1.** Sealing controls **direct** subtypes. `final` stops the line; `sealed` continues a closed list; `non-sealed` opens it again.

The point is modeling a **fixed set of kinds**, not reuse-by-subclassing. `Shape` can still have methods and fields; clients simply cannot invent a fourth direct subtype. Same-file nested types may **omit** `permits`: the compiler takes every same-compilation-unit class that lists this type as its direct superclass and has a canonical name. No `permits` and no such types is a compile error. A `permits` clause without `sealed` is also a compile error.

Each permitted type must **directly** extend or implement the sealed type, be accessible at compile time, and sit in that same module or package. Local and anonymous classes cannot be permitted (they have no canonical name) and cannot extend a sealed type. A class with a sealed direct superclass that is not `final`, `sealed`, or `non-sealed` (explicitly or implicitly) does not compile. `non-sealed` is illegal unless there **is** a sealed direct superclass or superinterface — you cannot sprinkle it on a freely extensible class.

Records are implicitly `final`, so they are legal permitted subtypes ([[What is a Java record]]). An enum is implicitly `final` or implicitly `sealed`, so it can implement a sealed interface. Versus an enum of singletons: [[When would you use a sealed class instead of an enum]]. `final` on a class is the one-type closed set ([[What does the final keyword mean in Java]]).

```java
sealed interface Shape permits Circle, Square, Rectangle {}

record Circle(double radius) implements Shape {}

non-sealed class Square implements Shape {
    double side;
}

sealed class Rectangle implements Shape permits FilledRectangle {
    double length, width;
}

final class FilledRectangle extends Rectangle {}

class Area {
    static double of(Shape s) {
        return switch (s) {
            case Circle c -> Math.PI * c.radius() * c.radius();
            case Square q -> q.side * q.side;
            case Rectangle r -> r.length * r.width;
        };
    }
}

// class Triangle implements Shape {}  // illegal: not permitted
```

**Listing 1.** Three ways to continue sealing. `Circle` is a record (implicitly `final`). `Square` is `non-sealed`. `Rectangle` stays sealed. Covering every permitted type makes this Java 21 pattern `switch` exhaustive — no `default`.

At run time `Class.isSealed()` is true for a sealed type; `getPermittedSubclasses()` then returns a non-null array of those direct permitted types (empty if none could be loaded). For a non-sealed type, primitive, `void`, or array, `isSealed()` is false and `getPermittedSubclasses()` returns `null`.

Because the compiler knows the permitted set, some casts become illegal: if no permitted lineage can share an instance with the target type, the types are **disjoint** and the cast is a compile error (the null reference is the only shared value). `non-sealed` in the middle of the tree can reopen that.

> [!warning] Exhaustive `switch` is Java 21 patterns, not a sealed-class feature
> Sealing landed as a **standard** modifier in **17**. Pattern `switch` was **preview in 17** and **final in 21**. A sealed type does not make a classic constant `switch` exhaustive. What sealing gives you is a known set of subtypes so a type-pattern `switch` can omit `default` when every permitted kind is listed ([[How do records work with pattern matching in switch]], [[How would you explain Java 17 21]]). `non-sealed` anywhere in that set breaks the closed proof.

> [!warning] `permits` is same module, not “same JAR”
> In a named module every permitted type must be in **that** module; they may sit in different packages. In the unnamed module they must share the **package**. A subclass in another Maven module that is not the same Java module is rejected. Omitting `final` / `sealed` / `non-sealed` on a permitted class is a compile error, not a default of `final`.

> [!tip] Interview answer
> **`sealed` plus `permits` names every direct subtype; those types must be in the same module, or the same package in the unnamed module, and each must be `final`, `sealed`, or `non-sealed`.** Records fit because they are already `final`. Standard in Java 17. The payoff with Java 21 pattern `switch` is exhaustiveness over that list — sealing itself does not turn an old `switch` into a type switch.
