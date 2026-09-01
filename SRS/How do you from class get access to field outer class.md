<!--
reps: 0
priority: 0
-->
#Java/Language/NestedClasses #SRS

# How does a nested class access a field of its enclosing class?

> [!abstract] Short answer
> **An inner class uses the enclosing instance:** the simple name of the outer field, or `Outer.this.field` when that name is hidden. A **`static` nested class has no enclosing instance**, so it can use **static** members of `Outer` by name, and instance members only through an explicit `Outer` reference. `Outer.this` is a compile-time error there.

## Inner: enclosing instance; static: no such instance

A nested class whose declaration is **not** `static` (and not implicitly `static`) is an **inner** class. Unless that declaration sits in a **static context** (a `static` method, `static` field initializer, or static initializer), each inner instance is tied to an immediately enclosing `Outer`. Reading an instance field of `Outer` uses **that** enclosing object ([[How would you explain nested classes in Java and when to use each kind]]).

A `static` nested class is not an inner class. There is no `Outer` bundled with it, so an **unqualified** use of an instance field of `Outer` does not compile. Static fields of `Outer` are still in scope and may be named directly (`s` or `Outer.s`).

```d2
direction: down
inner: "Inner class\n(not in a static context)" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
enc: "enclosing Outer instance\nfield, or Outer.this.field" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
st: "static nested class" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
stat: "Outer static field\n(s / Outer.s)" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
inst: "instance field only via\nan Outer reference o.n" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
inner -> enc
st -> stat
st -> inst
```

**Fig. 1.** Inner access is through an enclosing instance. Static nested access is through the type (static members) or a value of type `Outer` (instance members).

The simple name `n` is the field **in scope at the use**: a field declared or inherited by the nested class **hides** the same name on `Outer`. `TypeName.this` denotes a lexically enclosing instance. `Outer.this.n` is therefore the outer field when `Inner` also has an `n`. It is a compile-time error if `Outer.this` appears in a **static context**, or if the class that immediately contains it is **not** an inner class of `Outer` (and is not `Outer` itself).

```java
class Outer {
    private int n = 1;
    static int s = 2;

    class Inner {
        int n = 10;

        int own() {
            return n;
        }

        int enclosingInstance() {
            return Outer.this.n;
        }

        int classVar() {
            return s;
        }
    }

    static class Nested {
        int classVar() {
            return s;
        }

        int instanceVar(Outer o) {
            return o.n;
        }

        // int bad = Outer.this.n; // compile-time error
    }

    static void inStaticMethod() {
        class Local {
            // int k = n; // compile-time error: no enclosing instance
            int k = s;
        }
    }
}
```

**Listing 1.** `Inner.own()` is `10`; `enclosingInstance()` is `1`. `Nested` may read `s` without an `Outer` value, and `o.n` when one is passed — including a `private` `n` ([[Can object get access to member class declared how private if yes what way]]). A local class declared in a `static` method is in a static context: `Outer` instance fields are not available ([[How would you explain local classes in Java and their scoping rules]]).

`Outer.n` as a **type-qualified** name is legal only when `n` is a **class** variable. `Outer.n` for an instance field is a compile-time error; that is why the static nested class writes `o.n`, not `Outer.n`.

Deep nesting uses the same qualified `this`: `Outer.this.n`, `Middle.this.n`. Each name is the corresponding enclosing instance.

> [!warning] “Static nested can see only static fields” is too tight
> Unqualified (and `Outer.field`) instance access is illegal. Passing an `Outer` and reading `o.n` is legal, and `private` does not block it. The dump’s “direct access only to static fields” is about **no enclosing instance**, not about `private`.

> [!warning] `Outer.this` is not a universal disambiguator
> It works in an inner class of `Outer`. In a `static` nested class, a `static` method, or a local/anonymous class in a static context, `Outer.this` does not compile. Shadowing there is `this.n` vs `o.n` / `Outer.s`.

> [!warning] A local class in a `static` method is not a “simple inner” with an outer object
> It may still be an inner class of no enclosing instance. Instance fields of `Outer` fail the same way as in `Nested`. Effectively final locals of that method are a different rule, and are available.

> [!tip] Interview answer
> **Inner classes read outer instance state through the enclosing instance — `field` or `Outer.this.field` if the nested class hides the name.** A static nested class has no enclosing instance: use static members of `Outer` directly, and instance fields only via an `Outer` reference. **`Outer.this` is illegal in a static nested class; a local class inside a static method has the same restriction.**
