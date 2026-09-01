<!--
reps: 0
priority: 0
-->
#Java/OOP/Constructors #Java/Language #SRS

# What is constructor overloading in Java?

> [!abstract] Short answer
> **Constructor overloading** is several constructors in **one class** with **different parameter-type lists**. Behavior matches **method overloading**: the compiler picks a signature from the **compile-time** types of the `new C(...)` arguments. Constructors are **not** methods and **cannot be overridden** ([[Can you override a constructor the same way you override a method]]). Method overload: [[How would you explain method overloading in Java]]. vs override: [[How would you explain Overload vs Override]]. What a constructor is: [[What is constructor]].

## Same class name, different signatures

A constructor’s **signature** is the class name plus formal parameter types (and type parameters, if any)—not `throws`, not parameter names. Two constructors with override-equivalent signatures in one class are a compile-time error. Different arities or types are overloads. `Point()` and `Point(int x, int y)` overload; `Point(Point p)` is a **copy constructor by convention**, still just another overload ([[How would you explain copy constructors or defensive copying in Java]]; [[How do default copy and parameterized constructors differ]]).

**Resolution.** Each class instance creation expression is resolved at **compile time**, like a method call: argument count and static types, then strict / boxing / varargs phases. There is no run-time “constructor dispatch” on the object’s class—the class is already named in `new`.

**Default constructor.** If you declare **any** constructor, the implicit no-arg default is **not** created ([[How would you explain the default constructor synthesized by the Java compiler]]). Write `C() { this(defaults); }` if you still want no-arg. `this(...)` may chain overloads; `super(...)` is not overloading.

Chaining and bodies: [[What is constructor]].

```d2
direction: down
n: "new Point(...)\ncompile-time types" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
a: "Point()" {
  width: 120
  height: 32
  style.fill: "#e8f5e9"
}
b: "Point(int, int)" {
  width: 160
  height: 32
  style.fill: "#fff8e1"
}
n -> a
n -> b
```

**Fig. 1.** `new` chooses one constructor signature before the object exists.

```java
class Point {
    int x, y;

    Point() {
        this(0, 0);
    }

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    Point(Point p) {
        this(p.x, p.y);
    }
}

class Use {
    static void go() {
        Point a = new Point();
        Point b = new Point(1, 2);
        Point c = new Point(b);
    }
}
```

**Listing 1.** Three overloads. `Point()` chains to `Point(int, int)`. `new Point(b)` binds `Point(Point)`, not `Point(int, int)`.

> [!warning] Any declared constructor kills the default
> After you add `Point(int, int)`, `new Point()` is a compile-time error until you write `Point()` yourself. That is not overloading failure; the implicit constructor is gone.

> [!warning] Not overriding, not hiding
> A subclass `Child(int x)` does not replace `Parent(int x)`. It is a different class’s constructor. `new Child(1)` never runs `Parent(int)` unless `Child` calls `super(1)`.

> [!warning] Parameter names and `throws` do not distinguish overloads
> `Point(int x)` and `Point(int y)` are the same signature. Return type does not apply. Boxing/`null` can make `Point(Object)` vs `Point(String)` ambiguous, same as methods.

> [!tip] Interview answer
> Constructor overloading is several constructors with different parameter types in one class. `new` picks one at compile time from the argument types, the same way overloaded methods work. It is not overriding. If you declare any constructor, you must also declare a no-arg one if you still want `new C()`.
