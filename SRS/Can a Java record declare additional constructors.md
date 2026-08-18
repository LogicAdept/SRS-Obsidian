<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. Extra constructors must delegate to the canonical constructor as their first statement (`this(...)`).

```java
record Point(double x, double y) {
    Point() { this(0.0, 0.0); }
    Point(double x) { this(x, 0.0); }
}

Point origin = new Point();
Point onAxis = new Point(3.0);
```

You can combine extra constructors with a compact canonical constructor: `new Point(3)` still runs the compact validation because it chains to the canonical constructor.

> [!warning] Unverified traps from the dump
> - A constructor body that never calls `this(...)` is a compile error.
> - Field assignment still happens only on the canonical path.
