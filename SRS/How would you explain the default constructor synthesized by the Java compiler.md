<!--
reps: 0
priority: 0
-->
#Java/OOP/Constructors #SRS

# How would you explain the default constructor synthesized by the Java compiler?

> [!abstract] Short answer
> If a class (top-level, member, or local) **declares no constructors**, a **default constructor is implicitly declared**: **no formal parameters** (except the enclosing instance of a non-`private` inner member class), **no `throws`**, same access as the class (or package access if the class has none), body `super();` (`Object`’s is empty). If you declare **any** constructor, this implicit one is **not** created. It is **not** a copy constructor. vs copy / parameterized: [[How do default copy and parameterized constructors differ]]. Constructors: [[What is constructor]].

## Implicit `C() { super(); }`

The compiler does not invent a constructor at run time. The language **inserts a constructor declaration** when the class body has none. `public class Point { int x, y; }` is equivalent to adding `public Point() { super(); }`. Access matches the class: a `public` class gets a `public` default constructor; a package-private class gets a package-private one.

**When it is absent.** One explicit constructor—`private`, overloaded, or parameterized—**suppresses** the default. Then `new C()` is a compile-time error unless you also write a no-arg constructor. That is how utility classes kill `new` ([[How would you explain private constructors and common patterns that use them in Java]]).

**`super()` must work.** The implicit constructor has no `throws` and calls the superclass no-arg constructor. If the superclass has only `Parent(int)` (or a no-arg that is inaccessible or declares checked exceptions), the subclass that declares no constructor **fails to compile**.

**Not inherited, not overridable** ([[Can you override a constructor the same way you override a method]]). Instance `{ }` still run after that `super()` ([[How would you explain instance initializer blocks versus constructors]]). Enums: an undeclared constructor is **`private`**. Records get a **canonical** constructor, not this no-arg default. Copy constructors are a **convention** you write; nothing is synthesized from `C(C other)`.

The dump’s `public class ClassName() {}` is not legal Java (constructor syntax mixed into the class header).

```d2
direction: down
none: "no constructor declarations" {
  width: 240
  height: 36
  style.fill: "#e3f2fd"
}
def: "implicit C() { super(); }\nsame access as the class" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
any: "any explicit constructor" {
  width: 220
  height: 36
  style.fill: "#ffebee"
}
no: "no default constructor" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
none -> def
any -> no
```

**Fig. 1.** The default constructor exists only when the class declares none.

```java
public class Point {
    int x, y;
}

class Named {
    String n;

    Named(String n) {
        this.n = n;
    }
}

class Use {
    static void go() {
        Point p = new Point();
        Named q = new Named("a");
    }
}
```

**Listing 1.** `Point` compiles as if it declared `public Point() { super(); }`. `Named` declares a constructor, so `new Named()` would not compile.

> [!warning] “Default” is not “the no-arg constructor you wrote”
> `Point() { }` that you type is an **explicit** constructor. It happens to look like the default, but you declared it, so further constructors do not bring back a second implicit one. Interviewers use “default” only for the **implicit** case.

> [!warning] Any constructor suppresses it, including `private C() {}`
> You cannot keep the synthesized no-arg constructor and also add `C(int)`. Write both if you need both. A copy constructor `C(C other)` is extra source, never generated.

> [!warning] Superclass no-arg is required
> `class Child extends Parent {}` needs `Parent()` accessible and without a checked `throws`. Inner classes: the default constructor also takes the enclosing instance; `new Inner()` from the wrong place can fail even when `Inner` is visible.

> [!tip] Interview answer
> If you declare no constructors, the compiler supplies a no-arg default constructor with the same access as the class and a body that calls `super()`. If you declare any constructor, that implicit one disappears. It is not a copy constructor, it is not inherited, and it is a compile-time error if the superclass has no accessible no-arg constructor without checked exceptions.
