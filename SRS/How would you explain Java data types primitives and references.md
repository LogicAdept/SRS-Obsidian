<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #DataAndState/ValueSemantics #DataAndState/ReferenceSemantics #SRS

# How would you explain Java data types: primitives and references?

> [!abstract] Short answer
> **Two kinds of types, two kinds of values.** Primitive types (`boolean` and the numeric types) hold primitive values that do not share state. Reference types (classes, interfaces, type variables, arrays) hold **references** to objects — or `null`. An object is a class instance or an array. There is also a nameless **null type**.

## Two columns in the type system

Variables, arguments, and return values store either a **primitive value** or a **reference value** ([[What is the difference between primitive and reference types in Java]]).

**Primitives** are predefined and named by keywords: `byte`, `short`, `int`, `long`, `char`, `float`, `double`, `boolean` ([[Which primitives are there in Java]]). Widths are fixed (`byte` 8-bit signed, `int` 32-bit, `char` 16-bit unsigned, `float`/`double` IEEE 754). Primitive values do not share state: assigning `int b = a` copies bits. A primitive variable cannot be `null` ([[Why cannot a Java primitive variable be null]]). They are not subtypes of `Object` ([[Which Java language constructs are not subclasses of java.lang.Object]]).

**References** point at objects. Class types, interface types, type variables, and array types are the reference types. `new Point()` and `new int[10]` create objects; the variable stores the pointer, not the object’s guts. Two variables can refer to the same instance, so mutating through one is visible through the other. `null` is the reference to no object; you cannot declare a variable of the null type, but you can assign `null` to any reference type.

Wrappers (`Integer`, `Boolean`, …) exist so a primitive can be treated as an object (collections, generics, `null`) ([[Why are wrapper classes needed in Java]]). That is still a **reference** to a heap object that *contains* a primitive ([[Can primitive values reside on the Java heap]]).

Both kinds of value are passed **by value**: the primitive bits, or a copy of the reference ([[What does pass by value mean for Java parameters]]). `==` on primitives compares values; `==` on two references compares identity.

```d2
direction: down
types: "Java types" {
  width: 160
  height: 45
  style.fill: "#fff3e0"
}
prim: "primitive values\nboolean, numeric" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
ref: "reference values\n→ object or null" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
obj: "object =\nclass instance or array" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}

types -> prim
types -> ref
ref -> obj
```

**Fig. 1.** Primitive vs reference is about what the variable holds. Objects live behind references.

```java
public final class PrimitiveVsReference {
    static class Point {
        int x;
        Point(int x) { this.x = x; }
    }

    public static void main(String[] args) {
        int a = 1;
        int b = a;                 // copy of the bits
        b = 2;                     // a is still 1

        Point p = new Point(1);
        Point q = p;               // copy of the reference
        q.x = 2;                   // p.x is 2 — same object
        p = null;                  // q still refers to the Point

        int[] cells = new int[] { 1 }; // array is an object
        System.out.println(a);
        System.out.println(p);
        System.out.println(q.x);
        System.out.println(cells[0]);
    }
}
```

**Listing 1.** `int` assignment copies a value. `Point` assignment copies a reference. `int[]` is a reference type whose components are primitives.

> [!warning] “Object types vs primitives” misses arrays and `null`
> `int[]` is a reference type; its elements are still `int`. `String` is a class, not a primitive. `null` is not `0` and not a primitive. Saying “everything is an object” is false for the eight primitive types; saying “primitives never live on the heap” is false for fields and `int[]`.

> [!tip] Interview answer
> **Java has primitive types and reference types — and matching primitive vs reference values.** The eight primitives are values with no identity and no `null`. Classes, interfaces, and arrays are referenced objects; the variable holds a pointer (or `null`). Assignment and arguments copy that payload: bits for primitives, the pointer for objects.
