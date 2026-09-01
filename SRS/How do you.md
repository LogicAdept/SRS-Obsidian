<!--
reps: 0
priority: 0
-->
#Java/Annotations #Java/Versions/8 #SRS

# How do you

> [!abstract] Short answer
> **You declare two annotation types.** The repeatable one is meta-annotated `@Repeatable(Container.class)`. The container is another `@interface` whose `value()` returns `T[]`; any other container elements must have defaults. Java 8 (`@Repeatable` is `@since 1.8`). Repeating `@T` at one site is then legal; the compiler stores one container.

## Repeatable type plus a container whose `value()` is `T[]`

`@Repeatable` is a meta-annotation in `java.lang.annotation`. Its `value` names the **containing** type. `@Repeatable` itself cannot be repeated, so there is only one container per repeatable type. A container wraps at most one repeatable type. The repeatable type cannot name **itself** as the container ([[What are meta-annotations in Java]], [[How do you declare a repeatable annotation in Java]]).

The container is well-formed only if:

- `value()` returns `T[]`, not `Object[]` or some other array
- every other method on the container has a default
- the container is retained **at least as long** as `T` (`SOURCE` / `CLASS` / `RUNTIME`)
- `T` is applicable to at least the program-element kinds the container is applicable to
- if `T` is `@Documented` or `@Inherited`, the container is too (the reverse is allowed)

Those last rules are why a casual container with the wrong `@Target` or shorter `@Retention` fails to compile, even when `value()` looks right ([[Which program elements can be annotated in Java]], [[What happens if you omit Retention on a custom annotation]]).

```d2
direction: down
t: "@Repeatable(Tags.class)\n@interface Tag" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
c: "@interface Tags\nTag[] value()" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
use: "@Tag(\"a\") @Tag(\"b\")\n→ one @Tags container" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

t -> c: "names container"
t -> use: "repeat at one site"
```

**Fig. 1.** Two types. Repeated `@Tag` is stored as one `@Tags` whose `value` is the `@Tag` array ([[How are repeating annotations stored for compatibility]]).

```java
import java.lang.annotation.Repeatable;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
@Repeatable(Tags.class)
@interface Tag {
    String value();
}

@Retention(RetentionPolicy.RUNTIME)
@interface Tags {
    Tag[] value();
}

@Tag("a")
@Tag("b")
class Demo {}
```

**Listing 1.** Legal Java 8 pair. `Tags.value()` is `Tag[]`. Same `RUNTIME` retention so reflection can see the repeats. Extra elements on `Tag` (for example a defaulted `birthday()`) are fine; extra elements on `Tags` need defaults.

At a site with several `@Tag`, it is as if those `@Tag`s were omitted and one `@Tags` were declared. You cannot mix several `@Tag` with an explicit `@Tags` on the same site. Read repeats through the container with `getAnnotationsByType(Tag.class)`; `getAnnotation(Tag.class)` does not unwrap ([[How do you retrieve annotations at runtime]]).

> [!warning] `@Repeatable(FooContainer.class)` is not enough by itself
> If `FooContainer.value()` is not `Foo[]` — `Object[]` is the usual dump mistake — the `@Repeatable` annotation is a compile-time error. Wrong `@Target` on the container (kinds `T` does not cover) or a **shorter** retention than `T` is the same class of error.

> [!warning] One container instance, not a bag of `@Tag` in the class file
> A single `@Tag` is stored as `@Tag`. Two or more become `@Tags`. `getAnnotation(Tag.class)` then misses the repeats unless you ask for the container or use `getAnnotationsByType`. Default retention is `CLASS`, so omitting `@Retention(RUNTIME)` hides both types from runtime lookup.

> [!tip] Interview answer
> **A repeatable annotation is an ordinary `@interface` marked `@Repeatable(Container.class)`, plus a container whose `value()` is an array of that type.** That pair arrived in Java 8. The compiler packs repeats into the container; use `getAnnotationsByType` to read them, and keep container retention and `@Target` compatible with the repeatable type.
