<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #SRS

# What is unboxing?

> [!abstract] Short answer
> **Unboxing** is conversion of a **wrapper** to its **primitive**: `Integer` → `int`, `Boolean` → `boolean`, and so on. The compiler inserts the matching `xxxValue()` call (`int x = i` → `i.intValue()`). If the wrapper is **`null`**, that call throws **`NullPointerException`**. Boxing is the opposite direction (`valueOf`).

## Wrapper back to bits

Unboxing conversion is defined for the eight wrappers. For an `Integer` reference `r` it *is* `r.intValue()`. The same for `booleanValue`, `byteValue`, `shortValue`, `charValue`, `longValue`, `floatValue`, `doubleValue` ([[What method does the compiler insert when unboxing an Integer]], [[What are autoboxing and unboxing in Java]]).

The compiler inserts it when a wrapper is used as a primitive: assignment, arithmetic, `++` / `+=`, comparisons, numeric `? :`, a method that takes `int` ([[When does autoboxing occur in Java]]).

```d2
direction: down
w: "Integer i" {
  width: 140
  height: 40
}
u: "i.intValue()" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
ok: "int" {
  width: 80
  height: 40
  style.fill: "#e8f5e9"
}
npe: "i == null → NPE" {
  width: 180
  height: 50
  style.fill: "#ffebee"
}
w -> u -> ok
u -> npe
```

**Fig. 1.** Unboxing is a real virtual call; `null` fails there.

```java
Integer i = 5;          // boxing (valueOf)
int j = i;              // unboxing (intValue)

Integer missing = null;
// int boom = missing;  // NullPointerException
```

**Listing 1.** Conceptual: the happy path and the trap ([[Why cannot a Java primitive variable be null]]).

`Number`’s extra conversions (`doubleValue()` on an `Integer`) are not unboxing. Unboxing always matches the wrapper’s own primitive.

A field `Integer n;` starts as `null`, so `int x = n;` throws. Locals have no default and will not compile uninitialized.

> [!warning] The trap is `null`, not “failed assignment”
> `Integer i = null; int j = i;` looks like copying a number. It is `intValue()` on `null`. Same crash from `map.get(missingKey)` assigned to `int`, or a ternary that unboxes a null arm ([[What happens when a ternary operator unboxes a null Integer in Java]]).

> [!tip] Interview answer
> **Unboxing converts a wrapper to a primitive by calling `xxxValue()` — `int j = i` is `i.intValue()`.** Boxing wraps with `valueOf`. If `i` is `null`, unboxing is `NullPointerException`, not `0`. That is the usual interview trap.
