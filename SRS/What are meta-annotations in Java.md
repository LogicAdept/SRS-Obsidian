<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# What are meta-annotations in Java?

> [!abstract] Short answer
> A **meta-annotation** is an annotation **on an annotation interface declaration**. The usual ones live in `java.lang.annotation` and control **where** (`@Target`), **how long** (`@Retention`), **Javadoc** (`@Documented`), **subclass lookup** (`@Inherited`), and **repetition** (`@Repeatable`, Java 8). Any annotation whose target includes annotation declarations can play that role — including `@Deprecated` on an `@interface`.

## The language definition

An annotation on an `@interface` is a meta-annotation. A type may meta-annotate **itself**, and two types may meta-annotate each other; the predefined set does this.

`@Target(ElementType.ANNOTATION_TYPE)` restricts a custom type so it can be written **only** on annotation declarations (a dedicated meta-annotation). Omitting `@Target` also allows annotation declarations (all declaration contexts). Empty `@Target({})` forbids even that: [[How does an empty Target array affect a custom annotation]].

```java
@Documented
@Inherited
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Audited {
    String value() default "";
}
```

**Listing 1.** Typical meta-annotations on a custom type. `@Target` / `@Retention` are almost always required in practice for a runtime class-level marker.

## The `java.lang.annotation` set

| Meta-annotation | Role |
| --- | --- |
| `@Target` | `ElementType` contexts where instances may appear |
| `@Retention` | `SOURCE` / `CLASS` (default) / `RUNTIME` |
| `@Documented` | Instances are part of the annotated element’s **public contract**; javadoc shows them by default. Types **without** `@Documented` are omitted from that output |
| `@Inherited` | Class-level reflective lookup walks **superclasses** |
| `@Repeatable` | Names the **container** type for repeated uses |

`@Native` in the same package marks a **field** constant for native code — not a meta-annotation.

Placement: [[How does the Target meta-annotation restrict annotation placement]]. Retention: [[How do Java annotation retention policies work]]. Subclass lookup: [[How does Inherited annotation inheritance work]]. Repeats: [[How are repeating annotations stored for compatibility]].

```d2
direction: right
meta: "@Target @Retention\n@Documented @Inherited\n@Repeatable" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
anno: "@interface Audited" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
use: "@Audited class C" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}

meta -> anno: "annotates the type"
anno -> use: "annotates a program element"
```

**Fig. 1.** Meta-annotations configure the annotation interface; they are not copied onto every use of `@Audited`.

> [!warning] `@Deprecated` on an `@interface` is a meta-annotation, not one of the five
> It marks the annotation type as discouraged. It does **not** set retention, target, or inheritance. `@Documented` does **not** change retention: a `SOURCE` `@Documented` type still never reaches `getAnnotation`. Javadoc without `@Documented` simply does not treat that annotation as part of the public contract.

> [!tip] Interview answer
> Meta-annotations are annotations on other annotation types. The ones you name in an interview are Target, Retention, Documented, Inherited, and Repeatable — they control placement, lifetime, javadoc, superclass lookup, and repeating. Any annotation allowed on an @interface counts, including Deprecated, but that is not a substitute for Retention or Target.
