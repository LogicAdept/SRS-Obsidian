<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #Java/OOP/Polymorphism #SRS

# Can you use a weaker access modifier when overriding a method?

> [!abstract] Short answer
> **No.** An overriding (or hiding) method must provide **at least as much access** as the method it overrides. You may keep the same access or **widen** it (`protected` → `public`). You may not narrow it (`public` → `protected` / package / `private`). `private` methods are not overridden at all. Access levels: [[How do Java access modifiers work]]. Overriding: [[How would you explain method overriding in Java]].

## At least as much access

From most access to least: `public`, then `protected`, then package access (no modifier), then `private`. “Weaker” here means **more restrictive** (less visible).

| Overridden method | Legal override |
| --- | --- |
| `public` | `public` only |
| `protected` | `protected` or `public` |
| package access | package, `protected`, or `public` — **not** `private` |
| `private` | not overridden; a subclass method with the same signature is a new method |

The same table applies when a `static` method **hides** another class method. Hiding is not override: [[Can static methods be overridden in Java]]. Implementing a `public` interface method (implicitly `public` if you omit the modifier) also requires `public` on the class. Covariant returns are a different axis: [[Can you declare a narrower return type when overriding a method]].

```d2
direction: right
pub: "public" {
  width: 90
  height: 40
  style.fill: "#e8f5e9"
}
pro: "protected" {
  width: 110
  height: 40
  style.fill: "#e3f2fd"
}
pkg: "package" {
  width: 90
  height: 40
  style.fill: "#fff3e0"
}
pri: "private" {
  width: 90
  height: 40
  style.fill: "#ffcdd2"
}
pkg -> pro: "widen OK"
pro -> pub: "widen OK"
pub -> pro: "narrow illegal"
pro -> pkg: "narrow illegal"
pkg -> pri: "narrow illegal"
```

**Fig. 1.** Override may move toward `public`, never toward `private`.

```java
class Base {
    public void open() {}
    protected void share() {}
    void pack() {}
}

class Wider extends Base {
    @Override
    public void share() {}  // protected → public

    @Override
    protected void pack() {} // package → protected
}

class Same extends Base {
    @Override
    public void open() {}
}
```

**Listing 1.** Widening and keeping access are legal. `open()` must stay `public`.

```java
// Conceptual: does not compile
class Base {
    public void open() {}
    protected void share() {}
    void pack() {}
}

interface Named {
    String name(); // implicit public
}

class Narrower extends Base implements Named {
    @Override
    protected void open() {}   // public cannot become protected
    @Override
    void share() {}            // protected cannot become package
    @Override
    private void pack() {}     // package cannot become private
    @Override
    String name() {            // missing public — cannot implement Named
        return "x";
    }
}
```

**Listing 2.** Conceptual. Narrowing is a compile-time error, including a package-access `name()` that tries to implement a `public` interface method.

A subclass **may** declare `private void hidden()` when `Base` has `private void hidden()`. That is not an override: no `@Override`, no polymorphic dispatch, no substitutability rules. `private`: [[How would you explain private]]. Package access as the next wider level: [[When should you use package private visibility in Java]].

> [!warning] “Weaker” means narrower visibility, not a weaker `throws` clause
> Extra **checked** exceptions on an override are a separate compile-time error. Access and `throws` are two independent override checks. Do not mix them in one sentence.

> [!warning] Omitting the modifier is package access, not “default public”
> `@Override void open()` on a `public` superclass method does not compile. On an interface method it also fails: omitted access on a **class** is package-private; omitted access on an **interface** is `public`.

> [!warning] `@Override` will not save a private “override”
> If the superclass method is `private`, `@Override` on the subclass method is a compile-time error because nothing was overridden. You now have two unrelated methods.

> [!tip] Interview answer
> No. You cannot reduce access when overriding: public stays public, protected may become public, package access may become protected or public, and private is not overridden at all. You may only keep or widen visibility. The same rule applies to hiding static methods and to implementing interface methods, which are public.
