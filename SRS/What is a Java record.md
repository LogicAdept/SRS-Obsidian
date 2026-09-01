<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Versions/16 #SRS

# What is a Java record?

> [!abstract] Short answer
> A record is a **restricted class** that is a **shallowly immutable, transparent carrier** for a fixed set of values. The header *is* the state: `record Point(int x, int y) {}` commits to private `final` component fields, a canonical constructor, accessors `x()` / `y()`, and component-based `equals`, `hashCode`, and `toString`. Preview in JDK **14** and **15**; **standard from JDK 16**. Implicitly `final`, always extends `java.lang.Record`, may `implements` interfaces.

## Header is the API

```d2
direction: down
header: "record Point(int x, int y)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
state: "private final int x, y\ncanonical Point(int, int)" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
api: "x() / y()\nequals / hashCode / toString" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
limits: "implicitly final\nextends Record\nno extra instance fields" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
header -> state
state -> api
header -> limits
```

**Fig. 1.** The header is the state description. Construction, access, equality, and display are derived from it; the type cannot grow extra instance state or a subclass.

The point is **modeling data as data**, not a war on boilerplate and not a JavaBean DTO keyword. You give up hiding representation behind a different API. A record always extends `Record` and has **no `extends` clause** (same idea as an enum always extending `Enum`). Nested records are implicitly `static`. A copy through the accessors must equal the original: `new Point(p.x(), p.y())` equals `p` when accessors and `equals` behave as specified.

```java
public record Point(int x, int y) implements Comparable<Point> {
    @Override
    public int compareTo(Point o) {
        int cmp = Integer.compare(x, o.x);
        return cmp != 0 ? cmp : Integer.compare(y, o.y);
    }

    public static void main(String[] args) {
        Point a = new Point(3, 4);
        Point b = new Point(3, 4);
        a.x();
        a.equals(b);

        record Row(int x, int y) {}
        Row row = new Row(a.x(), a.y());
        new Point(row.x(), row.y()).equals(a);
    }
}

// class Sub extends Point {}     // illegal: record is implicitly final
// record Bad extends Object {}   // illegal: no extends clause
```

**Listing 1.** Header-derived API: `x()`, not `getX()`; `implements` allowed; a **local record** for an intermediate pair. Subclassing and `extends` are compile errors.

| What you get | What you do not get |
| --- | --- |
| `private final` field per component | Setters, extra instance fields, instance initializers |
| Canonical constructor (header-shaped) | A default no-arg constructor |
| Public accessor `name()`, not `getName()` | JavaBean getter naming |
| `equals` / `hashCode` / `toString` from **fields** | Identity equality from `Object` |
| `implements` interfaces; static members; instance methods; generics; local records | `abstract`, `native` methods, `extends` a class, annotation codegen |

Beyond those limits a record still **behaves like a class**: `new`, nested types, static fields and methods ([[Can a Java record declare static members and instance methods]]). Generated members: [[What methods does the compiler generate for a Java record]]. Versus an ordinary class: [[What is the difference between a Java record and a regular class]]. Versus Lombok `@Value`: [[What is the difference between a Java record and Lombok Value]]. Version: [[In which Java version were records standardized]]. Local form: [[Can you declare a record inside a Java method]]. Field rules: [[Are Java record fields final]]. Validation belongs in the canonical or compact constructor ([[What is a compact constructor in a Java record]]), not in an accessor that “fixes up” the value on the way out.

> [!warning] Implicitly final is not “no supertype”
> You cannot **subclass** a record because it is implicitly `final`. You cannot write `extends` on a record because the superclass is always `Record`. Those are two different rules. `implements Serializable` / `Comparable` is legal. Do not explain “you cannot inherit from records” as “Java has no multiple inheritance.”

> [!warning] 14 was preview, 16 is the language
> JDK 14 and 15 shipped records behind `--enable-preview`. `java.lang.Record` is **since 16**. Dump cues that say “Java 14+” collapse preview and standard. An empty body is a complete type; you may still add a compact constructor, methods, and `implements`.

> [!warning] Shallow immutability, not a JavaBean or Lombok DTO
> Component fields cannot be reassigned, but a mutable component object can still change. There is no setter and no `getX()`. Records are not aimed at mutable JavaBean classes or annotation-driven codegen. A record can *serve as* a DTO when the API is the components; it is not “for tests only,” and frameworks that demand a no-arg constructor or `getX()` still need a class. Implicit `equals` / `hashCode` / `toString` read the **fields**, not the accessors.

> [!tip] Interview answer
> **A record is a final class, previewed in Java 14/15 and standardized in 16, whose whole instance state is the header — private final fields, a canonical constructor, `x()` accessors, and component-based `equals` / `hashCode` / `toString`.** It always extends `Record`, never another class, and may implement interfaces. Use it as a shallowly immutable data carrier, including a local record for an intermediate value — not as a JavaBean, a Lombok stand-in, or a type you subclass.
