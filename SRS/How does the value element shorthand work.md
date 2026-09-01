<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# How does the value element shorthand work?

> [!abstract] Short answer
> `@Foo(v)` is **exactly** `@Foo(value = v)`. The omitted name must be the element **`value`**. That form is legal when `value` exists and **every other** element has a **default** (or there are no other elements). An element named `time` or `id` does **not** get this shorthand.

## Three syntactic forms

Normal annotations list `name =` pairs. Two shorthands exist:

| Form | Means | When it is legal |
| --- | --- | --- |
| `@Foo` | `@Foo()` | Marker — no elements, **or** every element has a default |
| `@Foo(v)` | `@Foo(value = v)` | A `value` element exists; all **other** elements have defaults |
| `@Foo(id = 1, name = "x")` | itself | Every element without a default is supplied |

```java
@SuppressWarnings("unchecked")
void raw() {}
```

**Listing 1.** Same as `@SuppressWarnings(value = "unchecked")`. `SuppressWarnings` is a single-element interface whose element is `value`. Marker vs single- vs multi-member: [[What is the difference between marker single-member and multi-member annotations]].

```java
@interface Schedule {
    String time();
}

@Schedule("morning")          // compile-time error — no element named value
@Schedule(time = "morning")   // legal
class Job {}
```

**Listing 2.** Conceptual — the shorthand is **name-based**, not “whatever the only member is.”

A type with several elements can still use `@Foo(v)` **if** the unnamed slot is `value` and the rest are defaulted. If two members lack defaults, you must write a **normal** annotation (`value = …` plus the other names). `@Foo("x", other = 1)` is not a legal mix of the two forms.

## Arrays and defaults

If the element type is an **array**, braces may be omitted for a **single** component: `@Endorsers("Epicurus")` is `{ "Epicurus" }`. Several values need braces: `@Endorsers({"A", "B"})`. Nested arrays are illegal as element types: [[What object types can an annotation element return]].

Every non-defaulted element must appear, or it is a compile-time error. A defaulted element may be omitted; the default is applied **when the annotation is read**, not baked into older class files. Element values (and defaults) must be **commensurate**: primitives/`String` are **constant expressions**, `Class` is a class literal, enums are constants, nested annotations are annotations — never `null`.

`@Target(ElementType.METHOD)` is the same shorthand on a meta-annotation (`value` is `ElementType[]`): [[How does the Target meta-annotation restrict annotation placement]].

```d2
direction: right
short: "@Foo(\"hi\")" {
  width: 160
  height: 60
  style.fill: "#e3f2fd"
}
full: "@Foo(value = \"hi\")" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}
bad: "@Foo(time = …)\nno shorthand" {
  width: 180
  height: 70
  style.fill: "#ffebee"
}

short -> full: "desugars"
```

**Fig. 1.** Only the element named `value` can drop its name in `@Foo(…)`.

> [!warning] `@Foo(v)` never binds `v` to a differently named lone element
> If the only member is `time()`, you still write `time = …`. The compiler does not “guess” the unique name. Using the single-element form when `value` is missing, or when another required member has no default, is a compile-time error.

> [!tip] Interview answer
> If the element is named value, you can write @Foo("x") instead of @Foo(value = "x"); that also works when other elements exist but all have defaults. The name value is required for the shorthand — a lone time() still needs time =. A one-element array can drop the braces; everything without a default must still be supplied in the normal name = form.
