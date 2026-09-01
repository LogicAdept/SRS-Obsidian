<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #Java/OOP #SRS

# Can instance methods overload?

> [!abstract] Short answer
> **Yes.** An instance method may share a name with a class (`static`) method. That is **overloading** whenever the signatures are **not override-equivalent**. `static` is **not** part of a signature: only the name, type parameters, and formal parameter types count. Two methods with override-equivalent signatures in one class are a **compile-time error**, whether one is static or not. Overloading: [[How would you explain method overloading in Java]]. Versus override: [[How would you explain Overload vs Override]]. Class methods: [[How would you explain static methods in Java]].

## Same name, different signature

A class method is invoked without a particular object as `this`. An instance method is always invoked with respect to an object. Those two kinds of members are still just methods of the class. If they have the same name and signatures that are not override-equivalent — one declared, both declared, or one inherited — the name is overloaded. The compiler picks a signature from the argument types at the call site. Only if that chosen method is an instance method does the JVM then look up an override at run time.

Return type, `throws`, and `static` versus instance do **not** make a new signature. `foo(int)` static next to `foo(int)` instance is the same signature twice.

The same rule applies across a superclass: a subclass instance method with a **different** parameter list overloads an inherited static name. A subclass instance method with an **override-equivalent** signature does **not** overload it; that attempted declaration tries to override a static method and is illegal. Static methods are not overridden at all: [[Can static methods be overridden in Java]].

```java
class Mix {
    static String id(int n) {
        return "class:" + n;
    }

    String id() {
        return "instance";
    }

    static String both() {
        Mix m = new Mix();
        String fromClass = Mix.id(1); // "class:1"
        String fromObj = m.id();      // "instance"
        String viaRef = m.id(2);      // "class:2" — still the class method
        return fromClass + "/" + fromObj + "/" + viaRef;
    }
}
```

**Listing 1.** `id(int)` and `id()` overload each other. `m.id(2)` is a class-method call written on an instance; there is no `this` inside `id(int)`.

```java
class Super {
    static void log(String msg) {}
}

class Sub extends Super {
    void log(int code) {}          // legal: overloads the inherited name
    // void log(String msg) {}     // illegal: instance method cannot override a static method
}

class Broken {
    static int value() { return 1; }
    // int value() { return 2; }   // illegal: override-equivalent signatures in one class
}
```

**Listing 2.** Conceptual: comments mark the two compile-time errors — same signature in one class, and an instance method trying to override a static method.

```d2
direction: down
name: "same simple name" {
  width: 180
  height: 40
  style.fill: "#fff8e1"
}
sig: "signatures override-equivalent?" {
  width: 240
  height: 44
  style.fill: "#e3f2fd"
}
overload: "overloading\n(static + instance OK)" {
  width: 220
  height: 48
  style.fill: "#e8f5e9"
}
sameClass: "compile error\nin one class" {
  width: 180
  height: 48
  style.fill: "#ffcdd2"
}
inherit: "compile error\noverride or hide" {
  width: 180
  height: 48
  style.fill: "#ffcdd2"
}
name -> sig
sig -> overload: "no"
sig -> sameClass: "yes, both declared here"
sig -> inherit: "yes, subclass mixes static/instance"
```

**Fig. 1.** Overloading cares about signatures, not `static`. Mixing static and instance on an **equivalent** signature is never a legal overload.

> [!warning] `static` does not split the signature
> `static void f(int x)` and `void f(int x)` in the same class do not overload. They are override-equivalent, so the class body is illegal. Changing only the return type does not help.

> [!warning] Overload is not override, and the reverse mix is also illegal
> A subclass **instance** method cannot override a superclass **static** method. A subclass **static** method cannot hide a superclass **instance** method. Those are compile-time errors, not overloads. A legal overload still binds the class-method alternative at compile time: `Super s = new Sub(); s.staticName(...)` uses `Super`, not the run-time class.

> [!tip] Interview answer
> Yes — an instance method can overload a static method when the parameter lists differ, because `static` is not part of the signature. Same name and same parameters in one class is a compile error even if one is static. That is overloading, not overriding: an instance method cannot override a static method, and a static method cannot hide an instance method.
