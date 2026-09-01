<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Paradigms/OOP #SRS

# Why is Java described as not purely object oriented?

> [!abstract] Short answer
> **Because it has primitive types, and those values are not objects.** `int`, `boolean`, and the other six primitives are not instances of a class, do not inherit from `Object`, and have no methods. Object-oriented Java is the **reference** side: class instances and arrays ([[What does it mean that Java is object oriented]]).

## Two type kinds, only one is objects

The language defines primitive types and reference types ([[What is the difference between primitive and reference types in Java]]). An object is a **class instance or an array**. A primitive value is neither. You cannot write `1.toString()` or store a bare `int` in an `ArrayList` without boxing.

`Object` is the root of the **class** hierarchy. Every class instance has `equals`, `hashCode`, and `toString`. A primitive does not sit in that hierarchy. Wrappers (`Integer`, `Boolean`, …) exist so a primitive can be carried as an object when an API needs one.

People still call Java object-oriented: code is organized in classes, objects encapsulate state, and subtype polymorphism works on references. “Not purely” is interview shorthand for **not every value is an object** — not a claim that Java lacks OOP ([[How would you explain Java primitive data types]]).

```d2
direction: down
val: "int 1" {
  width: 80
  height: 40
  style.fill: "#e8f5e9"
}
obj: "Integer instance" {
  width: 150
  height: 40
  style.fill: "#fff8e1"
}
root: "Object" {
  width: 90
  height: 40
}

val -> obj: "boxing"
obj -> root: "is-a"
```

**Fig. 1.** The primitive is not an `Object`. Boxing builds a separate instance that is.

```java
public final class NotPurelyOOP {
    public static void main(String[] args) {
        int n = 1;
        // n.toString();                      // does not compile
        Integer boxed = Integer.valueOf(n);
        System.out.println(boxed.toString());
        System.out.println(n + 1);            // operator, not a method call
    }
}
```

**Listing 1.** `n` has no members. `boxed` is an object and inherits `toString`. Arithmetic on `int` is a built-in operator.

> [!warning] Autoboxing hides the split; `int[]` does not
> `list.add(1)` boxes to `Integer` — the list still holds objects. Unboxing a `null` `Integer` throws `NullPointerException`. `int[]` *is* an object (an array); its **cells** are still primitives. `static` methods are a separate “not everything is an instance call” talking point; the primitives answer is the one this cue owns.

> [!tip] Interview answer
> **Java is object-oriented, but not purely, because primitives are not objects.** They are not `Object` subtypes and have no methods. When an API needs an object, you box. Arrays and wrappers are objects; `int` is not.
