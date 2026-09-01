<!--
reps: 0
priority: 0
-->
#Java/OOP/Polymorphism #SRS

# How would you explain dynamic runtime polymorphism in Java?

> [!abstract] Short answer
> **Runtime (dynamic) polymorphism** is **instance-method overriding**: the compiler picks a signature from the **compile-time type** of the qualifier; the JVM then looks up that method starting at the **run-time class** of the object. `Point p = new ColoredPoint(); p.clear();` runs `ColoredPoint.clear`. Fields, `static` methods, and `private` methods do **not** do this. `super.m()` and `static` invocation **forbid** overriding. Overriding: [[How would you explain method overriding in Java]]. Overload vs override: [[How would you explain Overload vs Override]]. Polymorphism in general: [[What is polymorphism]].

## Compile-time signature, run-time class

A method invocation is processed in two phases. **Compile time** finds a **most specific** method for the name and argument types, using the type of `p` (here `Point`). **Run time**, if the invocation mode is **`virtual`** or **`interface`**, lookup starts at class **R**, the actual class of the target (`ColoredPoint`). Walk superclasses until a method that **overrides** that compile-time declaration is found; else search superinterface defaults. `this` is the target object. If the target is `null`, `NullPointerException`. What polymorphism is: [[What is polymorphism]]. Mechanisms: [[What mechanisms implement polymorphism in Java]].

That is why `Point.move` calling `clear()` still hits `ColoredPoint.clear` when `this` is a `ColoredPoint`. Inheritance: [[How would you explain class inheritance in Java and tradeoffs]].

**Not dynamic**

| Form | Dispatch |
| Instance method, `virtual`/`interface` | Dynamic (overriding allowed) |
| `super.m()` | Superclass body; overriding **not** allowed ([[How do you call an overridden superclass method in Java]]) |
| `static` method | Compile-time type; hiding, not override ([[Can static methods be overridden in Java]]) |
| `private` instance method | The declaration in that class; not overridden |
| Field `p.x` | Compile-time type of `p` (hiding, not overriding) |

Overloading (`move(int)` vs `move(int,int)`) is resolved **before** run time. Two overloads are not runtime polymorphism.

```d2
direction: down
src: "p.clear()\np : Point" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
ct: "compile time\nsignature clear() in Point" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
rt: "run time\nR = p.getClass()\nwalk to overriding clear" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
src -> ct
ct -> rt
```

**Fig. 1.** The variable’s type selects the signature. The object’s class selects the body.

```java
class Point {
    int x, y;

    void move(int dx, int dy) {
        x += dx;
        y += dy;
        clear(); // virtual on this
    }

    void clear() {
        System.out.println("Point");
        x = 0;
        y = 0;
    }
}

class ColoredPoint extends Point {
    int color;

    @Override
    void clear() {
        System.out.println("ColoredPoint");
        super.clear();
        color = 0;
    }
}

class Test {
    static void go() {
        Point p = new ColoredPoint();
        p.move(1, 1); // ColoredPoint.clear, then Point.clear
        ((Point) p).clear(); // still ColoredPoint.clear
    }
}
```

**Listing 1.** `p` is typed `Point` and refers to a `ColoredPoint`. Every virtual `clear()` uses the subclass. `super.clear()` does not.

> [!warning] A cast does not pick the superclass method
> `((Point) p).clear()` still starts lookup at the **run-time** class. Only `super.clear()` (inside the subclass) is non-virtual.

> [!warning] Overloading is not “runtime polymorphism”
> Which `print` overload runs is fixed when the call compiles. Which **override** of that chosen signature runs depends on the object. Mixing the two words is the usual interview miss.

> [!warning] `static` and fields look polymorphic and are not
> `Parent p = new Child(); p.staticMeth();` uses `Parent`’s `static` method (and is a bad style). `p.field` is `Parent`’s field if `Child` hides one. Dynamic dispatch is **instance methods** that override.

> [!tip] Interview answer
> Dynamic polymorphism in Java is virtual invocation of overridden instance methods: the compiler binds a signature using the reference type, and at run time the JVM searches from the object’s class for the overriding body. That is why Point p = new ColoredPoint(); p.clear() runs ColoredPoint.clear, including when Point.move calls clear() on this. Static methods, private methods, and fields are not dispatched that way; super.method() is deliberately non-virtual.
