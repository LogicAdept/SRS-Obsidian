<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS

# What is the difference between a Java record and a regular class?

> [!abstract] Short answer
> A record is a **restricted class** whose API is the header: component fields are `private final`, the class is implicitly `final` and extends `java.lang.Record`, and the compiler supplies the canonical constructor, accessors `x()`, `equals`, `hashCode`, and `toString`. A regular class may choose any superclass, any fields, inheritance, and a no-arg constructor. Use a class when you need mutable state, subclassing, or a JPA entity; use a record when the value *is* the components.

## State description vs open class

```d2
direction: down
rec: "record Point(int x, int y)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
cls: "class Point { int x; int y; ... }" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
rlimits: "header = whole instance state\nfinal type, extends Record" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
climits: "you choose fields, superclass,\nconstructors, mutability" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
rec -> rlimits
cls -> climits
```

**Fig. 1.** JEP 395: a record **commits** to an API that matches its state. A normal class may decouple representation from API.

| | Record | Regular class |
| --- | --- | --- |
| Superclass | Always `java.lang.Record`; **no `extends`** | `Object` unless you write `extends` |
| Subclassing | Implicitly `final`; cannot be `abstract` | Allowed (`final` / `abstract` optional) |
| Instance state | Only header components; `private final` | Any fields, including mutable |
| Extra instance fields / instance initializers | Illegal | Allowed |
| Constructor | Canonical (header-shaped); no default `()` | Implicit no-arg if you declare none |
| Accessors | `x()`, not a JavaBean requirement | Often `getX()` by convention |
| `equals` / `hashCode` / `toString` | Derived from components unless you override | `Object` identity unless you override |
| Interfaces | `implements` allowed | `implements` allowed |
| Nested / local | Nested records are implicitly `static` | Nested class is inner unless `static` |

```java
public record Point(int x, int y) {}

// public class Bad extends Point {}        // record is final
// public record Bad extends Object {}      // no extends clause
public record User(String name) implements Serializable {} // interfaces: ok
```

**Listing 1.** The three dump checks: cannot subclass a record, cannot `extends` on a record, `implements` is fine.

Beyond those limits a record still **behaves like a class**: `new`, generics, static members, instance methods, nested types ([[Can a Java record declare static members and instance methods]], [[Can a Java record be generic]]). Generated members: [[What methods does the compiler generate for a Java record]]. Field rules: [[Are Java record fields final]]. JVM picture: [[How does the JVM represent a Java record]].

Reach for a **class** when you need mutable state, a type hierarchy, extra hidden fields, an abstract type, `native` methods, a no-arg constructor, or a JPA `@Entity` ([[Can you use a Java record as a JPA entity]]). Lombok `@Value` is still a regular class with codegen, not this language restriction ([[What is the difference between a Java record and Lombok Value]]).

> [!warning] Implements is not extends
> `implements Comparable<Point>` / `Serializable` is legal. `extends` of a class is not. Do not tell the interviewer that records cannot have a supertype — they always have `Record`, and they may list interfaces.

> [!warning] Shallow immutability is not “no setters on a class”
> Component fields cannot be reassigned, but a mutable component object can still change. A mutable JavaBean class is the right model when identity and in-place updates matter (entities, builders you mutate, caches).

> [!tip] Interview answer
> **A record is a final class that extends `Record` and whose whole instance state is the header — private final fields, canonical constructor, `x()` accessors, and component-based `equals` / `hashCode` / `toString`.** A regular class can extend, mutate, and hide state. Pick a record for an immutable data carrier; pick a class for entities, hierarchies, and anything that is not just those components.
