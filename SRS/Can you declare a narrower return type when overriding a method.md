<!--
reps: 0
priority: 0
-->
#Java/Versions/5 #Java/OOP/Polymorphism #SRS

# Can you declare a narrower return type when overriding a method?

> [!abstract] Short answer
> **Yes, for reference types** (since Java 5). The overriding method’s return type must be **return-type-substitutable** for the overridden one: a **subtype** of that reference type (covariant return), or `void`/`void`, or the **same primitive**. A wider type, a different primitive, or a primitive vs a reference is a compile-time error. The **signature** (name and parameters) must still match; a different return type alone is not overloading. Overriding: [[How would you explain method overriding in Java]]. Overload vs override: [[How would you explain Overload vs Override]].

## Covariant returns; primitives stay identical

An overriding (or hiding) method `d1` with return type R1 must be return-type-substitutable for the overridden method’s R2:

- If R1 is `void`, R2 is `void`.
- If R1 is a primitive, R2 is **identical** to R1 (`int` does not refine to `long` or `Integer`).
- If R1 is a reference type, R1 (adapted to `d2`’s type parameters) is a **subtype** of R2. Unchecked conversion to a subtype of R2 is also allowed and produces an unchecked warning.

That is covariant return: specialize `Animal` to `Dog`, `Object` to `String`, `C` to `D`. Access still cannot get narrower, and the overriding method cannot throw extra checked exceptions. Runtime dispatch still uses the object’s class; the **compile-time type** of the call is the return type of the compile-time declaration. Binding: [[What is the difference between static and dynamic binding in Java]].

```d2
direction: down
sup: "Animal resident()\nin Kennel" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
ok: "Dog resident()\nsubtype — legal" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
bad: "Number / int / void\nnot substitutable" {
  width: 240
  height: 50
  style.fill: "#ffcdd2"
}
sup -> ok
sup -> bad
```

**Fig. 1.** Narrower means a subtype of the **reference** return type. Primitives and `void` cannot be “narrowed.”

```java
class Animal {}
class Dog extends Animal {}

class Kennel {
    Animal resident() {
        return new Animal();
    }
}

class DogKennel extends Kennel {
    @Override
    Dog resident() {
        return new Dog();
    }
}

class Demo {
    static Animal asAnimal(Kennel k) {
        return k.resident();
    }

    static Dog asDog(DogKennel d) {
        return d.resident();
    }
}
```

**Listing 1.** `DogKennel.resident()` overrides `Kennel.resident()` with a narrower reference type. `Kennel k = new DogKennel(); k.resident()` still has compile-time type `Animal`.

```java
// Conceptual: does not compile
class Kennel {
    Animal resident() { return new Animal(); }
    int count() { return 1; }
    void close() {}
}

class Bad extends Kennel {
    Number resident() { return 0; }   // not a subtype of Animal
    long count() { return 1L; }       // primitive must be identical
    Animal close() { return null; }   // void stays void
    Dog resident(String name) {       // different parameters — overload, not override
        return new Dog();
    }
}
```

**Listing 2.** Conceptual. Changing only a primitive or `void` is illegal. A different parameter list overloads and does not override `resident()`.

The same substitutability rule applies when a `static` method **hides** another class method. Hiding is not override: [[Can static methods be overridden in Java]]. Private methods are not overridden at all, so a subclass “same signature” method may use any return type. Polymorphism: [[Which OOP principle does method overriding illustrate]].

> [!warning] The caller’s static type still sees the superclass return type
> `Kennel k = new DogKennel(); Dog d = k.resident();` does not compile. The invocation type is `Animal`. You need a `DogKennel` (or a cast) to see `Dog` without an extra cast from `Animal`.

> [!warning] “Narrower” is not a smaller primitive
> `short` does not override `int`. Boxing does not either: `Integer n()` does not override `int n()`. Both sides must be the same primitive, or both references with a subtype relation.

> [!warning] A raw/generic mismatch is an unchecked warning, not a free pass
> Return-type-substitutability allows an unchecked conversion so legacy raw returns can meet generic ones. That is unsound: you get a compile-time unchecked warning, not a new covariant subtype relationship you can ignore.

> [!tip] Interview answer
> Yes, since Java 5 an overriding method may return a subtype of the original reference type — covariant return. The name and parameters must still match, primitives must stay the same type, and void stays void. The call’s compile-time type is still the superclass return type; at run time the subclass method runs and returns the more specific object.
