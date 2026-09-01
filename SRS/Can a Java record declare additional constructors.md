<!--
reps: 0
priority: 0
-->
#Java/Language/Records/Constructors #SRS

# Can a Java record declare additional constructors?

> [!abstract] Short answer
> **Yes.** Besides the canonical constructor (the one whose parameters match the header), a record may declare other constructors. Every **non-canonical** constructor body must **start** with `this(...)`. That chain has to reach the canonical constructor, which is the only constructor allowed to initialize the component fields. There is no ordinary default constructor; the implicit constructor is the canonical one.

## Extra constructors must chain; the canonical one assigns

```d2
direction: down
extra: "Point() / Point(double x)\nnon-canonical" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
thisCall: "this(x, y)  first statement" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
canon: "canonical Point(double, double)\nvalidate / normalize, then fields" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
extra -> thisCall
thisCall -> canon
```

**Fig. 1.** Additional constructors exist only as overloads that delegate. Component fields are written on the canonical path.

A record with no constructor declarations still gets a **canonical** constructor, not `Point()`. JLS §8.10.4: non-canonical constructors are allowed, but each body must begin with an **alternate constructor invocation** (`this(...)`). `super(...)` is not that form, so it is illegal here. The canonical constructor itself must **not** contain `this(...)` or `super(...)`; it initializes the `private final` component fields (or, in compact form, the compiler assigns them after the compact body). See [[What is a canonical constructor in a Java record]] and [[What methods does the compiler generate for a Java record]].

`this(...)` may name the canonical constructor or another extra constructor. Ordinary constructor rules still forbid a `this(...)` cycle. Because only the canonical constructor is allowed *not* to start with `this(...)`, every `new` path ends there — that is the precise reading of “must invoke the canonical constructor.”

```java
record Point(double x, double y) {
    Point() { this(0.0, 0.0); }
    Point(double x) { this(x, 0.0); }
}

Point origin = new Point();
Point onAxis = new Point(3.0);
```

**Listing 1.** Two extra constructors; both delegate into the implicit canonical `Point(double, double)`.

An extra constructor may take a different type, not only defaulted primitives:

```java
record Pair<T extends Number>(T x, T y) {}

record RectanglePair(double length, double width) {
    public RectanglePair(Pair<Double> corner) {
        this(corner.x().doubleValue(), corner.y().doubleValue());
    }
}
```

**Listing 2.** Non-canonical constructor with a different parameter list; `this(...)` still matches the header.

## Compact canonical plus extra overloads

You may declare a **compact** canonical constructor and additional constructors together. You may **not** declare both a compact constructor and a normal constructor whose signature matches the header — those would be two canonical constructors. Compact details: [[What is a compact constructor in a Java record]].

```java
record Point(double x, double y) {
    public Point {
        if (x < 0 || y < 0)
            throw new IllegalArgumentException("negative");
    }

    Point() { this(0.0, 0.0); }
    Point(double x) { this(x, 0.0); }
}

Point p = new Point(3.0); // Point(double) → this(3.0, 0.0) → compact body, then fields
```

**Listing 3.** `new Point(3.0)` still runs compact validation because the extra constructor chains into the canonical constructor. Field writes happen after that compact body, not in `Point(double)`.

Statements before `this(...)` are illegal, so do not try to validate in an extra constructor and then delegate. Put checks and parameter normalization on the canonical / compact path. After `this(...)` returns, the component fields are already assigned (`final`); assigning `this.x = ...` in the extra constructor is not a substitute for chaining.

> [!warning] Missing `this(...)` is a compile-time error only for non-canonical constructors
> A body that assigns `this.x` / `this.y` and never calls `this(...)` is valid **only** if that constructor **is** the canonical one (header-matching signature). Any other constructor must start with `this(...)`. The canonical constructor must **not** call `this(...)`. Confusing the two is the usual compile failure.

> [!warning] You do not get `new Point()` unless you write it
> No extra constructors means one constructor: the canonical one, with every component. Empty `()` is not generated. If you add `Point() { this(0.0, 0.0); }`, that overload is yours; it still does not assign fields itself.

> [!tip] Interview answer
> **Yes — a record can declare extra constructors, but each one must start with `this(...)` so construction always reaches the canonical constructor that fills the component fields.** A compact canonical constructor still runs when an extra constructor chains into it. There is no implicit default constructor; `super(...)` is illegal in those extra constructors, and a no-arg overload exists only if you write it (or the header is empty).
