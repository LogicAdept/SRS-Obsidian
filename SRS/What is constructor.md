<!--
reps: 0
priority: 0
-->
#Java/OOP/Constructors #SRS

# What is constructor?

> [!abstract] Short answer
> A **constructor** initializes a **new instance**. Its name is the **simple name of the class**; it has **no result type** (not even `void`). It is **not a member** and **not a method**: you do not call it with `obj.C()`. It runs from `new C(...)`, from `this(...)` / `super(...)`, and a few implicit creations (for example some `String` concatenations). Longer mechanism: [[What is the difference between constructors and methods]]. Not overridable: [[Can you override a constructor the same way you override a method]]. Default: [[How would you explain the default constructor synthesized by the Java compiler]]. Class body: [[What does a Java class consist of]].

## Looks like a method, is not one

The declarator is `ClassName(params)` with optional type parameters. Access may be `public`, `protected`, `private`, or package. It cannot be `abstract`, `static`, `final`, `native`, `synchronized`, or `strictfp`. Body: optional `this(...)` or `super(...)`, then the rest; instance `{ }` run after `super` ([[How would you explain instance initializer blocks versus constructors]]).

**Role.** After memory is allocated and fields get defaults, the constructor (and chained superclass constructors) set the instance up. Several constructors in one class is **overloading** ([[What is constructor overloading in Java]]), not overriding. If you declare none, the compiler supplies a no-arg default.

**Dump.** “Special method, no return type, same name as the class, runs on `new`” is the usual sentence. The error is **method**: constructors are never invoked by method invocation expressions and are not inherited. `void Point()` is a **method** named `Point`, not a constructor.

Private constructors: [[How would you explain private constructors and common patterns that use them in Java]].

```d2
direction: down
n: "new Point(1, 2)" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
c: "constructor Point(int, int)\nnot a member" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
o: "initialized instance" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
n -> c
c -> o
```

**Fig. 1.** `new` selects a constructor. That is not a method call.

```java
class Point {
    int x, y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    void Point() {}
}

class Use {
    static Point go() {
        return new Point(1, 2);
    }
}
```

**Listing 1.** `Point(int, int)` is the constructor. `void Point()` is an ordinary instance method. `new Point(1, 2)` does not call `void Point()`.

> [!warning] No return type means no `void`
> `void C()` is a method. A constructor is `C()`. You do not `return` a value; `return;` is allowed only as leaving the body. The result of `new` is the new reference, not a value the constructor returned.

> [!warning] Same name as the class is required
> If the identifier is not the class’s simple name, it is not a constructor. Constructors are not inherited; a subclass must declare its own or take the default `super()`.

> [!warning] `new` is not the only trigger
> `this(...)` and `super(...)` invoke constructors. String concatenation and boxing can create instances too. You still never write `p.Point(1, 2)` to construct.

> [!tip] Interview answer
> A constructor initializes a new object. It has the class’s name and no return type, and it is not a method or a member, so it cannot be inherited or overridden. It runs when you use `new` (or `this`/`super`). If you write none, the compiler adds a no-arg default constructor.
