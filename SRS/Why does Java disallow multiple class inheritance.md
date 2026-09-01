<!--
reps: 0
priority: 0
-->
#Java/Language #Java/OOP/Inheritance #SRS

# Why does Java disallow multiple class inheritance?

> [!abstract] Short answer
> A class has **one direct superclass**. That superclass’s **implementation** (fields, constructors, instance methods) is what the subclass is **derived from**. Two superclasses would mean two instance layouts and two constructor chains to merge. Java still allows **many superinterfaces**: multiple **types**, and `default` methods with an **error unless you override** a conflict. Rule: [[Does Java support multiple inheritance for classes]]. Interfaces: [[How does Java model multiple inheritance with interfaces]]. Syntax: [[Which Java syntax elements express inheritance]].

## One class implementation, many types

**`extends` is singular.** Every class except `Object` is a subclass of **one** existing class. Enums and records have a fixed superclass (`Enum`, `Record`). The superclass is the source of the **class** implementation the subclass continues ([[What is inheritance]]).

**What that avoids.** Instance **fields** and **constructors** live on classes, not on interfaces. One superclass means one field layout and one `super(...)` chain. Two concrete parents that both declared `int x` or both had constructors would not have a single derivation rule.

**What is still multiple.** `implements I, J` (and interface `extends I, J`) is multiple inheritance of **type**. `default` methods are multiple inheritance of **behavior**, but two inherited defaults with the same signature are a **compile-time error** until the class (or subinterface) **overrides**. A method from the **superclass** already overrides a matching interface `default`, so the class line stays the implementation spine.

Need a second “parent” for reuse without a type? Use a **field** (composition), not a second `extends` ([[Why is composition often recommended over inheritance]]; [[What are alternatives to class inheritance]]).

```d2
direction: down
cls: "one extends (state + constructors)" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}
iface: "many implements (types + defaults)" {
  width: 280
  height: 45
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Class inheritance is a single implementation spine. Interfaces add types (and optional defaults).

```java
class Animal {
    int energy;
}

interface Fly {
    default String mode() {
        return "air";
    }
}

interface Swim {
    default String mode() {
        return "water";
    }
}

class Duck extends Animal implements Fly, Swim {
    public String mode() {
        return "both";
    }
}
```

**Listing 1.** `Duck` has one superclass, `Animal`, so `energy` has one layout. It implements two interfaces; it **must** override `mode()` because `Fly` and `Swim` both supply a default. `class Duck extends Animal, Vehicle` would not compile.

> [!warning] “Java has no multiple inheritance” is too short
> It has no multiple **class** inheritance. It has multiple **interface** inheritance. Since default methods, it also has multiple inheritance of **implementation**, with an explicit conflict error ([[How would you explain default interface methods since Java 8]]).

> [!warning] Interfaces still do not inherit instance state
> You cannot put an instance field on an interface and get two parents’ fields that way. Constants (`public static final`) are not per-object state.

> [!warning] A second abstract class is still a second class
> `abstract class` uses the same single `extends` slot as a concrete class. If you already `extend` one type, the other API must be an interface ([[What is the difference between a Java interface and an abstract class]]).

> [!tip] Interview answer
> Java allows one superclass so a class has one field layout and one constructor chain to derive from. Multiple inheritance of type is done with interfaces. Default methods can conflict; then you override. For a second implementation without a type relationship, use composition.
