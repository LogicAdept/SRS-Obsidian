<!--
reps: 0
priority: 0
-->
#Java/Language/Object #Java/OOP/Inheritance #SRS

# Do Java classes inherit from Object explicitly or implicitly?

> [!abstract] Short answer
> **Implicitly**, for a normal class that omits `extends`: its **direct** superclass is `java.lang.Object`. You **may** write `extends Object` explicitly; it is the same direct superclass. If you `extends SomeClass`, `Object` is still a **superclass** (the root), but not the direct one. `Object` itself has **no** superclass; it must not have an `extends` clause. Root type: [[How would you explain java.lang.Object as the root of the class hierarchy]]. Inheritance: [[What is inheritance]]. Not every type is a class: [[Which Java language constructs are not subclasses of java.lang.Object]].

## Direct superclass vs the root

Each class except `Object` is a subclass of exactly one existing class. A normal class declaration’s optional `extends` names that **direct** superclass. If the clause is missing, the direct superclass type is `Object`.

`extends` is forbidden on `Object` (primordial class, no direct superclass). `Enum` and `Record` cannot be named in a normal class’s `extends` clause; only enum classes and record classes get those as their implicit direct superclasses.

The superclass relation is transitive. `class ColoredPoint extends Point {}` has direct superclass `Point`. `Object` is still a superclass of `ColoredPoint`. Single class inheritance: [[Why does Java disallow multiple class inheritance]]. `extends` syntax: [[Which Java syntax elements express inheritance]].

```d2
direction: down
obj: "Object\nno extends, no superclass" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
point: "class Point {}\nimplicit extends Object" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
named: "class Named extends Object" {
  width: 260
  height: 45
  style.fill: "#fff3e0"
}
col: "class ColoredPoint extends Point" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}
obj -> point
obj -> named
point -> col
```

**Fig. 1.** Omit `extends` and the compiler inserts `Object`. Name another class and `Object` stays in the chain, one level up.

```java
class Point {}                 // direct superclass Object
class Named extends Object {}  // same direct superclass, written out
class ColoredPoint extends Point {}

class Demo {
    static boolean pointIsObjectChild() {
        return Point.class.getSuperclass() == Object.class;
    }

    static boolean coloredIsPointChild() {
        return ColoredPoint.class.getSuperclass() == Point.class;
    }
}
```

**Listing 1.** `Point` and `Named` both have direct superclass `Object`. `ColoredPoint`’s direct superclass is `Point`; `Object` is still a superclass.

```java
enum Color { RED }     // direct superclass Enum<Color>, then Object
record Point(int x, int y) {} // direct superclass Record, then Object
```

**Listing 2.** Enum and record declarations do not use `extends Object`. Their implicit direct superclasses are `Enum<E>` and `Record`. Enum `extends`: [[Can a Java enum extend a class]].

An anonymous class that implements an interface has direct superclass `Object`. An anonymous class that extends a class has that class as its direct superclass.

Interfaces are not classes. They do not have `Object` as a superclass. An interface with no `extends` still **implicitly declares** `Object`’s `public` instance methods as `abstract` members, which is why you can call `equals` on an interface-typed reference. Methods inherited from `Object`: [[How would you explain the most important methods declared on java.lang.Object]] and [[Where do default equals and hashCode implementations come from in Java]].

Arrays are objects, not class declarations. Every array type’s `Class` object acts as if its direct superclass is `Object`, and array types inherit `Object`’s members (`clone` is special-cased). Arrays as objects: [[Is a Java array a primitive or an object]].

> [!warning] “Everything extends Object” skips `Object` itself and non-class types
> `Object` has no superclass. Primitives are not objects. Interfaces do not extend `Object` as a class. You cannot write `class Foo extends Object, Bar` — one class superclass only.

> [!warning] `enum Color extends Object` does not compile
> An enum’s direct superclass is already `Enum<Color>`. A record’s is `Record`. You do not add `extends Object` to those declarations. `Object` is still in the superclass chain.

> [!warning] `extends Object` is redundant, not illegal
> `class Foo extends Object {}` is an explicit direct superclass of `Object`. It does not change the hierarchy compared with `class Foo {}`. Prefer omitting it.

> [!tip] Interview answer
> Implicitly: a normal class with no extends has Object as its direct superclass, though writing extends Object is legal and equivalent. If you extend another class, Object is still the root, not the direct parent. Object itself has no superclass; enums and records go through Enum and Record, and interfaces do not extend Object as a class.
