<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Language/NestedClasses #Java/Language/Modifiers/Static #SRS

# What is the difference between static nested classes and inner classes?

> [!abstract] Short answer
> **Inner means nested and not `static`: each instance is tied to an enclosing `Outer` (`outer.new Inner()`, `Outer.this`).** A **static nested** class is a member class with **no** enclosing instance (`new Outer.Nested()`). Both may use `private` members of `Outer`; the static nested class needs an `Outer` **reference** for instance fields. `Outer.this` is illegal in the static nested class.

## Enclosing instance is the split

An **inner** class is a nested class that is not explicitly or implicitly `static`: a non-`static` member class, a local **normal** class, or an anonymous class. A **`static` nested** class is a **member** class declared `static`. Nested enum/record types and a member class of an **interface** are implicitly `static`, so they are **not** inner ([[How would you explain static nested classes in Java]], [[How would you explain categories of Java classes such as nested and anonymous]]).

`private` is not the difference. Access from any nested type sits in the enclosing top-level body, so `o.n` is legal even from `static class Nested`. The difference is whether there is an **immediately enclosing instance** and therefore unqualified `n` / `Outer.this` ([[How do you from class get access to field outer class]], [[Can object get access to member class declared how private if yes what way]]).

```d2
direction: down
inner: "Inner class" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
enc: "enclosing Outer\nouter.new Inner() / Outer.this" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
st: "static nested class" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
none: "no enclosing instance\nnew Outer.Nested()" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
inner -> enc
st -> none
```

**Fig. 1.** Inner stores an association with an `Outer`. Static nested does not; construct it like a namespaced top-level type.

| | Inner member | Static nested |
| --- | --- | --- |
| Construct | `outer.new Inner()` | `new Outer.Nested()` (or `new Nested()` inside `Outer`) |
| Enclosing instance | Yes | No |
| Unqualified instance field of `Outer` | Yes (not in a static context) | Compile-time error |
| `Outer.this` | Yes | Compile-time error |
| `o.n` / `Outer.s` | Yes | Yes |
| `private` of `Outer` | Yes | Yes (same top-level body) |

Use **inner** when the helper must see this `Outer`’s instance state. Use **static nested** when it should not be glued to one `Outer` (and should not keep that object alive) ([[How would you explain nested classes in Java and when to use each kind]]).

```java
class Outer {
    private int n = 1;
    private static int s = 2;

    class Inner {
        int own() {
            return n;
        }

        int enclosing() {
            return Outer.this.n;
        }
    }

    static class Nested {
        int classVar() {
            return s;
        }

        int instanceVar(Outer o) {
            return o.n;
        }

        // int bad = n;              // compile-time error
        // int also = Outer.this.n; // compile-time error
    }
}
```

**Listing 1.** `Inner` reads `n` through the enclosing instance. `Nested` reads `s` without an `Outer`, and `o.n` when one is passed.

Since **Java SE 16**, an inner class may declare static members and static initializers (not only constant variables). The dump’s “inner classes cannot contain static methods, initializers, or classes” is the **pre-16** rule. The inner class itself still is not `static`. A `static` nested class could always declare static members.

**Local classes** are a **shape of inner** (local **normal** class), not a third alternative to static nested. Declared in a block; simple name in scope for the **rest of that block, including the header**; no `public` / `private` / `static` on the class. They capture enclosing members and **effectively final** locals (the `final` keyword is not required since Java SE 8). In a `static` method they have no enclosing instance — still not a static nested class ([[How would you explain local classes in Java and their scoping rules]]).

> [!warning] Inner holds the outer object
> `outer.new Inner()` associates the inner instance with that `Outer`. A static nested instance does not. Do not use inner for a helper that should outlive or be shared without a particular outer.

> [!warning] Pre-16 “no static members in inner” is stale
> Java SE 16 allows static members and static initializers in inner classes, including local and anonymous. Local/anonymous still cannot be **declared** `static`. Nested enum/record are already implicitly `static`.

> [!warning] `Outer.this` is not a static-nested trick
> It names a lexically enclosing **instance**. In `static class Nested` it is a compile-time error. Disambiguate with `o.n` or `Outer.s`.

> [!tip] Interview answer
> **Inner class: nested, not static, has an enclosing instance — `outer.new Inner()` and `Outer.this`.** Static nested is a member class with no outer object — `new Outer.Nested()`. Both can use `private` of `Outer`; static nested just cannot say `n` without an `Outer` in hand. **Since 16, inner classes may have static members; they still are not static classes.**
