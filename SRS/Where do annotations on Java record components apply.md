<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Annotations #SRS

# Where do annotations on Java record components apply?

> [!abstract] Short answer
> An annotation on a header component is **not copied to “all three” sites blindly**. It is **propagated to each implicit member whose declaration context matches that annotation’s `@Target`**: `FIELD` → the private field, `METHOD` → the accessor, `PARAMETER` → the canonical-constructor parameter (or the compact constructor’s implicit parameters). `TYPE_USE` also lands on those types. Runtime reflection on the **component itself** (`RecordComponent.getAnnotation`) sees the annotation only if it is meta-annotated `@Target(RECORD_COMPONENT)`.

## `@Target` chooses the copies

```d2
direction: down
comp: "record User(@A String name)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
field: "private final String name\nif FIELD or TYPE_USE" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
acc: "public String name()\nif METHOD or TYPE_USE" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
param: "User(String name) param\nif PARAMETER or TYPE_USE" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
comp -> field
comp -> acc
comp -> param
```

**Fig. 1.** JEP 395: “all of the elements to which this particular annotation is applicable.” JLS §8.10.1: reflection on the component and propagation to members are **independent**.

JLS §9.7.4: a record-component location is one of the places an annotation may be a declaration annotation, a type annotation, or both. It is a compile-time error to write `@A` there unless `A` is applicable to **at least one of** record-component, field, method, or formal-parameter declarations, or to type contexts. So `@Target(ElementType.FIELD)` alone is already legal on a component — you do not need `RECORD_COMPONENT` for the source to compile.

`ElementType.RECORD_COMPONENT` exists since Java 16. JEP 395: a declaration annotation on a component is **not** in `RecordComponent`’s reflective set unless that meta-annotation is present. Field/method/parameter copies can still exist.

```java
@Target(ElementType.FIELD)
@interface OnField {}

@Target(ElementType.METHOD)
@interface OnMethod {}

@Target(ElementType.PARAMETER)
@interface OnParam {}

@Target(ElementType.RECORD_COMPONENT)
@interface OnComponent {}

public record User(
        @OnField @OnMethod @OnParam @OnComponent String name) {}
```

**Listing 1.** `@OnField` appears on the field, `@OnMethod` on `name()`, `@OnParam` on the implicit constructor parameter, `@OnComponent` on the component for `getRecordComponents()`. Mix and match; nothing is “always all three.”

If you **explicitly declare** the accessor or a **non-compact** canonical constructor, **nothing is propagated onto those members** — they keep only the annotations written on them. Compact constructors still receive applicable parameter annotations on the implicit parameters. You may put different annotations on an explicit constructor parameter than on the component (JLS §8.10.4.1 `Person` / `@Foo` vs `@Bar`).

Jackson `@JsonProperty` is typically targeted at field, method, and parameter, so it belongs on the **component** ([[How do you serialize a Java record with Jackson]]). Bean Validation (`@NotBlank`, `@Min`) follows the **same `@Target` rule** — Spring examples next to a compact constructor are extra checks, not a second propagation mechanism. Inspect copies with `getDeclaredField` / `getDeclaredMethod` / constructor parameters; inspect the header with [[How do you inspect a Java record with reflection]].

> [!warning] “Always field + accessor + parameter” is false
> `@Target({FIELD})` never annotates `name()`. `@Target({METHOD})` never annotates the field. An annotation with only `@Target(TYPE)` cannot sit on a component at all.

> [!warning] Explicit members drop the copies
> `public String name() { return name; }` does not inherit component annotations. Repeat them on the method if a framework looks at getters. Same for an explicit `User(String name)` canonical constructor.

> [!tip] Interview answer
> **Annotations on a record component are copied to the implicit field, accessor, and constructor parameter only where that annotation’s `@Target` allows — not automatically to all three.** `RECORD_COMPONENT` is required for `RecordComponent` reflection, not for writing `@JsonProperty` on the header. Explicit accessors or a full canonical constructor do not receive those copies.
