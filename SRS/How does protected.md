<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #Java/OOP #SRS

# How does protected?

> [!abstract] Short answer
> **`protected`** is package access **plus** a subclass right. Same-package code may use the member whether it is a subclass or not. Outside that package, only a **subclass body** may use it — and for a **`protected` instance** field or method the receiver’s compile-time type must be **that subclass** (or a further subclass), not the declaring superclass. It is not “any `Super` reference once you extend.” Levels: [[How do Java access modifiers work]]. Versus package access: [[How does package private visibility relate to encapsulation]]. Override widening: [[Can you use a weaker access modifier when overriding a method]].

## Package, then “this family of objects”

A member or constructor declared `protected` is accessible (i) from the package that contains its declaring class, and (ii) as specified for subclasses. Top-level types cannot be `protected`; interface methods cannot be `protected`. Accessibility is compile-time.

Outside the declaring package, a `protected` member of an object may be used only by code **responsible for implementing that object**. For an instance field or instance method, that means: you are inside a subclass `S`, and the qualifying type of the access (`p.x`, `p.m()`, `TypeName.x`) is `S` or a subclass of `S`. A parameter typed as the **superclass** is not enough, even inside `S`. A further subclass of `S` is a legal qualifier.

`static protected` members skip that extra receiver rule: they are still limited to the package and to subclass bodies, but you may name them as `Super.NAME` from `S`. A `protected` constructor may be used as `super(...)` (or a qualified `E.super(...)`) from a subclass in another package; a plain `new Super(...)` that does not declare an anonymous class is **not** permitted from outside the declaring package.

An overriding method must not narrow `protected` (it stays `protected` or becomes `public`).

```java
package geom;

public class Point {
    protected int x;
    protected static int count;

    protected Point() {}
}

class Neighbor {
    int peek(Point p) {
        return p.x + Point.count; // same package: subclass not required
    }
}
```

**Listing 1.** In `geom`, `protected` behaves like package access for every class in the package.

```java
package extra;

public class Point3d extends geom.Point {
    void bump(geom.Point p, Point3d q) {
        q.x++;
        this.x++;
        Point3d.count++;
        geom.Point.count++;
        // p.x++;              // compile-time error: qualifying type is Point
        // new geom.Point();   // compile-time error: protected constructor, other package
    }
}
```

**Listing 2.** Conceptual (second package). Instance `x` needs a `Point3d` (or subclass) receiver. `count` may be named on `Point`. `p` is the wrong qualifying type even though this class extends `Point`.

```d2
direction: down
decl: "protected member of Point" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
pkg: "any class in geom" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
sub: "subclass body outside geom" {
  width: 240
  height: 44
  style.fill: "#e3f2fd"
}
recv: "instance: qualifier is S or subclass of S" {
  width: 300
  height: 48
  style.fill: "#e8f5e9"
}
bad: "other.Point p.x  /  new Point()" {
  width: 260
  height: 48
  style.fill: "#ffcdd2"
}
decl -> pkg
decl -> sub
sub -> recv: "instance field/method"
sub -> bad: "Super-typed receiver or foreign new"
```

**Fig. 1.** Same package is free. Foreign subclasses implement **their** instances, not every `Point`.

> [!warning] A subclass reference is not “any `Point`”
> Inside `Point3d`, `Point p` is still the wrong type for `p.x`. Cast-and-hope is not access: the compile-time qualifier must already be `Point3d` (or a subclass). Code in `Point` also cannot read a `protected` field declared only in `Point3d`.

> [!warning] `protected` is a published subclass API
> Foreign subclasses can depend on it. If you only wanted same-package helpers, omit the modifier (package access) instead of `protected`. `new Super(...)` from another package does not become legal just because you extend `Super`.

> [!tip] Interview answer
> Protected means the whole package plus subclasses in other packages. Outside the package you do not get a Super-typed handle: the receiver of a protected instance member must be your subclass type. Same-package classes do not need to be subclasses. A protected constructor is for super, not for new Super from another package.
