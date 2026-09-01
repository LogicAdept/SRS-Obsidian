<!--
reps: 0
priority: 0
-->
#Java/Language/Object #DataAndState/Objects #SRS

# How would you explain objects?

> [!abstract] Short answer
> In Java an **object** is a **class instance or an array** — not a primitive, not `null`. You reach it through a **reference** (a pointer to that instance, or the null reference). **Assignment copies the reference**, so two variables can share **one** object and see each other’s writes. **State** lives in instance fields or array components; **behavior** is method invocation on that reference. Every object supports `Object`’s methods ([[How would you explain java.lang.Object as the root of the class hierarchy]]).

## Class instance or array

The types that exist at all are **primitive types** and **reference types** (class, interface, type variable, array). Only **objects** sit behind references: a `new Point(…)`, a `new int[3]`, a string created by `+`. An `int` is a value in the variable itself; there is no `int` object unless you box ([[Is a Java array a primitive or an object]], [[Which Java language constructs are not subclasses of java.lang.Object]]).

A class instance is created by a class-instance creation expression (`new`). An array is created by an array creation expression or an array initializer. Other expressions may create objects **implicitly** (for example string concatenation). The **null** reference refers to **no** object.

On a reference you can: access fields, invoke methods, cast, concatenate with `String` (via `toString`), use `instanceof`, compare with `==` / `!=`, and use `?:`. `==` on references is **identity**: same object or not, not “same fields.”

```d2
direction: right
v1: "v1" {
  width: 80
  height: 50
  style.fill: "#e3f2fd"
}
v2: "v2 = v1" {
  width: 100
  height: 50
  style.fill: "#e3f2fd"
}
obj: "one Value object\nval == 6" {
  width: 180
  height: 70
  style.fill: "#ffebee"
}
v1 -> obj
v2 -> obj
```

**Fig. 1.** After `v2 = v1`, both names point at the **same** instance. That is not a copy of the object.

```java
class Value {
    int val;
}

class ObjectIdentity {
    public static void main(String[] args) {
        int i1 = 3;
        int i2 = i1;
        i2 = 4;                    // i1 stays 3 — two primitive variables

        Value v1 = new Value();
        v1.val = 5;
        Value v2 = v1;             // copies the reference, not the object
        v2.val = 6;                // v1.val is 6
        System.out.println(v1 == v2); // true
    }
}
```

**Listing 1.** Conceptual: primitive assignment copies a value. Reference assignment aliases one object.

## State, identity, `Object`

Most objects have **state**: fields of a class instance, or components of an array. Many references may point at that same state; mutation through one is visible through the others. Each object also has a **monitor** used by `synchronized` and by `wait` / `notify`.

The runtime class of an object is a subclass of `Object` (arrays included). You therefore always have `equals`, `hashCode`, `toString`, `getClass`, and the rest unless a subclass overrides them ([[How would you explain key methods declared on java.lang.Object]]). Default `equals` is the same identity test as `==`.

Creating a **second** object with similar state is a separate operation (`new`, a copy constructor you write, `clone`, and so on). It is not what `=` does ([[What is the difference between shallow and deep copying in Java]], [[How would you explain the Object clone method and its issues]]).

> [!warning] `=` does not clone
> `Box b = a;` gives you two variables and **one** heap object. Later `b.mutate()` is `a.mutate()`. Interview answers that start with `clone()` are answering a different question; the object model starts with **reference semantics**.

> [!warning] “Everything is an object” is false
> `int`, `boolean`, and the other primitives are **not** objects. `null` is not an object. An **interface** is a type of reference, not an instance; the instance you store there is still a class instance or an array.

> [!tip] Interview answer
> **An object is a class instance or an array, reached by a reference.** Assignment copies that reference, so two names can share one bundle of fields. Primitives are not objects; `null` refers to none. All objects inherit `Object`’s methods, and `==` on references means identity.
