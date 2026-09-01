<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Language/NestedClasses #Java/Language/Modifiers/Static #SRS

# How would you explain static nested classes in Java?

> [!abstract] Short answer
> **A member class declared `static` is nested but not inner: it has no enclosing instance.** It is a namespaced helper of `Outer` — like a top-level class moved inside for packaging. Unqualified `n` or `Outer.this` is illegal; static members of `Outer` and `o.n` (even `private`) are fine. `new Outer.Nested()` does not need an `Outer` object.

## `static` on a member class means no enclosing instance

The `static` modifier on a **class** applies only to **member** classes. It marks the nested class as **not** an inner class: there is no immediately enclosing `Outer` bundled with each instance. Local and anonymous classes cannot be declared `static` (some are **implicitly** `static`: nested enum and record types, and a member class of an **interface**) ([[How would you explain categories of Java classes such as nested and anonymous]]).

That is the same idea as a `static` method: no current `Outer` in the body. Unqualified references to **instance** variables, instance methods, type parameters, or locals of lexically enclosing declarations do not compile. `Outer.this` does not compile either — the class that contains it is not an inner class of `Outer` ([[How do you from class get access to field outer class]]).

```d2
direction: down
st: "static class Nested" {
  width: 260
  height: 45
}
no: "no enclosing Outer instance" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
ok: "Outer.s / Nested members\nnew Outer.Nested()" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
inst: "instance of Outer only via\nan explicit o, including o.n" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
st -> no
no -> ok
no -> inst
```

**Fig. 1.** Static nested is about **linkage to an outer object**, not about `private`. `o.n` is language-legal; `n` and `Outer.this.n` are not.

As a member, `Nested` may be `public`, `protected`, package-private, or `private`. From **inside** `Outer`, `new Nested()` is enough. From any other type it is `new Outer.Nested()`. Contrast `outer.new Inner()` for a non-`static` member class ([[How would you explain nested classes in Java and when to use each kind]]).

```java
class Outer {
    private int n = 1;
    private static int s = 2;

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

class Other {
    Outer.Nested make() {
        return new Outer.Nested();
    }
}
```

**Listing 1.** `Nested` is constructed with no `Outer`. `s` is a class variable of the enclosing type. `o.n` is allowed because the access sits in `Outer`’s top-level body ([[Can object get access to member class declared how private if yes what way]]). `Other` cannot write `new Nested()`.

Use a static nested class when the helper should be **widely nameable** (`Outer.Nested`), should **not** capture method locals, and should **not** be glued to one `Outer` instance — builders, caches, `Map.Entry`-style companions, `private` implementation types. If the helper must read `this.n` without an extra argument, that is an **inner** member class.

> [!warning] “Cannot access outer members” is the unqualified-instance rule
> The JDK 8 tutorial’s “static nested classes do not have access to other members of the enclosing class” is too tight. They have no **enclosing instance**. `Outer.s` and `o.n` work; `n` and `Outer.this` do not.

> [!warning] `static` is not allowed on local or anonymous classes
> `static class Local` inside a method does not compile. Nested **enum** and **record** types are already implicitly `static` (not inner) whether or not you write `static`. A member class in an **interface** is likewise implicitly `static`.

> [!warning] `new Nested()` is not a top-level constructor
> Inside `Outer` the simple name works. Everywhere else the type is `Outer.Nested`. Serializing or sharing a static nested instance does not keep an `Outer` alive; an inner instance does.

> [!tip] Interview answer
> **A static nested class is a member class with no enclosing instance — a top-level class nested in `Outer` for packaging.** Construct it with `new Outer.Nested()`. It can use static members of `Outer` and instance fields through an `Outer` reference, including `private` ones. **It is not an inner class; `Outer.this` is illegal. Do not put `static` on a local or anonymous class.**
