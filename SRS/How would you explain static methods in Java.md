<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #Java/OOP #SRS

# How would you explain static methods in Java?

> [!abstract] Short answer
> A **`static` method** is a **class method**: it is invoked **without** a particular object as `this`. Its body is a **static context** — no `this` / `super`, no unqualified instance fields or instance methods. You still **may** call instance methods if you have an object in hand. Prefer `ClassName.method(...)`. Hiding, not override: [[Can static method be override or]]. Interface form: [[How do you invoke a static method on a Java interface]]. Versus instance members: [[What is the difference between an instance member and a static member in Java]].

## No current instance

An instance method always runs with respect to an object, which becomes `this`. A class method does not. That is why `abstract` cannot be combined with `static`, and why a receiver parameter (`Foo this`) is illegal on a class method.

Invocation of a class method uses invocation mode `static`. `TypeName.method(...)` has no target reference. If you write `expr.method(...)` and `method` is a **class** method declared on a **class**, `expr` is still evaluated and then **discarded** — it is not `this`, and it is **not** checked for `null`. A `static` method declared on an **interface** must not be invoked that way at all.

A subclass `static` method with an override-equivalent signature **hides** the superclass class method. The compile-time type of the qualifier chooses which class method runs. An instance method cannot override a `static` method; a `static` method cannot hide an instance method. Different signatures are ordinary overloading, even mixing `static` and instance: [[Can an instance method overload a static method in Java]]. `main`: [[Why is the main method static in Java]].

```java
class Counter {
    int n;

    static int zero() {
        return 0;
    }

    static int from(Counter c) {
        return c.n; // object supplied as an argument, not as this
    }

    int bump() {
        return ++n;
    }
}

class Demo {
    static void go() {
        System.out.println(Counter.zero());
        Counter c = new Counter();
        System.out.println(Counter.from(c));
        System.out.println(c.bump());
        // System.out.println(n);    // illegal: no instance
        // System.out.println(this); // illegal in a static context
    }
}
```

**Listing 1.** Class methods talk to the class, or to an object they were **passed**. They do not get `this` for free.

```java
class Test1 {
    static void mountain() {
        System.out.println("Monadnock");
    }
    static Test1 favorite() {
        System.out.print("Mount ");
        return null;
    }
    public static void main(String[] args) {
        favorite().mountain(); // prints "Mount Monadnock" — no NPE
    }
}
```

**Listing 2.** `favorite()` is evaluated; the `null` result is discarded because `mountain` is `static`.

```d2
direction: down
call: "Counter.zero() / c.zero()" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
mode: "invocation mode static" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
body: "static context\nno this / super" {
  width: 220
  height: 48
  style.fill: "#e8f5e9"
}
npe: "null receiver is not this\n(no NPE for class methods)" {
  width: 260
  height: 48
  style.fill: "#ffcdd2"
}
call -> mode -> body
call -> npe: "expr.method discarded"
```

**Fig. 1.** Class method calls do not bind `this`. A null expression qualifier is still evaluated for side effects.

> [!warning] “Static methods can call only static methods” is false
> They cannot use **unqualified** instance members. `from(Counter c) { return c.n; }` is legal. What is illegal is `n` or `bump()` with no receiver inside `zero()`.

> [!warning] `instance.staticMethod()` is not polymorphism
> For a class method it is legal and misleading; hiding follows the **compile-time** type. For an interface `static` method it is a **compile-time error**. `null.staticMethod()` on a class does not throw NPE.

> [!tip] Interview answer
> A static method is a class method: no this, no instance fields unless you pass an object in. Call it as ClassName.method. It is hidden, not overridden, so the compiler picks it from the compile-time type. Writing it on an instance is allowed for class methods and does not use that instance as this.
