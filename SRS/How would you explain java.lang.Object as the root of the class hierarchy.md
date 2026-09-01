<!--
reps: 0
priority: 0
-->
#Java/Language/Object #Java/OOP/Inheritance #SRS

# How would you explain `java.lang.Object` as the root of the class hierarchy?

> [!abstract] Short answer
> **The class hierarchy is a tree with `Object` at the top.** Every class except `Object` has **exactly one** direct superclass; `Object` has **none**, and **`extends` on `Object` is a compile-time error**. “Superclass” is the **transitive** closure of that link. **`Object` is also a supertype of array types and of a stand-alone interface type**, even though those are not `class X extends Object`. A variable of type `Object` can hold **any object** (class instance or array) or `null`. **Primitives are not classes.**

## Class hierarchy: one parent, then `Object`

`Object` is documented as **the root of the class hierarchy**: every class has `Object` as a superclass. A normal class’s `extends` names its **direct** superclass; if `extends` is omitted, the direct superclass is `Object`. Each class except `Object` is an extension of a **single** existing class.

The **superclass** relation is the transitive closure of **direct** superclass. `ColoredPoint extends Point` does not skip `Object`. A constructor that is not `Object`’s and that does not start with `this(...)` / `super(...)` implicitly begins with **`super();`**. `Object` is the stop.

`enum` and `record` do **not** have `Object` as a *direct* superclass: an enum’s direct superclass type is `Enum<E>`, a record’s is `Record`. Both still sit under `Object`.

```d2
direction: down
obj: "Object\n(no extends)" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
point: "Point\n(implicit extends Object)" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
cp: "ColoredPoint\nextends Point" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
named: "interface Named\nsupertype Object\n(not a subclass)" {
  width: 220
  height: 80
  style.fill: "#f3e5f5"
}
arr: "int[] / String[]" {
  width: 180
  height: 55
  style.fill: "#e8f5e9"
}
en: "enum Kind\nextends Enum<Kind>" {
  width: 200
  height: 55
  style.fill: "#f3e5f5"
}
obj -> point
point -> cp
obj -> named
obj -> arr
obj -> en
```

**Fig. 1.** Class subclassing is a single chain under `Object`. Interfaces and arrays have `Object` as a **supertype**; enums reach it through `Enum`.

```java
class Point { int x, y; }
class ColoredPoint extends Point { int color; }

interface Named { String name(); }

class Person implements Named {
    public String name() { return "Ada"; }
}

enum Kind { A, B }            // direct superclass: Enum<Kind>
record Pair(int a, int b) {}  // direct superclass: Record
```

**Listing 1.** Implicit `Object`, explicit `extends`, interface, enum, and record.

```java
Object o1 = new ColoredPoint();
Object o2 = new Person();
Named n = new Person();
Object o3 = n;                  // interface type widened to Object
Object o4 = new int[] { 1, 2 };
Object o5 = null;               // allowed; not an instance
boolean allObjects = new Point() instanceof Object
        && o4 instanceof Object
        && Kind.A instanceof Object; // true (non-null)
```

**Listing 2.** Conceptual: `Object` is the universal reference type for objects. Widening follows **supertype**, not only `extends`.

## Supertype is wider than superclass

**Superclass** is a relation on **classes** (arrays: direct superclass is `Object`). **Supertype** is the type-system closure used for assignment.

For a non-generic interface with **no** direct superinterfaces, **`Object` is a direct supertype** of that interface type. `Named` is not a **subclass** of `Object`. For arrays: `Object` is a direct supertype of `Object[]` and of a primitive array `P[]`. `Object[]` is **not** a supertype of `int[]` — a primitive array is an `Object`, not an `Object[]` ([[Is a Java array a primitive or an object]]).

All class and array types inherit `Object`’s methods ([[How would you explain key methods declared on java.lang.Object]], [[How would you explain the most important methods declared on java.lang.Object]]). A type parameter with no bound is assumed to be `Object`, so a bare `<T>` still allows `t.toString()`.

> [!warning] Superclass ≠ supertype
> Saying “every type extends `Object`” mixes three relations. **Primitives** are outside the class hierarchy. An **interface** is not a subclass of `Object`, yet `Object` is still a **supertype** of a stand-alone interface. **`ColoredPoint extends Point`**, an **enum**, and a **record** do **not** have `Object` as their *direct* superclass ([[Which Java language constructs are not subclasses of java.lang.Object]]).

> [!tip] Interview answer
> **`Object` is the root of the class hierarchy: one direct superclass per class, none for `Object`, and every class is a subclass of `Object` by transitivity.** That is why you can store any object — including an array — in an `Object` variable. Do not say every *type* extends `Object`: primitives do not, and an interface is a supertype relationship, not `class I extends Object`.
