<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #Java/OOP #SRS

# How do you invoke a static method on a Java interface?

> [!abstract] Short answer
> Write **`InterfaceName.method(...)`** — a type name, then the method. A class method on an interface is invoked **without** a particular object. It is **not** a member of implementing classes or of subinterfaces, so `impl.method()`, `ImplementingClass.method()`, and `SubInterface.method()` do not see it. An expression qualifier (`p.show()`) is a **compile-time error** for a `static` method **declared in an interface**. What they are: [[How would you explain static methods on Java interfaces]]. Versus class `static`: [[How would you explain static methods in Java]]. Versus `default`: [[How would you explain default interface methods since Java 8]].

## Type name, not a receiver

An interface may declare `static` methods. They have a block body. With no access modifier they are implicitly `public`; `private static` is allowed (callable only from the declaring interface). `static` cannot be combined with `abstract` or `default`. `this` and `super` are illegal in that static context.

Because neither a class nor a subinterface **inherits** `static` methods from superinterface types, those types are not searched for the name. The legal qualified form is `TypeName.method(...)`, and that compile-time declaration **must** be `static`. `TypeName` has to be the interface that **declares** the method (or a static import of that method, which then allows an unqualified `method(...)`).

`InterfaceName.super.method(...)` is for **default** (instance) methods in a superinterface, not for `static` ones.

```java
interface Paper {
    static void show() {
        System.out.println("show");
    }

    static Paper blank() {
        return new Paper() {};
    }
}

class Licence implements Paper {
    void print() {
        Paper.show();
        Paper p = Paper.blank();
        // p.show();           // illegal: expression qualifier
        // Licence.show();     // illegal: not inherited by the class
        // show();             // illegal: not a member of Licence
    }
}
```

**Listing 1.** Call site is the interface type. Factories such as `blank()` are the usual reason to have a class method on the interface.

```java
interface Sub extends Paper {
    static void demo() {
        Paper.show(); // OK: TypeName is the declaring interface
        // show();    // illegal: Sub does not inherit show
    }
}
```

**Listing 2.** Conceptual (needs `Paper` from Listing 1). A subinterface qualifies with the declaring type; it does not inherit the class method.

```d2
direction: down
decl: "static method declared on Paper" {
  width: 260
  height: 44
  style.fill: "#fff8e1"
}
ok: "Paper.show()\n(or static import)" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
noInst: "p.show() / this.show()" {
  width: 240
  height: 48
  style.fill: "#ffcdd2"
}
noCls: "Licence.show() / Sub.show()" {
  width: 260
  height: 48
  style.fill: "#ffcdd2"
}
decl -> ok: "TypeName is Paper"
decl -> noInst: "Primary / ExpressionName"
decl -> noCls: "not inherited"
```

**Fig. 1.** Class methods of an interface are not inherited and must not be invoked through an instance expression.

A `static` method on an interface also cannot hide a `public` instance method of a superinterface, and an interface cannot declare a method override-equivalent to a `public` method of `Object` unless it is `abstract`. Those are declaration errors, not invocation tricks. Hiding vs override for class methods: [[Can static methods be overridden in Java]].

> [!warning] Unlike `static` methods of a **class**
> `instance.staticMethod()` is a legal (if misleading) form when the method is declared on a **class**. The same shape is illegal when the method is declared on an **interface**.

> [!warning] `implements` does not import the name
> An implementing class can call `Paper.show()` but cannot treat `show` as its own static member. Copying a same-signature `static` method onto the class is a **different** method, not an override.

> [!tip] Interview answer
> You invoke a static interface method as InterfaceName.method, or via a static import of that method. Implementing classes and subinterfaces do not inherit it, so you cannot call it on an instance or as ImplementingClass.method. That is different from static methods on classes, which may be written on an instance or a subclass type.
