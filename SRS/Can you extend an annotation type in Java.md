<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# Can you extend an annotation type in Java?

> [!abstract] Short answer
> **No.** An `@interface` declaration has **no `extends` clause**. Its only direct superinterface is always `java.lang.annotation.Annotation`. You compose annotations with **annotation-typed members** or **meta-annotations**, not by subclassing.

## `@interface` has a fixed superinterface

An annotation type is a specialized interface: `@` immediately before `interface`. That production does not include `extends` (or type parameters). The compiler therefore cannot parse `public @interface Timed extends Audited { … }` as an annotation declaration — it is a **compile-time error** (the grammar has no `extends` production), not a supported form of annotation inheritance.

The type still has a superinterface: **always** `Annotation`. You do not write that relationship, and you cannot replace it. `Annotation` itself is **not** an annotation type. Methods inherited from it (`equals`, `hashCode`, `toString`, `annotationType`) are **not** annotation elements; you cannot supply them in `@Timed(…)`.

```java
public @interface Audited {}

public @interface Timed extends Audited { // does not compile
    long millis();
}
```

**Listing 1.** Conceptual — an `extends` clause on `@interface` is illegal. Declare `Timed` without `extends`; it already extends `Annotation`.

`Annotation` is an **interface**, not a class. It does not have `Object` as a parent class. Public `Object` methods exist on annotation values because `Annotation` (like other interfaces with no `extends` list) implicitly declares them — not because the annotation type extends `Object`.

## Compose instead of inheriting the type

Two legal ways to reuse another annotation type:

1. **Nested member** — an element whose return type is another annotation interface (or an array of one). That is a field of annotation data, not a subtype.
2. **Meta-annotation** — annotate the `@interface` declaration itself (`@Retention`, `@Target`, or a custom type whose `@Target` includes `ANNOTATION_TYPE`).

```java
@interface Name {
    String first();
    String last();
}

@interface Author {
    Name value();
}

@Author(@Name(first = "Ada", last = "Lovelace"))
class Spec {}
```

**Listing 2.** `Author` **contains** a `Name` value. `Author` does not extend `Name`. Nested array types such as `String[][]` are illegal as elements.

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Audited {}
```

**Listing 3.** `@Retention` and `@Target` are **meta-annotations** on `Audited`. They constrain retention and placement; they do not make `Audited` a subtype of those types.

See [[What object types can an annotation element return]] and [[What are meta-annotations in Java]] for the member-type list and the meta-annotation set. Declaration syntax: [[How do you declare a custom annotation in Java]].

```d2
direction: right
anno: "@interface A\nsuperinterface:\nAnnotation only" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
illegal: "@interface B extends A\ncompile-time error" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
compose: "B has member of type A\nor B is meta-annotated with A" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}

anno -> illegal: "type hierarchy"
anno -> compose: "reuse"
```

**Fig. 1.** Annotation types do not form an inheritance tree of `@interface`s. Reuse is nesting or meta-annotation.

> [!warning] A normal `interface` that `extends` an annotation type is not an annotation
> `interface AuditedOps extends Audited {}` **does compile**. `AuditedOps` is an ordinary interface. It is **not** an annotation type, so `@AuditedOps` on a class or method is illegal. The same rule applies if you `extends java.lang.annotation.Annotation` by hand: that interface still does not become an `@interface`. Do not mix this up with [[How does Inherited annotation inheritance work]] — `@Inherited` only affects **class-level** reflective lookup on subclasses; it does not let one annotation type extend another.

> [!tip] Interview answer
> You cannot extend an annotation type: `@interface` has no `extends` clause, and the only superinterface is `java.lang.annotation.Annotation`. A normal interface that extends an annotation type is not itself an annotation, so you cannot write `@` on it. Reuse another annotation by nesting it as a member or by meta-annotating; `@Inherited` is a different mechanism that only copies class annotations onto subclasses.
