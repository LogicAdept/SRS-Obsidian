<!--
reps: 0
priority: 0
-->
#Java/Language #Java/OOP/Polymorphism #SRS

# What is the difference between static and dynamic binding in Java?

> [!abstract] Short answer
> **Binding** is choosing **which method body** a call runs. **Static (early) binding** is finished **before** the object’s run-time class matters: **overload** resolution, **`static`** methods, **`private`** methods, **`super.m()`**. **Dynamic (late) binding** is **instance** `virtual` / `interface` lookup from the **run-time class**—overriding ([[How would you explain dynamic runtime polymorphism in Java]]; [[How would you explain method overriding in Java]]). The **signature** is **always** chosen at **compile time** ([[How would you explain Overload vs Override]]). Typing: [[How would you explain static typing in Java]].

## Signature first, then maybe a vtable

**Compile time (every call).** Name, argument types, accessibility → one **descriptor**. That is already static binding of **which overload** ([[How would you explain method overloading in Java]]). A `Parent` variable never “sees” a `Child.m(String)` that is only an overload.

**Then run time, only for some instance calls.** Invocation mode `virtual` or `interface`: if the method is not `private`, start at the target object’s class and find the method that **overrides** that signature ([[What is polymorphism]]; [[What is polymorphism]]). That is dynamic binding. `null` → `NullPointerException` first.

**Still static at run time.**

- **`static`:** no target for dispatch; `Parent p = new Child(); p.m();` still runs `Parent.m` if both are `static` ([[Can static methods be overridden in Java]]).
- **`private`:** the compile-time class’s method; not overridden.
- **`super.m()`:** the superclass body, not virtual ([[How do you call an overridden superclass method in Java]]).
- **Constructors:** not methods; `new` is not dynamic dispatch.

**`final`.** A `final` instance method **cannot be overridden**, so the body is unique and the JVM may inline it. Private methods “behave as final” for overriding. The dump’s “all Java methods are late-bound unless `final`” **skips `static`, overloads, `private`, and `super`**. Message passing: [[What is message passing in object oriented programming]].

```d2
direction: down
sig: "compile time\nwhich signature?" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
dyn: "run time (instance virtual)\nwhich body?" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
st: "static / private / super\nthat body, no lookup" {
  width: 260
  height: 45
  style.fill: "#fff8e1"
}
sig -> dyn
sig -> st
```

**Fig. 1.** Overload resolution is always static. Only some instance calls then look up an override.

```java
class Parent {
    static String kind() {
        return "P";
    }

    String name() {
        return "P";
    }
}

class Child extends Parent {
    static String kind() {
        return "C";
    }

    @Override
    String name() {
        return "C";
    }
}

class Use {
    static String go() {
        Parent p = new Child();
        return p.kind() + p.name();
    }
}
```

**Listing 1.** `go()` returns `"PC"`. `p.kind()` is a `static` call on type `Parent`. `p.name()` is dynamically bound to `Child.name`.

> [!warning] Not every method is late-bound
> The dump’s “all methods except `final`” is a classroom shortcut. `static` hides. Overloads are chosen from **compile-time** argument types. `private` and `super` skip override lookup.

> [!warning] `final` is “cannot override,” not a third kind of `new`
> A `final` instance method is still invoked as an instance method. There is simply no subclass body that can replace it. Do not say `final` methods are “called like `static`.”

> [!warning] Two `int` overloads are not dynamic polymorphism
> `f(Object)` vs `f(String)` with `Object x = "a"; f(x);` is **static** binding to `f(Object)`. Dynamic binding needs an **overridden instance** method on `x`.

> [!tip] Interview answer
> Static binding decides the method signature at compile time and is used for overloads, static methods, private methods, and `super`. Dynamic binding looks up an instance method on the run-time class after that signature is fixed—that is overriding. Java does not late-bind every call; `final` only forbids further overrides. `Parent p = new Child(); p.staticM()` still runs `Parent.staticM`.
