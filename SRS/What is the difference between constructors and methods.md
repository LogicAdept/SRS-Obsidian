<!--
reps: 0
priority: 0
-->
#Java/OOP/Constructors #SRS

# What is the difference between constructors and methods?

> [!abstract] Short answer
> A **constructor** **initializes a new instance**. Its name is the **class’s simple name**, it has **no result type** (not `void`), it is **not a member**, and it is **never inherited or overridden**. It runs from `new`, `this(...)`, or `super(...)`, never from a method invocation. A **method** is a **member**: it has a **return type**, may be **`static` / `abstract` / `final`**, is **inherited** (if accessible), and **instance** methods **dispatch** on the run-time class. Constructor: [[What is constructor]]. Not override: [[Can you override a constructor the same way you override a method]]. Class body: [[What does a Java class consist of]].

## Same-looking syntax, different roles

**Constructor.** Looks like a method with no result. Cannot be `abstract`, `static`, `final`, `native`, `synchronized`, or `strictfp`. Access still applies (`private` constructors exist). If you declare none, the compiler synthesizes a default ([[How would you explain the default constructor synthesized by the Java compiler]]). Several constructors = **overloading**, resolved at `new` ([[What is constructor overloading in Java]]). `{ }` instance initializers run after `super`, not as methods ([[How would you explain instance initializer blocks versus constructors]]). Longer: [[What is constructor]].

**Method.** `int m()`, `void m()`, `static void m()`. Members: inherited, hidden (`static`), or overridden (instance) ([[How would you explain Overload vs Override]]; [[How would you explain method overloading in Java]]). Called as `obj.m()` or `Type.m()`. May `return` a value. `void Point()` in class `Point` is a **method**, not a constructor.

**Return of `new`.** The expression `new C(args)` yields a reference to the new object. The constructor does not `return` that reference as a method result; `return;` only exits the constructor body.

```d2
direction: down
ctor: "constructor C(int)\nnot a member, new / this / super" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
m: "method void m()\nmember, obj.m() / C.m()" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Construction vs a call on an existing object (or on the class, if `static`).

```java
class Point {
    int x;

    Point(int x) {
        this.x = x;
    }

    void Point() {
        x = 0;
    }

    int x() {
        return x;
    }
}

class Use {
    static int go() {
        Point p = new Point(1);
        p.Point();
        return p.x();
    }
}
```

**Listing 1.** `new Point(1)` is the constructor. `p.Point()` is the `void` method. `x()` is a normal instance method. `go()` returns `0`.

> [!warning] `void C()` is not a constructor
> Missing return type is required. `void` is a return type. Subclasses never inherit constructors; they inherit methods (if accessible). `new Child()` does not search `Parent(int)` as a constructor of `Child`.

> [!warning] No virtual constructors
> You cannot override `Parent()` in `Child`. You can overload constructors in each class separately. Instance methods of the same signature override.

> [!warning] `this` in both is not the same phase
> In a constructor, `this` is the object under construction; instance `{ }` have already run after `super`. In a method, construction has finished (unless you called the method from a constructor—then overrides can see unset fields).

> [!tip] Interview answer
> A constructor initializes a new object, has the class name and no return type, and is not a member, so it is not inherited or called as `obj.C()`. A method is a member with a return type, may be static or abstract, and instance methods are dispatched on the run-time class. `void C()` is a method. Both can be overloaded; only methods can be overridden.
