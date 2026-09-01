<!--
reps: 0
priority: 0
-->
#Java/OOP/Inheritance #SRS

# Does Java support multiple inheritance for classes?

> [!abstract] Short answer
> **No.** A class has **at most one** direct superclass (`extends` names a single type). Every class except `Object` is a subclass of exactly one existing class. A class **may** `implements` **many** interfaces, and an interface **may** `extends` many interfaces. That is multiple inheritance of **interface types**, not of class implementation. Why one superclass: [[Why does Java disallow multiple class inheritance]]. Interfaces as the substitute: [[How does Java model multiple inheritance with interfaces]]. `Object` as root: [[Do Java classes inherit from Object explicitly or implicitly]].

## One `extends` class; many `implements` interfaces

The `extends` clause of a normal class names **the** direct superclass type. There is no comma-separated list of classes. `class C extends A, B` is a compile-time error. The superclass relation is a tree rooted at `Object` (plus enum/`Record` as implicit direct superclasses). Inheritance: [[What is inheritance]]. Syntax: [[Which Java syntax elements express inheritance]].

The `implements` clause lists **zero or more** interfaces (`InterfaceType, InterfaceType, …`). The same interface must not appear twice (even under two names). Superinterfaces of the superclass are superinterfaces of the class as well.

An interface’s `extends` clause uses that same list form: one interface may have many direct superinterfaces. There is no single root interface analogous to `Object`.

```d2
direction: down
obj: "Object" {
  width: 120
  height: 36
  style.fill: "#e3f2fd"
}
a: "class Animal" {
  width: 140
  height: 36
  style.fill: "#e8f5e9"
}
d: "class Duck\nextends Animal" {
  width: 180
  height: 48
  style.fill: "#e8f5e9"
}
fly: "interface Fly" {
  width: 140
  height: 36
  style.fill: "#fff3e0"
}
swim: "interface Swim" {
  width: 140
  height: 36
  style.fill: "#fff3e0"
}
obj -> a
a -> d
fly -> d: "implements"
swim -> d: "implements"
```

**Fig. 1.** Class inheritance is a single parent. Interface implementation (and interface-to-interface `extends`) can fan in.

```java
interface Fly {
    default String kind() {
        return "air";
    }
}

interface Swim {
    default String kind() {
        return "water";
    }
}

class Animal {}

class Duck extends Animal implements Fly, Swim {
    @Override
    public String kind() {
        return "both";
    }
}
```

**Listing 1.** One superclass (`Animal`), two superinterfaces. `kind()` must be overridden because both interfaces supply a default with the same signature. Default methods: [[How would you explain default interface methods since Java 8]].

```java
// Conceptual: does not compile
class Animal {}
class Vehicle {}
class FlyingCar extends Animal, Vehicle {} // two classes
class Redundant implements Cloneable, java.lang.Cloneable {} // same interface twice
```

**Listing 2.** Conceptual. Multiple class `extends` is illegal. Naming the same interface twice in `implements` is also illegal.

If two superinterfaces declare default methods that are override-equivalent, a class (or subinterface) that inherits both without overriding them is a compile-time error. The class must declare its own method (or make the class `abstract`). That conflict is **not** a second class superclass; it is incompatible inherited **interface** methods.

A class also cannot implement two different parameterizations of the same generic interface (or a parameterization and the raw type of that interface).

> [!warning] “Java has multiple inheritance now” usually means default methods
> Java 8 added bodies on interfaces. A class still has one superclass. Default methods can create a diamond **of interfaces**; you resolve it by overriding in the class, not by `extends A, B`.

> [!warning] `implements A, B` is not two implementations of state
> Interfaces have no instance fields. Shared constants are `public static final`. Instance state still lives on the single class hierarchy.

> [!warning] Mixins via more than one class still do not compile
> Abstract classes, inner classes, and `static` nested helpers do not add a second `extends` class. Composition (`has-a`) is the usual substitute when you need two concrete implementations.

> [!tip] Interview answer
> No. A Java class can extend only one class. It can implement many interfaces, and an interface can extend many interfaces. Default methods let you inherit behavior from several interfaces, but conflicting defaults must be overridden in the class. That is not multiple class inheritance.
