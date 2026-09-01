<!--
reps: 0
priority: 0
-->
#Java/Language/Object/Clone #Java/OOP/Constructors #SRS

# Which cloning approach is preferred in Java?

> [!abstract] Short answer
> **The language does not name a preferred cloning style.** The **built-in** operation is **`Object.clone`**: `protected`, **`Cloneable`-gated**, **shallow**. A **copy constructor** (or a static factory that calls one) is just a constructor you write: **explicit fields**, **blank `final`s assignable**, **no marker interface**. **Arrays** already have public `T[] clone()`. Prefer the tool that matches the type: **array `clone` for arrays**; for your classes, a constructor/factory if you need a real copy without `Cloneable` ([[How would you explain the Object clone method and its issues]]).

## What the platform actually gives you

`Object.clone` is the specified copy: new instance of the **runtime** class, fields filled **as if by assignment**. Convention: `super.clone()` so `x.clone().getClass() == x.getClass()`. That **does** copy subclass fields when the chain uses `super.clone()`. The usual clone bugs are **shallow sharing** and **skipping `super.clone()`** (`return new Foo(this)` in `clone()` drops subclass state) — not “`clone` forgets subclass fields by design.”

`Cloneable` still **does not declare `clone`**. Callers need your public override. Independence of nested mutables is extra work ([[What is the difference between shallow and deep copying in Java]]).

A **copy constructor** is an ordinary constructor `Foo(Foo other)` that assigns fields (and may copy mutables). Blank **`final`** instance variables must be definitely assigned **in every constructor** — so you can set a `final` field to a **new** nested object there. After `super.clone()`, the clone **already exists**; a `clone()` method **cannot** assign those `final`s to a deep copy.

```java
final class Box {
    final int n;
    final int[] cells;

    Box(int n, int[] cells) {
        this.n = n;
        this.cells = cells.clone();
    }

    Box(Box other) {                 // copy constructor — deep for cells
        this(other.n, other.cells);
    }
}

final class CellBox implements Cloneable {
    int n;
    int[] cells;

    @Override
    public CellBox clone() {
        try {
            CellBox c = (CellBox) super.clone();
            c.cells = cells.clone(); // legal: cells is not final
            return c;
        } catch (CloneNotSupportedException e) {
            throw new AssertionError(e);
        }
    }
}
```

**Listing 1.** Conceptual: copy constructor initializes `final` fields. `clone()` can replace a **non-final** mutable field after `super.clone()`.

```d2
direction: right
clone: "Object.clone\nCloneable, shallow,\nprotected" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
ctor: "copy constructor\nexplicit fields,\nfinals OK" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
arr: "array.clone()\npublic T[]" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Three different tools. The spec does not rank the first two; arrays already expose `clone`.

## So what do you say in an interview?

Not “Java prefers copy constructors.” Say: **no ranking in the spec**; **`clone` is the API** and it is **awkward** (marker, `protected`, shallow). A copy constructor makes the copied fields **visible in source** and can fill **`final`s**. Subclasses still need their **own** copy constructor (`super(other)`), just as they need to keep the `super.clone()` chain. For **`int[]` / `T[]`**, `clone()` is the public, covariant, no-checked-exception copy ([[How does cloning work for objects arrays and two-dimensional arrays in Java]]).

> [!warning] “Preferred = copy constructor because clone misses subclass fields” is backwards
> With **`super.clone()`**, the native copy includes **all** fields of the **runtime** class. The inheritance trap is **`new C()` inside `clone()`**, which **changes the class**. Copy constructors have the twin trap: a subclass that does not add `Sub(Sub s)` drops **its** fields.

> [!tip] Interview answer
> **Java does not bless one cloning style.** `Object.clone` is the built-in shallow copy behind a marker interface. For application types, a copy constructor or factory is often simpler — explicit fields and `final`s — and for arrays you already have public `clone()`. Do not claim the JDK deprecated `clone` in favor of constructors; it did not.
