<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Library/Lombok #SRS

# What is the difference between a Java record and Lombok Value?

> [!abstract] Short answer
> A record is a **language and JVM type** (Java 16): the header *is* the state, accessors are `x()`, the class extends `java.lang.Record`, and you cannot add extra instance fields or a superclass. Lombok `@Value` is an **annotation processor** that rewrites a **regular class** into something *similar*: `private final` fields, a `final` class, `getX()` JavaBean getters, and generated `equals` / `hashCode` / `toString`. `@Data` is not `@Value` — it generates **setters**. Records do not replace Lombok.

## Semantic type vs generated POJO

```d2
direction: down
rec: "record Point(int x, int y)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
val: "@Value class Point { int x; int y; }" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
rjvm: "class file: extends Record\nRecord attribute, x()" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
lombok: "ordinary class + getX()\nannotation processor" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
rec -> rjvm
val -> lombok
```

**Fig. 1.** JEP 395’s non-goals include “annotation-driven code generation” and JavaBeans naming. `@Value` is exactly that kind of generator.

| | `record` | Lombok `@Value` |
| --- | --- | --- |
| What it is | Restricted class in the language / JVM | `@Value` → `@Getter` + private `final` fields + `@AllArgsConstructor` + `@ToString` + `@EqualsAndHashCode` + class `final` |
| Accessors | `x()` | `getX()` (JavaBean; `isX` for `boolean`) |
| Extra instance fields | Illegal | Allowed — it is still a class |
| Superclass | Always `Record`; no `extends` | May `extends` another class |
| `final` type | Always (not removable) | `final` **by default**; `@NonFinal` can remove it |
| Construction | Canonical / compact constructor | All-args constructor (any explicit constructor suppresses it) |
| Runtime | `Class.isRecord()`, record patterns, record serialization | Ordinary class; no `Record` attribute |
| Tooling | JDK 16+ | Lombok on the compiler classpath |

```java
@Value
public class Point {
    int x;
    int y;
}
// point.getX();

record Point(int x, int y) {}
// point.x();
```

**Listing 1.** Same two ints, different API and different binary. Delombok of `@Value` is a `public final class` with `getX()` / `getY()`.

`@Data` is the **mutable** sibling: getters, **setters on non-final fields**, `toString` / `equals` / `hashCode`, and a required-args constructor. That is a JavaBean, not a record. Prefer records on Java 16+ for new immutable carriers ([[What is the difference between a Java record and a regular class]], [[In which Java version were records standardized]]). Keep Lombok when you need `getX()` for bean-oriented libraries, `@Builder` / `@With`, extra fields, a real superclass, or a pre-16 baseline.

> [!warning] `@Data` is not a record
> `@Value` is “immutable `@Data`”: no setters, fields `final` by default. `@Data` generates setters. Interview dumps that treat `@Data` and records as the same thing fail the mutability check.

> [!warning] Not “syntactic sugar for Lombok”
> A record is not a regular class with generated methods. It cannot grow extra instance fields, cannot `@NonFinal`, cannot `extends Foo`, and the VM stores a `Record` attribute ([[How does the JVM represent a Java record]]). Compact constructors and record serialization have no Lombok equivalent ([[What is a compact constructor in a Java record]]).

> [!tip] Interview answer
> **A record is a JDK 16 language type whose header is the whole state and whose accessors are `x()`; `@Value` is Lombok generating a final JavaBean-style class with `getX()`.** `@Data` is mutable and is not a record. Use records for new immutable data; keep Lombok for builders, bean getters, extra fields, or older JDKs.
