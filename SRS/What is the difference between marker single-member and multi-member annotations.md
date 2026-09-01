<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# What is the difference between marker single-member and multi-member annotations?

> [!abstract] Short answer
> Three **use-site shapes** of the same construct. A **marker** is `@Name` with **no element values** (shorthand for `@Name()`). A **single-member** (single-element) form is `@Name(expr)`, shorthand for `@Name(value = expr)`. A **multi-member** use is a **normal** annotation: `@Name(a = …, b = …)` with explicit names. The **interface** side matches: no elements, one element, or several.

## Interface vs use-site

A **marker annotation interface** declares **no** elements. Presence is the whole payload — `@Override`, `@FunctionalInterface`, `@Preliminary {}`. Prefer that over a boolean flag you always set to `true`.

A **single-element annotation interface** declares **one** element. By convention it is named `value`, which unlocks [[How does the value element shorthand work]]: `@Copyright("…")` means `@Copyright(value = "…")`.

Several elements → a **normal** annotation: every element-value pair is `name = …`. You must supply a pair for every element that has **no** default. Interview dumps call this **multi-member**.

All three are still annotation types: they can take `@Target` / `@Retention` like any other [[What is a Java annotation]].

```java
@interface Flag {}                          // marker interface
@interface Copyright { String value(); }    // single-element
@interface Window { int min(); int max(); } // several elements

@Flag
@Copyright("Yoyodyne")
@Window(min = 1, max = 80)
class Widget {}
```

**Listing 1.** Three declarations and the three matching use-site forms.

The shorthands are **not** locked to those interface shapes. `@Name` is legal even when the interface **has** elements, if **every** element has a default (`@Deprecated` is the usual example). `@Name(expr)` is legal on a **multi-element** type if one element is `value` and the rest have defaults.

```d2
direction: right
m: "@Name\nmarker" {
  width: 140
  height: 70
  style.fill: "#e3f2fd"
}
s: "@Name(expr)\nsingle-element" {
  width: 160
  height: 70
  style.fill: "#e8f5e9"
}
n: "@Name(a=…, b=…)\nnormal / multi" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}

m -> s: "add value"
s -> n: "named pairs"
```

**Fig. 1.** Same `@` token; richness is how many element-value pairs you write.

> [!warning] `value` is required for the parentheses shorthand
> A lone element named `label()` is **not** a single-element *use*. `@Foo("x")` looks for `value`. You must write `@Foo(label = "x")`. Empty `@Bar` does **not** prove `Bar` has no elements — every element may simply have a default.

> [!tip] Interview answer
> Marker means no values at the use site, typically an empty @interface. Single-member means one element, conventionally value, so you can omit the name. Multi-member means a normal annotation with explicit names for each element you set. The compiler still expands the first two to the normal form; a type with only defaulted elements can still be written as a marker.
