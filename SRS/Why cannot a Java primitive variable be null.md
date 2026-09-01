<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# Why cannot a Java primitive variable be `null`?

> [!abstract] Short answer
> **`null` is a reference that points to no object.** A primitive variable holds a **value** of that exact primitive type (`0`, `false`, `'\u0000'`, …) — never a reference — so `int x = null` does not compile. Wrappers are references and **can** be `null`. Unboxing that `null` (`int y = boxed`) compiles and throws `NullPointerException`.

## `null` is not a primitive value

The `null` literal has the **null type**. That value may be assigned to any **reference** type. It is not one of the primitive values (`true`/`false`, the numeric values, `char`s). A primitive variable always holds a primitive value of its own type; there is no conversion from the null type to `int` / `boolean` / `char`.

```d2
direction: down
prim: "int n\nmust hold a 32-bit value" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
wrap: "Integer n\nreference or null" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
npe: "int y = boxedNull\nunbox → NPE" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
wrap -> npe
```

**Fig. 1.** Primitives store bits; only wrappers store “no object.”

```java
// int primitiveAge = null;      // compile-time error

Integer boxed = null;            // legal — reference
int x = boxed;                   // compiles; unbox intValue() → NPE
```

**Listing 1.** Conceptual: `null` on `int` is rejected; `null` on `Integer` then unboxed is a runtime throw ([[What method does the compiler insert when unboxing an Integer]], [[What is NullPointerException]]).

Field defaults follow the same split: `int` → `0`, `boolean` → `false`, `char` → `'\u0000'`; any wrapper field → `null` ([[What default values do wrapper-typed fields receive in Java]]). Locals of either kind have no default.

That is why wrappers exist for “optional number” and collections: the object type system includes `null`; the primitive type system does not ([[Why are wrapper classes needed in Java]], [[What is the difference between int and Integer in Java]]).

> [!warning] `Integer x = null; int y = x;` is not a compile error
> The conversion is unboxing from `Integer`, which is legal. Failure is at run time when `intValue()` runs on `null`. The compile error is only the **literal** (or other null-typed expression) assigned straight to a primitive: `int y = null`.

> [!tip] Interview answer
> **`null` means “no object,” and primitives are not objects.** An `int` always holds a number, so `int n = null` does not compile. Use `Integer` when you need absence; then remember that unboxing that `null` is `NullPointerException`, not a default `0`.
