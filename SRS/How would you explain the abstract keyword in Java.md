<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Abstract #Java/OOP #SRS

# How would you explain the abstract keyword in Java?

> [!abstract] Short answer
> **`abstract` on a class** means the class is incomplete: you cannot write `new AbstractType(...)`. **`abstract` on a method** means signature, result, and `throws` — **no body**. A normal class that has (or inherits) an `abstract` method must itself be `abstract`. A concrete subclass must implement those methods. Do not use `abstract` merely to block `new`; use a `private` constructor for that. Versus interfaces: [[When should you use an abstract class versus an interface]]. `abstract` + `static`: [[Can a method be abstract and static at the same time]]. Enums: [[Can a Java enum have abstract methods]].

## Incomplete type, missing implementation

An `abstract` class may still have constructors, fields, and concrete methods. Instantiating a **concrete** subclass runs the abstract class’s constructor and instance field initializers. You may declare a class `abstract` even if it declares no `abstract` methods — the type is still incomplete. You must declare it `abstract` if any member method, declared or inherited, is `abstract` (including an un-overridden package-access `abstract` method from a superclass).

An `abstract` method lives in an `abstract` class, except in an **enum** body (every constant then needs a class body that implements it). You cannot write `abstract enum`. A non-`abstract` subclass of an `abstract` class must implement `m`, or it is a compile-time error. An `abstract` class may override an `abstract` method with another `abstract` method (docs, covariant return, narrower `throws`). A **concrete** instance method may be overridden to become `abstract`.

`abstract` on a method cannot combine with `private`, `static`, `final`, `native`, `strictfp`, or `synchronized`. A class cannot be both `abstract` and `final`. Every interface is implicitly `abstract` (the modifier on the interface is obsolete). Interface methods that are not `private`, `default`, or `static` are implicitly `abstract`: [[How would you explain default modifiers for fields and methods inside interfaces]].

If the only goal is “nobody calls `new`,” declare at least one constructor, make them all `private`, and invoke none of them from outside — that is how `java.lang.Math` is shaped, not `abstract`.

```java
abstract class Point {
    int x = 1, y = 1;

    void move(int dx, int dy) {
        x += dx;
        y += dy;
        alert();
    }

    abstract void alert();
}

class SimplePoint extends Point {
    void alert() { }
}

class Demo {
    void run() {
        Point p = new SimplePoint();
        p.move(1, 0);
        // Point q = new Point(); // compile-time error
    }
}
```

**Listing 1.** `Point` must be `abstract` because `alert` has no body. `new SimplePoint()` is legal and still runs `Point`’s field initializers.

```java
abstract class Named {
    abstract String label();
}

abstract class ColoredNamed extends Named {
    abstract int rgb();
}
```

**Listing 2.** `ColoredNamed` stays `abstract` because it inherits `label()` and adds another `abstract` method. No `abstract` method is required on a class that you merely mark incomplete.

```d2
direction: down
abs: "abstract class\n(+ optional abstract methods)" {
  width: 260
  height: 48
  style.fill: "#fff8e1"
}
newA: "new AbstractType()" {
  width: 200
  height: 40
  style.fill: "#ffcdd2"
}
sub: "concrete subclass\nimplements abstract methods" {
  width: 280
  height: 48
  style.fill: "#e8f5e9"
}
newS: "new Subclass() OK\n(super constructor still runs)" {
  width: 280
  height: 48
  style.fill: "#e3f2fd"
}
abs -> newA: "compile-time error"
abs -> sub
sub -> newS
```

**Fig. 1.** `abstract` blocks direct instantiation. Completing subclasses are ordinary types.

> [!warning] `abstract` is not a utility-class lock
> `abstract` advertises that **subclasses should exist** to finish the type. A `final` class with a `private` constructor is the opposite design. A bare `new Point()` is a compile-time error; `new Point() { void alert() {} }` is a different type (an anonymous subclass).

> [!warning] `super.abstractMethod()` does not work
> Overriding a concrete method (for example `Object.toString`) to be `abstract` hides the parent implementation from `super`. Provide a separate concrete hook if subclasses still need it. `abstract static` is illegal.

> [!tip] Interview answer
> Abstract on a class means the type is incomplete and you cannot instantiate it. Abstract on a method means no body; then the class must be abstract too, and a concrete subclass must implement it. Use abstract when you want subclasses to fill in behavior, not merely to forbid new. Interfaces are a different kind of incomplete type: their abstract methods are implied unless you write default, static, or private.
