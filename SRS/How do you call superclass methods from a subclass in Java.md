<!--
reps: 0
priority: 0
-->
#Java/OOP/Inheritance #SRS

# How do you call superclass methods from a subclass in Java?

> [!abstract] Short answer
> **Inherited** instance methods are members of the subclass: call them with a **simple name** (`move(1)`) or `this.move(1)`. If the subclass **overrides** that method, the simple name is **virtual** (the override); reach the superclass body with **`super.move(1)`**. **Constructors** are not methods — chain with **`super(...)`**. **`private`** superclass methods are **not inherited** and cannot be called. Overridden case: [[How do you call an overridden superclass method in Java]]. Inheritance: [[What is inheritance]]. Overriding: [[How would you explain method overriding in Java]].

## Inherited member, `super.m()`, or `super(...)`

A subclass’s members include those **inherited** from the direct superclass, except `private` members. `protected` and `public` (and package-access in the **same** package) instance methods are therefore callable as if declared in the subclass. Access: [[How do Java access modifiers work]]. `protected`: [[How does protected]].

**No override.** `move(dx)` is the inherited method. There is nothing extra to write.

**Override.** The subclass method **hides** that inherited instance method from simple-name lookup for that signature. `super.m(...)` searches the **direct superclass** and invokes **without** further overriding. A cast `((Super) this).m()` does **not** skip the override. Detail: [[How do you call an overridden superclass method in Java]].

**Constructor.** Constructors are **not members** and are **not inherited** ([[Can you override a constructor the same way you override a method]]). A subclass constructor calls a superclass constructor with `super(...)` (or `this(...)` then eventually `super`). If you write no explicit constructor invocation, `super();` is inserted.

**`static`.** Concrete `static` methods **are** inherited from the **superclass** (not from superinterfaces). They are **not overridden** ([[Can static methods be overridden in Java]]). Prefer `Super.m()`; a subclass declaration with the same signature **hides** the inherited one.

```d2
direction: down
need: "subclass needs Super's behavior" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
inh: "not overridden\nmove(dx) / this.move(dx)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
ovr: "overridden instance\nsuper.move(dx)" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
ctor: "constructor\nsuper(x, y)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
need -> inh
need -> ovr
need -> ctor
```

**Fig. 1.** Simple name for inherited instance methods. `super.m` when you overrode them. `super(...)` for construction.

```java
class Point {
    int x;

    Point(int x) {
        this.x = x;
    }

    void move(int dx) {
        x += dx;
    }

    private void reset() {
        x = 0;
    }

    static int origin() {
        return 0;
    }
}

class ColoredPoint extends Point {
    int color;

    ColoredPoint(int x, int color) {
        super(x); // superclass constructor, not a method
        this.color = color;
    }

    @Override
    void move(int dx) {
        super.move(dx); // Point.move
        color++;
    }

    void bump() {
        move(1); // ColoredPoint.move (virtual)
    }

    int fromInheritedStatic() {
        return origin(); // Point.origin, unless hidden
    }

    // void wipe() { reset(); } // compile-time error: private, not inherited
}
```

**Listing 1.** `bump` uses the override. `super.move` uses `Point`. `super(x)` constructs. `reset` is invisible. `origin` is an inherited class method.

> [!warning] After you override, the simple name is the subclass method
> `move(1)` inside `ColoredPoint` is `this.move(1)`, so it is **virtual**. Forgetting `super` when you meant the original body is a recursion / logic bug, not an access error.

> [!warning] `private` superclass methods are not on the subclass
> `reset()` in `ColoredPoint` does not compile. Same-class `private` access does not extend to subclasses. Package-access methods are inherited only in the **same package**.

> [!warning] `super()` is not `super.m()`
> `super(args)` must appear as the constructor invocation (after any prologue). It never selects an overridden **method**. There is no `super.Point(x)`.

> [!tip] Interview answer
> If the subclass does not override the method, call it by name — it is inherited. If it does override, super.method(...) runs the direct superclass body without virtual dispatch; a cast to the superclass does not. Constructors are chained with super(...), and private superclass methods cannot be called at all.
