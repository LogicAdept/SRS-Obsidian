<!--
reps: 0
priority: 0
-->
#Java/Language/Object/Clone #Java/Arrays #SRS

# How does cloning work for objects, arrays, and two-dimensional arrays in Java?

> [!abstract] Short answer
> **`Object.clone` is a shallow field-for-field copy** after a **`Cloneable` check**. **`Cloneable` declares no `clone` method.** **Every array is `Cloneable`** and exposes a **public** `clone` whose return type is **`T[]`**. That still copies **component slots as if by assignment**: a **1-D** clone has independent slots (primitive values are distinct; object references are shared). A **2-D** clone creates **only the outer array**; **rows stay shared**.

## `Cloneable` and `Object.clone`

`clone` lives on `java.lang.Object` as **`protected Object clone()`** throwing **`CloneNotSupportedException`**. `Cloneable` is a **marker**: it tells `Object.clone` that a field-for-field copy is legal. It **does not** declare `clone`, so a `Cloneable` reference does not give you a method to call ([[Why is clone declared on Object rather than on Cloneable]], [[How would you explain the Object clone method and its issues]]).

`Object` itself is **not** `Cloneable`. If the runtime class does not implement `Cloneable`, `Object.clone` throws **`CloneNotSupportedException`**. Otherwise it **creates a new instance of that same class** and fills each field with **exactly the contents** of the original field, **as if by assignment**. Nested objects are **not** cloned. That is a **shallow copy**, not a deep copy ([[What is the difference between shallow and deep copying in Java]]).

The documented intent is `x.clone() != x` and usually `x.clone().getClass() == x.getClass()`, and often `x.clone().equals(x)` — **none of those are absolute requirements**. Convention: override `clone` as **public**, obtain the instance with **`super.clone()`**, then replace references to mutable internals if the copy must be independent. A class with only primitives and immutable references can often return `super.clone()` unchanged.

```java
final class Point implements Cloneable {
    int x;
    int[] extras;

    Point(int x, int[] extras) {
        this.x = x;
        this.extras = extras;
    }

    @Override
    public Point clone() {
        try {
            return (Point) super.clone();
        } catch (CloneNotSupportedException e) {
            throw new AssertionError(e);
        }
    }
}
```

**Listing 1.** Covariant public `clone` that delegates to `Object.clone`. `x` is copied by value; `extras` is copied as a **reference**.

```java
Point a = new Point(1, new int[] { 9 });
Point b = a.clone();
boolean distinct = a != b && a.getClass() == b.getClass(); // true
boolean shared = a.extras == b.extras;                     // true — shallow
b.extras[0] = 0;                                           // a.extras[0] is 0 too
```

**Listing 2.** Conceptual: same-class distinct instance, shared mutable field. Uses Listing 1’s `Point`.

## Arrays: public `T[] clone()`

Arrays are objects ([[Is a Java array a primitive or an object]]). Every array type **implements `Cloneable` and `Serializable`**, and **overrides `clone` as public**. The return type of `clone` on `T[]` is **`T[]`**, and it **throws no checked exceptions** — so `int[] copy = original.clone();` needs no cast and no `try`.

A 1-D clone still follows the shallow rule: it allocates **one new array** and assigns each component. For `int[]`, the slots are independent variables (mutating `original[i]` does not change `copy[i]`). For `StringBuilder[]` (or any reference array), the **element objects are shared**.

## Two-dimensional arrays share rows

Java has no packed matrix type: `int[][]` is an **array whose components are `int[]` references** (or `null`). `ia.clone()` therefore copies **only the outer array**. **Subarrays are shared.** `ia != ja` is true; `ia[0] == ja[0]` is also true when that row is non-null. Writing `ja[0][i]` mutates `ia[0][i]`.

Independence takes a second pass: clone the outer array, then **clone each non-null row**.

```d2
direction: right
ia: "ia (int[][])\nouter array" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
ja: "ja = ia.clone()\nnew outer array" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
row: "one int[] row\nshared by both" {
  width: 200
  height: 80
  style.fill: "#ffebee"
}
ia -> row
ja -> row
```

**Fig. 1.** A 2-D `clone` allocates a new outer array and reuses the same row objects.

```java
int[] ia1 = { 1, 2 };
int[] ia2 = ia1.clone();
boolean distinct1d = ia1 != ia2; // true
ia1[1]++;
int copySlot = ia2[1];           // still 2 — independent primitive slots

int[][] ia = { { 1, 2 }, null };
int[][] ja = ia.clone();
boolean distinct2d = ia != ja;                 // true
boolean sharedRows = ia[0] == ja[0] && ia[1] == ja[1]; // true
ja[0][0] = 99;                                 // ia[0][0] is 99

int[][] deep = ia.clone();
for (int i = 0; i < deep.length; i++) {
    if (deep[i] != null) {
        deep[i] = deep[i].clone();
    }
}
deep[0][0] = 7;                                // ia[0][0] stays 99
```

**Listing 3.** Conceptual: 1-D primitive clone copies values; 2-D clone shares rows; a row-by-row clone decouples the inner arrays. Skip `null` rows.

> [!warning] `clone()` on `T[][]` is not a snapshot of the matrix
> The method name suggests a full copy. For a two-dimensional array it copies **one** array object. Nested `clone()` on each row is required if later writes to `copy[r][c]` must not change `original[r][c]`. The same leak exists for any **reference** array: `Date[] copy = dates.clone()` shares the `Date` instances.

> [!warning] `implements Cloneable` is not a public `clone()`
> Client code still cannot call `clone` unless the class **overrides** it with sufficient access (by convention, `public`). Reflective `clone` on a `Cloneable` instance is **not** guaranteed to succeed.

> [!tip] Interview answer
> **`Object.clone` shallow-copies fields after checking `Cloneable`; the marker interface has no `clone` method.** Arrays are always `Cloneable` and expose public `T[] clone()` with no checked exception, but that copy is still assignment of slots. **A 1-D primitive array gets independent values; a 2-D array clone shares the inner rows**, so you must clone each row if you need a real matrix copy.
