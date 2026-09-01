<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #Java/OOP/Polymorphism #SRS

# Can static methods be overridden in Java?

> [!abstract] Short answer
> **No.** A `static` method is a **class method**. A subclass method with an override-equivalent signature **hides** it; it does **not** override it. There is no runtime dispatch on the class method: the **compile-time type** of the qualifier (or the named class) chooses which `static` method runs. Instance methods override; class methods hide. Hiding vs “override or”: [[Can static method be override or]]. `static` itself: [[How would you explain static methods in Java]]. Overload vs override: [[How would you explain Overload vs Override]].

## Hide at compile time; instance methods still dispatch

Overriding applies to **instance** methods. If class C declares instance method `mC` that would override `mA`, it is a compile-time error when `mA` is `static`. The other mix is also illegal: a `static` method cannot hide an instance method.

When both sides are `static` and the subclass signature is a subsignature of the superclass class method, the subclass method **hides** the superclass one. A hidden class method is still callable through a qualifier whose compile-time type is the declaring class, or through `super`. `@Override` is legal only when the method actually overrides a supertype method (or a few `Object` / record-accessor cases). On a hiding `static` method it is a compile-time error.

Overload resolution is always compile-time. If the chosen signature is an instance method, the JVM then looks up an override. If it is a class method, that choice is final. Binding: [[What is the difference between static and dynamic binding in Java]]. Different parameter lists with one `static` and one instance method are overloading, not overriding: [[Can an instance method overload a static method in Java]].

```d2
direction: down
call: "s.greeting()  s has type Super\nruntime class Sub" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
st: "static greeting\ncompile-time type Super" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
inst: "instance name\nruntime class Sub" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
call -> st
call -> inst
```

**Fig. 1.** Same receiver, two rules: class methods follow the variable’s type; instance methods follow the object’s class.

```java
class Super {
    static String greeting() {
        return "Goodnight";
    }

    String name() {
        return "Richard";
    }
}

class Sub extends Super {
    static String greeting() {
        return "Hello";
    }

    @Override
    String name() {
        return "Dick";
    }
}

class Demo {
    public static void main(String[] args) {
        Super s = new Sub();
        System.out.println(s.greeting() + ", " + s.name());
        System.out.println(Sub.greeting());
    }
}
```

**Listing 1.** Prints `Goodnight, Dick` then `Hello`. `s.greeting()` is `Super.greeting`. `s.name()` is `Sub.name`. Prefer `Super.greeting()` / `Sub.greeting()` so the hiding is obvious.

```java
// Conceptual: does not compile
class Super {
    static void m() {}
    void n() {}
}

class Sub extends Super {
    @Override static void m() {} // hiding is not overriding
    void m() {}                  // instance cannot override static
    static void n() {}           // static cannot hide instance
}
```

**Listing 2.** Conceptual. `@Override` does not apply to hiding. Mixing `static` and instance on an override-equivalent signature is illegal either way.

A class does not inherit `static` methods from superinterfaces. `InterfaceName.m()` is a different rule set, not override: [[How would you explain static methods on Java interfaces]]. `final` on a class method blocks hiding: [[How would you explain the final modifier on a static method in Java]].

> [!warning] `Super s = new Sub(); s.staticMethod()` looks like polymorphism and is not
> The compiler uses the type of `s`. Replacing `s` with a `Sub` at run time does not change which class method runs. That is the usual interview trap.

> [!warning] Same name and parameters is hiding, not a second override
> You can still call the hidden method via `Super.m()` or `super.m()` from the subclass. That is field-like hiding, not `super` as in instance override dispatch of the runtime type.

> [!warning] A `static` method on an interface is not overridden by the implementing class
> Classes do not inherit interface `static` methods. Declaring `static void m()` on the class does not override `I.m()`; it is a separate class method. Call `I.m()` or `C.m()` by name.

> [!tip] Interview answer
> No. Static methods are not overridden and do not take part in instance polymorphism. A subclass static method with the same signature hides the superclass class method, and the compile-time type of the qualifier picks which one runs. Instance methods still override as usual. `@Override` on a static method is a compile-time error.
