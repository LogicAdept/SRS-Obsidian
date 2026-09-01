<!--
reps: 0
priority: 0
-->
#Java/OOP/Polymorphism #SRS

# How would you explain method overriding in Java?

> [!abstract] Short answer
> An **instance** method in a subclass **overrides** a superclass (or superinterface) instance method when it has a **subsignature** of that method and the superclass method is inherited-or-would-be (not `private`, and package-private only in the same package). Invocation uses the **run-time class** of the object, not the compile-time type of the variable. `static` methods **hide**; constructors are **not** methods ([[Can you override a constructor the same way you override a method]]). vs overload: [[How would you explain Overload vs Override]]. Dispatch: [[How would you explain dynamic runtime polymorphism in Java]].

## Same signature, subclass body

A class **inherits** accessible instance methods whose signatures it does not declare. If it **does** declare an instance method whose signature is a subsignature of an inherited instance method, that declaration **overrides** (and, if the parent is `abstract`, **implements**). Signature: name + formal parameter types (and type parameters), **not** the return type. Overriding is **per signature**: other overloads of the same name stay inherited ([[How would you explain method overloading in Java]]).

**Contract.** The override must be **return-type-substitutable** (covariant reference types are allowed: [[Can you declare a narrower return type when overriding a method]]), must not declare **more checked exceptions** ([[What happens if an override declares a broader checked exception than the parent]]), and must be **at least as accessible** ([[Can you use a weaker access modifier when overriding a method]]). `@Override` is a compile-time check that a method really overrides or implements; it is not what makes overriding happen ([[How does the Override annotation work]]).

**Dispatch.** `Point p = new SlowPoint(); p.move(1, 1);` still runs `SlowPoint.move`. A cast to `Point` does **not** select the parent body. Only `super.move(...)` inside the subclass (or an enclosing type’s `Outer.super`) is non-virtual ([[How do you call an overridden superclass method in Java]]).

`final` instance methods cannot be overridden. `private` methods are not inherited, so a subclass “same signature” is a **new** method. `static` methods with the same signature **hide** ([[Can static methods be overridden in Java]]).

```d2
direction: down
v: "variable type Point\nchooses signature move(int,int)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
o: "run-time class SlowPoint\nruns SlowPoint.move" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
v -> o: "instance invoke"
```

**Fig. 1.** The compile-time type picks the signature. The run-time class picks the overriding body.

```java
class Point {
    int x, y;

    void move(int dx, int dy) {
        x += dx;
        y += dy;
    }
}

class SlowPoint extends Point {
    @Override
    void move(int dx, int dy) {
        super.move(dx / 2, dy / 2);
    }
}

class Use {
    static void go() {
        Point p = new SlowPoint();
        p.move(10, 10);
    }
}
```

**Listing 1.** `p.move` is `move(int,int)` from type `Point`, then `SlowPoint.move` runs. `super.move` is the only way to call the parent body.

> [!warning] `static` hides; it does not override
> `Parent.m()` vs `Child.m()` with the same signature is hiding. `Parent p = new Child(); p.m();` still runs `Parent.m` if both are `static`. An instance method cannot override a `static` one (compile-time error).

> [!warning] Cast does not undo an override
> `((Point) slow).move(1, 1)` is still virtual. `super` is the keyword that bypasses dispatch. Fields hide by name; methods do not.

> [!warning] `private` and `final` are not overridable
> A subclass method that matches a `private` parent method is unrelated: no `@Override`, no access/`throws` contract. `final` (and methods of a `final` class) cannot be overridden or hidden.

> [!tip] Interview answer
> Overriding replaces an inherited instance method with a subclass method of the same signature; the JVM looks up that method on the run-time class. The override cannot be less visible, cannot throw extra checked exceptions, and may narrow a reference return type. Static methods hide instead, constructors are not overridden, and only `super.m(...)` calls the parent implementation.
