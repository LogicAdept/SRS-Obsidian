<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# How are repeating annotations stored for compatibility?

> [!abstract] Short answer
> **In a container annotation.** When two or more annotations of a `@Repeatable` type appear on the same element, the compiler **replaces** them with **one** implicitly declared annotation of the **containing** type. The class file stores that container (its `value` array holds the repeats in source order). Legacy `getAnnotation` / `getAnnotations` still see a **single** annotation — the container — so pre-Java 8 readers keep working.

## Why a container exists

Java 8 allowed the same annotation interface to appear more than once, but the class-file and reflection model was built around **at most one** annotation of a given type per element (`RuntimeVisibleAnnotations` and friends). Wrapping repeats in a **user-declared** container type preserves that shape: old code that already read a container (or that expected a single annotation) still links; new code uses `getAnnotationsByType` / `getDeclaredAnnotationsByType`, which **look through** the container.

You declare both types. `@Repeatable(Schedules.class)` names the container; the compiler does **not** invent the container type.

```java
import java.lang.annotation.Repeatable;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
@interface Schedules {
    Schedule[] value();
}

@Retention(RetentionPolicy.RUNTIME)
@Repeatable(Schedules.class)
@interface Schedule {
    String time() default "morning";
}

@Schedule(time = "morning")
@Schedule(time = "night")
class Job {}
```

**Listing 1.** `Schedules` is the containing type: a `value()` method whose return type is `Schedule[]`. Two `@Schedule` uses become one implicit `@Schedules({@Schedule(time = "morning"), @Schedule(time = "night")})` on `Job`.

A containing type is well-formed only if:

- `value()` returns `A[]` (not `Object[]`, not a different annotation array)
- every **other** method on the container has a **default**
- the container is retained **at least as long** as the repeatable type (`RUNTIME` can contain `CLASS` or `SOURCE`; the reverse is illegal)
- the container’s `@Target` kinds are a **subset** of the repeatable type’s (with the documented `TYPE` / `ANNOTATION_TYPE` / `TYPE_USE` exceptions)
- if the repeatable type is `@Documented` or `@Inherited`, the container **must** be too (the container may have those meta-annotations even when the repeatable type does not)

`@Repeatable` without a legal container is a **compile-time error**. A malformed class file that claims `@Repeatable` but whose container lacks `T[] value()` surfaces as `AnnotationFormatError` at runtime. Declaration details: [[How do you declare a repeatable annotation in Java]]. Retention pairing: [[How do Java annotation retention policies work]].

## What reflection actually sees

On the annotated element the container is **directly present**. Each repeated annotation is only **indirectly present** (inside `value`).

| Method | After two `@Schedule` |
| --- | --- |
| `getAnnotation(Schedule.class)` / `getDeclaredAnnotation` | `null` — `Schedule` is not directly present |
| `getAnnotations()` / `getDeclaredAnnotations()` | the **`Schedules`** instance, not the two `Schedule`s |
| `getAnnotationsByType(Schedule.class)` / `getDeclaredAnnotationsByType` | unwraps the container; returns both `Schedule`s in `value` order |

Making an existing type `T` `@Repeatable` with an already-used container `TC` is **source- and binary-compatible**. `getAnnotation` / `getAnnotations` keep returning `TC` as before. `getAnnotationsByType(T.class)` **changes**: it starts looking through `TC`. Adding a second `@T` is also source- and binary-compatible, but **not** behaviorally compatible for the old single-annotation methods — they stop seeing `T` and see only `TC`. Runtime lookup: [[How do you retrieve annotations at runtime]].

```d2
direction: right
source: "source\n@Schedule @Schedule" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
container: "class file\none @Schedules\nvalue = [s1, s2]" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
legacy: "getAnnotation(Schedule)\nnull" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}
unwrap: "getAnnotationsByType\n[s1, s2]" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}

source -> container: "compile"
container -> legacy: "directly present\nis Schedules"
container -> unwrap: "look through"
```

**Fig. 1.** Repeats are stored as one container annotation so the class file still has a single annotation of that containing type.

> [!warning] One `@Schedule` is not wrapped
> A **single** `@Schedule` is stored as `@Schedule`. No container is synthesized. Mixing **several** `@Schedule` with an **explicit** `@Schedules` on the same element is a compile-time error (it would need nested containers and would change what reflective code already sees on `@Schedules`). One `@Schedule` plus one `@Schedules` is legal: there is nothing to wrap. Do not treat `@Inherited` on the repeatable type as a substitute for putting `@Inherited` on the **container** — class-level lookup walks the container; see [[How does Inherited annotation inheritance work]].

> [!tip] Interview answer
> Repeating annotations are stored in a container type you declare and name with `@Repeatable`. The compiler folds multiple occurrences into one container annotation whose `value` array holds the repeats, which is why old `getAnnotation` still sees a single annotation. Use `getAnnotationsByType` to unwrap; a lone occurrence is not wrapped, and the container needs `T[] value()`, retention at least as long as `T`, and `@Inherited` on the container whenever `T` is inherited.
