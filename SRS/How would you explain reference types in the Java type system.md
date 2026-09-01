<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #DataAndState/ReferenceSemantics #Java/OOP #SRS

# How would you explain reference types in the Java type system?

> [!abstract] Short answer
> **A reference type’s values are pointers to objects — or `null`.** There are four kinds: class types, interface types, type variables, and array types. An object is a class instance or an array. The variable holds the reference; two variables can name the same object. Primitives are the other kind of type.

## Four kinds, one kind of value

The language has primitive types and reference types ([[How would you explain Java data types primitives and references]], [[What is the difference between primitive and reference types in Java]]). A reference value is a pointer to an object, or the null reference. You cannot declare a variable of the nameless **null type**; you assign `null` to any reference type ([[Why cannot a Java primitive variable be null]]).

| Kind | Example |
| --- | --- |
| Class type | `String`, `Point` |
| Interface type | `Runnable`, `List<String>` |
| Type variable | `T` in `class Box<T>` |
| Array type | `int[]`, `Point[]` |

A class or interface type may be parameterized (`List<String>`). `Object` is a superclass of every class; class and array types inherit `Object`’s members. `String` literals are references to `String` instances. Arrays **are** objects ([[Is a Java array a primitive or an object]]).

Creating an object (`new Point()`, `new int[10]`) yields a reference. Assigning that reference copies the pointer, not the object. Widening a reference (subtype to supertype) is compile-time only: the object is unchanged; the compiler regards the pointer as a more general type. Narrowing (`(Child) parent`) can throw `ClassCastException` ([[When can a ClassCastException be thrown in Java]]). `instanceof` tests before that downcast.

```d2
direction: down
rt: "reference type" {
  width: 180
  height: 45
  style.fill: "#fff3e0"
}
val: "reference value\npointer or null" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
obj: "object\nclass instance or array" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

rt -> val
val -> obj
```

**Fig. 1.** The type lives on the variable. The object lives on the other end of the reference.

```java
class Value { int val; }

public final class ReferenceTypes {
    public static void main(String[] args) {
        int i1 = 3;
        int i2 = i1;
        i2 = 4;                    // i1 is still 3

        Value v1 = new Value();
        v1.val = 5;
        Value v2 = v1;             // same object
        v2.val = 6;                // v1.val is 6

        Object o = v1;             // widening; same object
        int[] cells = new int[2];  // array type, array object
        Runnable r = null;

        System.out.println(i1);
        System.out.println(v1.val);
        System.out.println(o == v1);
        System.out.println(cells.length);
        System.out.println(r);
    }
}
```

**Listing 1.** Primitive assignment copies bits. Reference assignment copies a pointer. `Object o = v1` does not copy `Value`. `int[]` is a reference type.

> [!warning] A cast does not convert the object, and `(String) 5` is not a thing
> `(Child) parent` reinterprets the **reference**; if the object is not a `Child`, you get `ClassCastException`. Check with `instanceof` (or a pattern) first. Boxing `Integer` ↔ `int` is a conversion; it is not “forbidden” the way a dump that lists only string conversion claims. You do not write `(String) 5`; concatenation `+` can stringify a value. Primitive widening/narrowing is a different catalog ([[How would you explain widening and narrowing casts between Java primitive types]]).

> [!tip] Interview answer
> **Reference types are class, interface, type-variable, and array types; their values are pointers to objects or `null`.** An object is a class instance or an array. Assignment copies the pointer, so two variables can share one object. `null` is legal on references and illegal on primitives.
