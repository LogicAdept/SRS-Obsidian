<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Versions/21 #Java/Language/Switch #SRS

# How do records work with pattern matching in switch?

> [!abstract] Short answer
> In Java 21 a **record pattern** such as `Circle(double r)` can appear in a `case` label (or in `instanceof`). If the selector is an instance of that record, the language invokes each component accessor and binds the results to pattern variables — no cast and no explicit `radius()` call. With a **sealed** hierarchy of records, covering every permitted type makes the `switch` exhaustive, so `default` is not required.

## Record patterns deconstruct; type patterns do not

```d2
direction: down
sel: "switch (shape)" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
pat: "case Circle(double r)" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
acc: "invoke Circle.radius()\nbind r" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
sel -> pat: "record pattern"
pat -> acc
```

**Fig. 1.** A record pattern is a type test plus deconstruction. Matching calls accessors, then initializes the pattern variables.

JLS §14.30.1: a record pattern is `RecordType(component patterns…)`. The type must name a record class; the pattern list length must equal the component list. JEP 440 (final in JDK 21; preview in 19/20) co-evolved with pattern matching for `switch` (JEP 441). This is **not** part of JEP 395 (Java 16 records). Records themselves only promised later deconstruction. See [[In which Java version were records standardized]] and [[What is the difference between pattern matching and a switch statement]].

Two `case` forms:

- **Type pattern** — `case Circle c` binds the whole record; you still call `c.radius()`.
- **Record pattern** — `case Circle(double r)` binds components. Nested record patterns take the object graph apart in one label.

`var` in a component pattern infers the component type (`Point(var x, var y)`). A raw generic record pattern infers type arguments (`case MyPair(var f, var s)` on a `MyPair<String, Integer>`). See [[Can a Java record be generic]].

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
```

**Listing 1.** Record patterns in a `switch` expression. `Shape` is sealed and both permitted records are covered, so the switch is exhaustive — no `default`. Same Shape/Circle/Rectangle setup as the Java SE 21 pattern-matching tutorial, using deconstruction instead of `case Circle c`.

```java
record Point(int x, int y) {}

if (p instanceof Point(int x, int y)) {
    System.out.println(x + y);
}
```

**Listing 2.** The same record pattern works in `instanceof` (JEP 440). The compiler calls `x()` and `y()` for you.

Nested example: `Rectangle(ColoredPoint(Point(var x, var y), var c), var lr)` matches only if every nested pattern matches.

## Exhaustiveness, `null`, and accessors

A `switch` **expression**, and any `switch` **statement** that uses patterns or `null`, must be exhaustive. For an abstract sealed type, covering every permitted subtype is enough (JLS §14.11; records are implicitly `final`, so they can be permitted subtypes). That is the closed-set dispatch people used to write as a visitor over an ADT — [[How would you explain Sealed classes]].

`null` does **not** match any record pattern. If the selector is `null` and there is no `case null`, the switch throws `NullPointerException`. `case null, default` is the combined leftover label.

Matching a record pattern invokes **accessor methods**, not the fields. If an accessor completes abruptly, pattern matching throws `MatchException` with that cause. An explicit accessor that does not return the stored component therefore changes what the pattern binds — [[Can you override a record accessor method]].

```java
record Box<T>(T t) {}

int unwrap(Box<String> b) {
    return switch (b) { // exhaustive for this parameterization
        case Box<String>(String s) -> s.length();
    };
}
```

**Listing 3.** A record pattern that covers every component type covers the record type, so this `switch` on `Box<String>` needs no `default`.

> [!warning] `null` is not a `Circle(...)`
> A record pattern never matches `null`. Enhanced switches still throw `NullPointerException` on a null selector unless you write `case null`. Nested components that are reference types fail the whole record pattern if that nested type pattern does not match (including null, unless the nested type pattern is null-matching).

> [!warning] Accessors run; a throwing accessor is `MatchException`
> Deconstruction is not field access. A logging or copying accessor runs on every match. If it throws, you get `MatchException`, not a silent bind. Keep accessors consistent with the stored components if you use record patterns.

> [!tip] Interview answer
> **Java 21 record patterns let a `switch` (or `instanceof`) test the record type and bind components in one step, by calling the accessors.** Combine them with a sealed interface of records and the compiler can prove the switch is exhaustive without `default`. This came with JEP 440/441, years after records themselves in Java 16.
