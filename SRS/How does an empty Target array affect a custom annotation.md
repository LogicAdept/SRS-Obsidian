<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# How does an empty Target array affect a custom annotation?

> [!abstract] Short answer
> `@Target({})` makes the annotation interface **inapplicable in every declaration and type context**. You **cannot** write it as a modifier on a class, method, field, package, or even another `@interface`. The `@interface` is still legal; it is meant only as a **member type** inside a larger annotation declaration (an element type, or a nested type).

## Empty array vs omitted `@Target`

`@Target` lists the `ElementType` constants where instances may appear. An **empty** `value` array lists **none**, so the compiler rejects every standalone use (`@Foo` on a program element is a compile-time error).

**Omitting** `@Target` is the opposite: the type is applicable in **all declaration contexts** (and in no type contexts). Empty is not “default”; it is **zero contexts**. Placement: [[How does the Target meta-annotation restrict annotation placement]] and [[Which program elements can be annotated in Java]].

Duplicate constants in one `@Target` are a separate compile-time error: [[What happens if the same ElementType appears twice in Target]].

```java
@Target({})
public @interface Name {
    String first();
    String last();
}

public @interface Author {
    Name value();
}

@Author(@Name(first = "Ada", last = "Lovelace"))
public class Spec {}
```

**Listing 1.** `Name` cannot be written as `@Name` on `Spec`. It is legal as the **element type** of `Author`. Member types of an annotation interface are listed in [[What object types can an annotation element return]].

```java
@Target({})
public @interface Name { String first(); String last(); }

@Name(first = "Ada", last = "Lovelace") // compile-time error
public class Spec {}
```

**Listing 2.** Conceptual — standalone use of a `@Target({})` type is illegal even though the `@interface` compiled.

```d2
direction: right
empty: "@Target({})\nzero contexts" {
  width: 200
  height: 80
  style.fill: "#ffebee"
}
omit: "no @Target\nall declarations" {
  width: 210
  height: 80
  style.fill: "#e8f5e9"
}
nested: "element / nested member\nstill legal" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}

empty -> nested: "only this"
omit -> nested: "and @Foo on types"
```

**Fig. 1.** Empty `@Target` forbids `@Foo` as a modifier; it does not forbid using `Foo` as a nested annotation value.

> [!warning] `@Target({})` is not a meta-annotation target
> `ANNOTATION_TYPE` is what allows `@Foo` **on** another annotation interface. An empty array forbids that too. Use `@Target({})` only when the type should appear as a **value** (or nested type) inside a containing annotation, never as `@Foo` itself.

> [!tip] Interview answer
> @Target({}) means the annotation cannot be applied to any program element — not even as a meta-annotation. That is the opposite of omitting @Target, which allows every declaration context. The empty-target type still exists so you can nest it as a member of another annotation; writing it on a class or method is a compile-time error.
