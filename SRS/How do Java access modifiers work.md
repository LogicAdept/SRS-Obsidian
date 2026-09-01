<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #Java/OOP/Encapsulation #SRS

# How do Java access modifiers work?

> [!abstract] Short answer
> Four levels, checked at **compile time**. **`private`**: the enclosing **top-level** class or interface body (nested types in that nest included). **Package access** (no `public` / `protected` / `private` on a class member): the declaring package only. **`protected`**: that package, plus subclasses — and for **instance** members outside the package, only through a receiver whose type is the accessing subclass (or a further subclass). **`public`**: permitted wherever the **enclosing type** is accessible (and, across modules, the package is exported). There is no `package-private` keyword. `protected` trap: [[How does protected]]. Package as encapsulation: [[How does package private visibility relate to encapsulation]]. When to use package access: [[When should you use package private visibility in Java]]. Interface omitted access is `public`: [[How would you explain default modifiers for fields and methods inside interfaces]].

## The member is reachable only if the type is too

A member or constructor is accessible only if (i) its class, interface, or type is accessible, and (ii) the member itself allows the access. `public` on a field of a package-access class does not leak that field outside the package.

| Modifier written | Same top-level type | Same package | Subclass in another package | Everywhere else |
| --- | --- | --- | --- | --- |
| `public` | yes | yes | yes | yes, if the type is reachable |
| `protected` | yes | yes | yes, with the instance qualifier rule | no |
| *(none)* | yes | yes | **no** | no |
| `private` | yes (whole top-level nest) | no | no | no |

**Same-package subclasses already have package access; the “subclass” column is the other-package case.**

Top-level classes and interfaces are **`public` or package access**. `protected` and `private` apply to **members** (including member types), not to a top-level type. A class member or constructor with no access modifier has package access. Interface members with no access modifier are **implicitly `public`** — not package access. Interface methods may be declared `public` or `private`; they may not be `protected` or package-access.

`private` is the body of the **top-level** type that encloses the declaration, so nested types in that same top-level type may read each other’s private members. Subclasses do **not** inherit `private` members. A `private` method is not overridden: a subclass may reuse the signature with no “at least as much access” rule. An overriding or hiding method otherwise **must not narrow** access (`public` stays `public`; `protected` stays `protected` or `public`; package access must not become `private`): [[Can you use a weaker access modifier when overriding a method]].

```java
package demo;

public class Box {
    public int pub;
    protected int prot;
    int pack;        // package access
    private int priv;

    public int readPriv() { return priv; }

    static class Nested {
        int steal(Box b) { return b.priv; } // same top-level class
    }
}

class SamePackage {
    int peek(Box b) {
        return b.pub + b.prot + b.pack; // b.priv is not accessible here
    }
}
```

**Listing 1.** Same package sees `public`, `protected`, and package access. `private` is the top-level `Box` body, including `Nested`, not `SamePackage`.

```java
package other;
// Conceptual — separate package from points.Point with protected int x

public class Point3d extends points.Point {
    public void delta(points.Point p) {
        // p.x += 1;           // compile-time error: receiver type is Point, not Point3d
    }
    public void delta3d(Point3d q) {
        q.x += 1;              // OK: qualifying type is Point3d (this subclass)
    }
}
```

**Listing 2.** Conceptual. Outside the declaring package, `protected` instance access is allowed only when the qualifying type is the accessing subclass (or a subclass of it). A `Point` parameter is not enough even inside `Point3d`.

```d2
direction: down
priv: "private\nenclosing top-level body" {
  width: 240
  height: 44
  style.fill: "#ffcdd2"
}
pkg: "package access\nsame package" {
  width: 240
  height: 44
  style.fill: "#fff8e1"
}
prot: "protected\npackage + subclass rules" {
  width: 260
  height: 44
  style.fill: "#e3f2fd"
}
pub: "public\n(+ module export for types)" {
  width: 260
  height: 44
  style.fill: "#e8f5e9"
}
priv -> pkg -> prot -> pub
```

**Fig. 1.** Each level adds callers. `protected` is not “package plus any `Super` reference in a subclass.”

> [!warning] `default` is not an access modifier
> Package access is the **absence** of `public`, `protected`, and `private`. The keyword `default` marks an interface instance method with a body. On an interface, omitting the modifier means `public`.

> [!warning] `private` is not “this class file only,” and `public` is not “the whole JVM”
> Nested types of the same top-level class share `private` members. A `public` member of a package-access class is still trapped in the package. A `public` type in a non-exported module package is not world-visible.

> [!warning] `protected new` and sibling instances
> A `protected` constructor may be used as `super(...)` from a subclass in another package, but a plain `new Super(...)` (non-anonymous) from that subclass is illegal. A subclass also cannot touch `protected` instance fields of a **sibling** instance typed as the superclass.

> [!tip] Interview answer
> Java has four compile-time access levels: private to the enclosing top-level type, package access with no modifier, protected for the package plus subclasses, and public. Protected instance members outside the package are only usable through a receiver of your subclass type, not through a Super-typed variable. Interface members without a modifier are public, not package-private.
