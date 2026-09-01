<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Inheritance #SRS

# What is inheritance?

> [!abstract] Short answer
> **Inheritance** is declaring a class (or interface) **from existing types** so it **gains members** of those types. In Java a class has **one** superclass (`extends`; `Object` if omitted) and any number of superinterfaces (`implements`). The subclass **is-a** the parent ([[What do in OOP expressions is-a and has-a]]). **Constructors and `{ }` / `static { }` are not inherited** ([[What does a Java class consist of]]). Tradeoffs: [[How would you explain class inheritance in Java and tradeoffs]]. Multiple class inheritance: [[Does Java support multiple inheritance for classes]]. `Object`: [[Do Java classes inherit from Object explicitly or implicitly]].

## Subclass reuses members, not constructors

**What is inherited.** Accessible fields, methods, and nested types of the superclass and superinterfaces become members of the subclass unless a same-signature instance method **overrides** ([[How would you explain method overriding in Java]]) or a field **hides**. `private` members are not inherited. Package-private members are inherited only in the same package.

**What is not.** Constructors. Static and instance initializers. You write `super(...)` (or get `super()` from the default constructor). A subclass that declares no constructor still does **not** inherit `Parent(int)` ([[How would you explain the default constructor synthesized by the Java compiler]]).

**Why.** Subtype polymorphism: a `Car` variable can refer to a `Sedan` ([[What is polymorphism]]). Shared implementation: protected helpers, common fields. Principles: [[What are the main oop principles]]. Encapsulation still applies: do not inherit to reach private state ([[What is encapsulation]]).

The dump’s factory story is is-a reuse. The phone sample is incomplete (`AbstractPhone` never shown; `WirelessPhone` is `abstract` without the methods `CellPhone` claims to override). “Little new code” is a side effect, not the definition—and a deep `extends` chain is costly.

```d2
direction: down
p: "Point\nx, y, move" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
c: "ColoredPoint extends Point\ncolor" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
p -> c: "inherits members"
```

**Fig. 1.** `ColoredPoint` is a `Point`. It does not inherit `Point`’s constructors.

```java
class Point {
    int x, y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    void move(int dx, int dy) {
        x += dx;
        y += dy;
    }
}

class ColoredPoint extends Point {
    int color;

    ColoredPoint(int x, int y, int color) {
        super(x, y);
        this.color = color;
    }
}

class Use {
    static void go() {
        Point p = new ColoredPoint(1, 2, 0xff0000);
        p.move(1, 0);
    }
}
```

**Listing 1.** `ColoredPoint` inherits `move`. `Use` treats it as a `Point`. `new ColoredPoint` must call `super`; there is no inherited `Point(int, int)` to invoke as a constructor of `ColoredPoint`.

> [!warning] Inheritance is not “copy the parent’s constructors”
> `new ColoredPoint(1, 2)` is a compile-time error unless you declare that constructor. `super` is required (explicitly or as `super()` in a default constructor).

> [!warning] `implements` is inheritance of types
> A class inherits abstract/default methods from interfaces too. That is still is-a, not has-a. You cannot `extends` two classes.

> [!warning] Less source is not automatically better
> The dump’s `Smartphone extends CellPhone extends …` is the fragile-base-class shape. If you only needed `install`, a field (has-a) plus forwarding is often cheaper. Inherit for **substitutability**, not for two methods.

> [!tip] Interview answer
> Inheritance means a new class is declared as a subclass (or an interface as a subinterface) and receives accessible members of the parent types. In Java that is one `extends` and many `implements`. Constructors are not inherited. Use it for is-a relationships and polymorphism, not as a way to steal a couple of methods.
