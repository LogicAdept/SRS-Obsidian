<!--
reps: 0
priority: 0
-->
#Java/Language/Object/Clone #SRS

# How would you explain the `Object.clone` method and its issues?

> [!abstract] Short answer
> **`Object.clone` is `protected`, throws `CloneNotSupportedException` if the runtime class is not `Cloneable`, and then does a shallow field-for-field copy** (assignment of each field, not a nested copy). **`Cloneable` declares no `clone` method**, so implementing the marker does not give callers an API. Independence of the copy is **convention**: you override, call `super.clone()`, and replace mutable internals yourself. Arrays are the special case with a **public `T[] clone()`** — still shallow for `T[][]`.

## What `clone` is specified to do

`clone` lives on `Object`, not on the interface ([[Why is clone declared on Object rather than on Cloneable]]). After the `Cloneable` check it **creates a new instance of the same class** and fills each field with **exactly the contents** of the original, **as if by assignment**. Nested objects are **not** cloned ([[What is the difference between shallow and deep copying in Java]]).

Documented intent: `x.clone() != x`, usually the same `getClass()`, often `equals` — **none of those are requirements**. Convention: obtain the instance with **`super.clone()`** so the runtime class is preserved down the hierarchy, then patch mutable structure.

`Object` itself is **not** `Cloneable`; cloning a plain `Object` throws. A class that implements `Cloneable` but does **not** override `clone` still has only the **protected** method — clients outside the package/hierarchy cannot call it.

```java
final class Box implements Cloneable {
    int n;
    int[] cells;

    Box(int n, int[] cells) {
        this.n = n;
        this.cells = cells;
    }

    @Override
    public Box clone() {
        try {
            return (Box) super.clone();
        } catch (CloneNotSupportedException e) {
            throw new AssertionError(e);
        }
    }
}
```

**Listing 1.** Public covariant override that still returns a **shallow** copy: `n` is copied, `cells` is the **same array**.

```java
Box a = new Box(1, new int[] { 9 });
Box b = a.clone();
boolean distinct = a != b;              // true
boolean shared = a.cells == b.cells;    // true — the usual bug
```

**Listing 2.** Conceptual: new outer object, aliased mutable field.

## The issues

**Marker with no method.** `Cloneable` only tells `Object.clone` that a field copy is legal. It **does not** declare `clone`, so you cannot call `clone` on a `Cloneable` typed reference. Reflective `clone` is **not** guaranteed to succeed.

**Protected, checked exception.** Callers need a public override. `CloneNotSupportedException` is checked, so every override that calls `super.clone()` pays a `try` even when the class implements `Cloneable` (the throw is then a logic error).

**Shallow by definition.** A “clone” that shares a mutable array, collection, or date is not independent. Deep copy is extra field writes on the object returned by `super.clone()`.

**Arrays look fine and still lie.** Every array is `Cloneable` and has public `T[] clone()` with no checked exception. A 1-D primitive array copies values; a **2-D** clone copies **only the outer array** — rows stay shared ([[How does cloning work for objects arrays and two-dimensional arrays in Java]]).

**Assignment, not a nested snapshot.** The copy initializes fields **as if by assignment**. That is the whole of `Object.clone`; any extra independence is your override.

```d2
direction: down
mark: "implements Cloneable\n(no clone() in the interface)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
copy: "Object.clone\nprotected, shallow fields" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
leak: "shared mutable internals\nunless you copy them" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
mark -> copy
copy -> leak
```

**Fig. 1.** The marker does not expose an operation; the operation does not give you a deep snapshot.

> [!warning] `implements Cloneable` is not a public `clone()`
> Client code still cannot clone you until you **override** with enough access. The interface is a permission bit for `Object.clone`, not a contract you can program to.

> [!warning] `clone() != original` does not mean independent
> Identity of the outer object is the easy check. If a field or array component is mutable, both sides still alias it. That is the default, not a JVM bug.

> [!tip] Interview answer
> **`Object.clone` is a protected shallow copy that throws unless the class is `Cloneable`; the marker interface has no `clone` method, which is the design smell.** You override, call `super.clone()`, and copy mutable fields if you need independence. Arrays have a public `clone` that is still shallow — especially `T[][]`. Do not treat `clone` as a general copying API.
