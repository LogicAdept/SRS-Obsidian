<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# What happens if the same ElementType appears twice in Target?

> [!abstract] Short answer
> **A compile-time error.** The `value` array of `@Target` must not contain the same `ElementType` constant more than once. Duplicates are not merged or ignored.

## The rule

`@Target` has a single element, `value`, of type `ElementType[]`. Listing a constant twice is illegal, even if the rest of the declaration is fine.

```java
@Target({ElementType.FIELD, ElementType.TYPE, ElementType.FIELD})
public @interface TestAnnotation {
    int[] value() default {};
}
```

**Listing 1.** Conceptual — does not compile. The second `FIELD` is the error. `int[] value() default {}` is a legal array element with an empty default; it is **not** why compilation fails. Drop one `FIELD` and the type is legal (`TYPE` + `FIELD`).

```java
@Target({ElementType.FIELD, ElementType.METHOD, ElementType.FIELD})
public @interface Bogus {}
```

**Listing 2.** Conceptual — the same error with a shorter type. Placement itself is [[How does the Target meta-annotation restrict annotation placement]]. An **empty** `@Target({})` is a different, legal shape: [[How does an empty Target array affect a custom annotation]].

```d2
direction: right
dup: "@Target({FIELD, TYPE, FIELD})" {
  width: 250
  height: 70
  style.fill: "#ffebee"
}
ok: "@Target({FIELD, TYPE})" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

dup -> ok: "remove duplicate"
```

**Fig. 1.** Repeating a constant is not “more of the same target”; it is ill-formed `@Target`.

The shorthand `@Target(ElementType.FIELD)` is one occurrence of `FIELD` and is legal: [[How does the value element shorthand work]].

> [!warning] The compiler will not treat duplicates as a set
> You cannot “emphasize” `FIELD` by writing it twice. There is no runtime behavior here — the `@interface` never compiles. Do not blame other members (`default {}`, extra targets) until the `ElementType` list is unique.

> [!tip] Interview answer
> If the same ElementType appears twice in @Target, the annotation type does not compile. The language requires unique constants in that array; duplicates are a compile-time error, not a warning or a merge. Fix it by listing each context once.
