<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers/Autoboxing/Cache #Java/Language/Primitives #SRS

# What are `Boolean.TRUE` and `Boolean.FALSE`?

> [!abstract] Short answer
> They are the two **`public static final Boolean` constants** for primitive `true` and `false`. OpenJDK initializes them once (`TRUE = new Boolean(true)`, `FALSE = new Boolean(false)`). `Boolean.valueOf(boolean)` **returns exactly those instances** (`b ? TRUE : FALSE`). Autoboxing a `boolean` and `valueOf(String)` (via `parseBoolean`) also resolve to them. They are not a third boolean state — `null` on a `Boolean` variable is.

## The only two interned `Boolean` objects

JavaDoc: `TRUE` is “the `Boolean` object corresponding to the primitive value `true`”; `FALSE` is the same for `false`. That is the entire cache: unlike `Integer`, there is no range to extend. `valueOf(boolean)` has been the preferred factory since 1.4 because it returns these constants instead of allocating. The `Boolean(boolean)` constructor is deprecated (for removal) for that reason.

Boxing conversion of a `boolean` constant `true`/`false` is specified to yield indistinguishable references (`==`). Combined with `valueOf`, `Boolean b = true;` is `TRUE`.

```d2
direction: down
prim: "boolean true / false" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
vo: "valueOf / autoboxing\nvalueOf(String)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
c: "Boolean.TRUE  or  Boolean.FALSE" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
neu: "new Boolean(true)\ndistinct deprecated instance" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}

prim -> vo
vo -> c
prim -> neu: "avoid"
```

**Fig. 1.** Factories and autoboxing share two constants; `new Boolean` does not.

```java
Boolean.valueOf(true) == Boolean.TRUE;   // true
Boolean.valueOf(false) == Boolean.FALSE; // true
Boolean boxed = true;                    // TRUE
Boolean.valueOf("TRUE") == Boolean.TRUE; // true — see [[How does the Boolean wrapper interpret a String argument]]

new Boolean(true) == Boolean.TRUE;       // false — distinct object
```

**Listing 1.** Conceptual: identity holds for `valueOf` / boxing, not for the deprecated constructor.

`booleanValue()` on `TRUE`/`FALSE` returns the primitive. The constants are immutable `final` wrappers ([[Are Java wrapper types immutable]]). A `Boolean` **field** can still be `null` to mean unset; that is a third state of the *variable*, not a third constant ([[Why cannot a Java primitive variable be null]]).

> [!warning] `== TRUE` is not a substitute for `booleanValue()`
> `if (flag == Boolean.TRUE)` is false for `null` and for a deprecated `new Boolean(true)`. `if (Boolean.TRUE.equals(flag))` treats `null` as false and still loses to a non-interned instance unless you also use `equals`. Prefer a primitive `boolean`, or unbox after a null-check.

> [!warning] Do not construct a fourth boolean
> `new Boolean(true)` allocates a new object even though `TRUE` already exists. Prefer `Boolean.TRUE`, `valueOf`, or autoboxing. `parseBoolean` returns a primitive; only `valueOf(String)` boxes onto `TRUE`/`FALSE`.

> [!tip] Interview answer
> **`Boolean.TRUE` and `Boolean.FALSE` are the two interned wrapper constants for `true` and `false`.** `valueOf` and autoboxing return those same instances, so `Boolean.valueOf(true) == Boolean.TRUE`. `new Boolean(true)` is a different object and is deprecated; `null` is how a `Boolean` variable represents “unset,” not a third constant.
