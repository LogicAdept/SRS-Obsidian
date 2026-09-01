<!--
reps: 0
priority: 0
-->
#Java/Language/Object/Clone #SRS

# Why is `clone` declared on `Object` rather than on `Cloneable`?

> [!abstract] Short answer
> **`clone` is a `protected` method on `Object` that *implements* field-for-field copy.** **`Cloneable` is only a runtime permission bit** — the interface **declares no `clone`**. An interface method **cannot be `protected`** (or `native`); without a modifier it is **`public`**. Putting `clone` on `Cloneable` would have made a **public** cloning API on every implementor and could not host `Object`’s **protected** copy. A `Cloneable` reference still has **nothing to call**. The current `Object.clone` specification does **not** list the method as `native`.

## Two roles, one method

`Object.clone` does the work: if the **runtime class** is not `Cloneable`, throw **`CloneNotSupportedException`**; otherwise create a same-class instance and assign each field. `Object` itself is **not** `Cloneable`. Arrays are treated as `Cloneable` and expose public `T[] clone()` ([[How does cloning work for objects arrays and two-dimensional arrays in Java]], [[How would you explain the Object clone method and its issues]]).

**`protected`** does **not** mean “only after you override.” Clients outside `java.lang` and outside the subclass relationship cannot call it. A subclass **can** call `super.clone()` with **no** public override. Unrelated application code needs a **public** (or otherwise visible) override — the usual convention.

`Cloneable` has **no methods**. Implementing it does not add `clone` to the type. Reflective `clone` is **not** guaranteed to succeed.

```d2
direction: down
obj: "Object.clone()\nprotected · does the copy" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
gate: "Cloneable\nmarker · no clone() declared" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
pub: "your override\npublic clone() → super.clone()" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
obj -> gate
gate -> pub
```

**Fig. 1.** The operation lives on the root class. The interface is a check, not an API.

## Why the interface cannot hold it

Interface instance methods are **`public` or `private`**. Omit the modifier and the method is **implicitly `public`**. An interface method **must not** be declared **`protected`**, package-private, **`final`**, **`synchronized`**, or **`native`**.

Stand-alone interfaces also pick up **`Object`’s public instance methods** as implicit abstract members. **`clone` is not public**, so it is **not** in that implicit set.

```java
class Secret implements Cloneable {
    @Override
    protected Secret clone() {
        try {
            return (Secret) super.clone();
        } catch (CloneNotSupportedException e) {
            throw new AssertionError(e);
        }
    }
}

final class Box implements Cloneable {
    @Override
    public Box clone() {
        try {
            return (Box) super.clone();
        } catch (CloneNotSupportedException e) {
            throw new AssertionError(e);
        }
    }
}

class NotMarked {
    @Override
    public NotMarked clone() {
        try {
            return (NotMarked) super.clone(); // still throws
        } catch (CloneNotSupportedException e) {
            throw new IllegalStateException(e);
        }
    }
}

// Cloneable c = new Box();
// c.clone();           // does not compile
Box copy = new Box().clone();
```

**Listing 1.** Conceptual: `Secret` is `Cloneable` for `super.clone()` but not a caller API. `Box.clone` is public. A public override on a non-`Cloneable` class still throws from **`Object.clone`**.

> [!warning] `implements Cloneable` is not a public `clone()`
> Client code still cannot clone you until you override with enough access. A `Cloneable` parameter is not a cloning API. A public `clone()` that only calls `super.clone()` still throws if the class is not `Cloneable`.

> [!warning] `protected` ≠ “unoverridden objects cannot clone”
> Subclasses may call `super.clone()` without redeclaring `clone` as public.

> [!tip] Interview answer
> **`clone` sits on `Object` because that is where the protected field-copy lives and where every class can inherit it.** `Cloneable` cannot declare that method: interface methods are not `protected`. The marker only authorizes `Object.clone`; you still override `clone` as public if callers need it, and `super.clone()` still checks `Cloneable`.
