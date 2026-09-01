<!--
reps: 0
priority: 0
-->
#Java/Language/Object/Clone #Java/Arrays #SRS

# What is the difference between shallow and deep copying in Java?

> [!abstract] Short answer
> A **shallow copy** is a **new instance** whose fields are filled **as if by assignment**: primitives and references are duplicated, but **nested objects are not**. A **deep copy** also copies the **mutable inner structure**, so later writes through the copy do not change the original. **`Object.clone` implements shallow copy.** Deep copy is extra work after `super.clone()` (or an equivalent copy), not a second JVM instruction.

## Two meanings of “copy”

`Object.clone` states the distinction directly. After the `Cloneable` check, it **creates a new instance of the same class** and initializes each field with **exactly the contents** of the corresponding field of the original, **as if by assignment**. “The contents of the fields are not themselves cloned.” That is a **shallow copy**, not a **deep copy** ([[How would you explain the Object clone method and its issues]]).

Independence is a **convention**: after `super.clone()`, **replace** references to mutable internals with copies. Primitives were already copied; you do not copy them “again.” Nested objects need **some** copy path — their own `clone()`, `array.clone()`, a copy constructor, or a field-by-field `new` — not “every type must be `Cloneable`.” `super.clone()` runs **once** on the outer object.

Assignment of a variable (`b = a`) is **not** even a shallow copy of the object: both names refer to **one** instance. Shallow copy allocates a **second** instance and then uses assignment **per field**.

```d2
direction: down
orig: "original\nn=1, cells → [9]" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
shallow: "shallow copy\nn=1, cells → same [9]" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
deep: "deep copy\nn=1, cells → new [9]" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
shared: "one int[] {9}" {
  width: 180
  height: 55
  style.fill: "#ffebee"
}
fresh: "another int[] {9}" {
  width: 180
  height: 55
  style.fill: "#e8f5e9"
}
orig -> shared
shallow -> shared
deep -> fresh
```

**Fig. 1.** Shallow copy shares the nested array. Deep copy allocates a second array with the same component values.

```java
final class Box implements Cloneable {
    int n;
    int[] cells;

    Box(int n, int[] cells) {
        this.n = n;
        this.cells = cells;
    }

    public Box shallowCopy() {
        try {
            return (Box) super.clone();
        } catch (CloneNotSupportedException e) {
            throw new AssertionError(e);
        }
    }

    public Box deepCopy() {
        Box copy = shallowCopy();
        copy.cells = cells.clone();
        return copy;
    }
}
```

**Listing 1.** `shallowCopy` is `Object.clone` (field assignment). `deepCopy` then clones the mutable `int[]`. `n` is a primitive, so it needs no extra step.

```java
Box a = new Box(1, new int[] { 9 });
Box s = a.shallowCopy();
Box d = a.deepCopy();

boolean twoObjects = a != s && a != d;     // true
boolean shallowShares = a.cells == s.cells; // true
boolean deepIndependent = a.cells != d.cells; // true

s.cells[0] = 0;  // a.cells[0] is 0
d.cells[0] = 7;  // a.cells[0] stays 0
```

**Listing 2.** Conceptual: identity of the `Box` vs identity of `cells`.

## Arrays make the same split visible

Every array is `Cloneable` and has a public `T[] clone()`. That method is still **shallow** ([[How does cloning work for objects arrays and two-dimensional arrays in Java]]).

For `int[]`, components **are** primitives. A shallow clone already copies the values into a new array, so mutating `copy[i]` does not change `original[i]`. For `StringBuilder[]`, components are **references**; the builders stay shared.

A multidimensional array is an array of arrays. Its `clone` “creates only a **single** new array. Subarrays are shared.” `ia != ja` and `ia[0] == ja[0]` can both be true. A deep copy of `int[][]` clones the outer array **and** each non-null row.

```java
int[][] ia = { { 1, 2 }, null };
int[][] shallow = ia.clone();
boolean sharedRow = ia[0] == shallow[0]; // true

int[][] deep = ia.clone();
for (int i = 0; i < deep.length; i++) {
    if (deep[i] != null) {
        deep[i] = deep[i].clone();
    }
}
boolean copiedRow = ia[0] != deep[0];    // true
```

**Listing 3.** Conceptual: one `clone()` on `int[][]` is shallow; cloning each row is the deep version for this structure.

> [!warning] `clone()` is shallow even when the result “looks copied”
> `x.clone() != x` only proves you have a **new outer object**. If a field or array component holds a mutable object, both sides still alias it. `int[][]` and `StringBuilder[]` are the usual interview traps. Sharing **immutable** nested objects (`String`) is fine; sharing a mutable array or collection is not.

> [!warning] “Deep” is not `super.clone()` on every field
> Calling `super.clone()` **once** creates the outer shell. Nested `clone()` / `new` is **per mutable field**. A type that is not `Cloneable` can still be deep-copied by hand.

> [!tip] Interview answer
> **Shallow copy duplicates the object and assigns each field; nested objects stay shared. Deep copy also copies the mutable inner structure so the two graphs can diverge.** `Object.clone` and array `clone()` are shallow. Primitives need nothing extra; a 2-D array or a field that holds an `int[]` needs another clone (or equivalent) per mutable level.
