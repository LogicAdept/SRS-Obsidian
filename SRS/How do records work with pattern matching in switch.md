<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: records are first-class in deconstruction patterns (Java 21, JEP 440). You can bind components in `switch` or `instanceof` without an explicit cast or accessor call.

```java
sealed interface Shape permits Circle, Rectangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double w, double h) implements Shape {}

double area(Shape s) {
    return switch (s) {
        case Circle(double r) -> Math.PI * r * r;
        case Rectangle(double w, double h) -> w * h;
    };
}

Point p = new Point(42, 0);
if (p instanceof Point(int x, int y)) {
    System.out.println(x + y);
}
```

Records + sealed interfaces + switch pattern matching are described as a visitor-pattern replacement. This is later than the Java 16 record JEP.

> [!warning] Unverified traps from the dump
> - Deconstruction patterns are a Java 21 dump claim, not part of JEP 395 itself.
> - There is no tag-tree leaf yet for pattern matching or sealed types.
