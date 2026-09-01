<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #SRS

# How do you convert a wrapper to a primitive with `xxxValue` methods?

> [!abstract] Short answer
> Call the matching instance method on the wrapper: `intValue()`, `longValue()`, `floatValue()`, `doubleValue()`, `byteValue()`, `shortValue()`, `charValue()`, or `booleanValue()`. Unboxing is the same conversion done implicitly — an `Integer` used where `int` is required becomes `r.intValue()`. Numeric wrappers inherit the six numeric methods from `Number`; `Boolean` and `Character` are not `Number` subtypes and expose only `booleanValue()` / `charValue()`.

## Matching `xxxValue` is explicit unboxing

Unboxing conversion is defined as invoking that method on the reference:

| Wrapper | Method inserted for unboxing |
| --- | --- |
| `Boolean` | `booleanValue()` |
| `Byte` | `byteValue()` |
| `Short` | `shortValue()` |
| `Character` | `charValue()` |
| `Integer` | `intValue()` |
| `Long` | `longValue()` |
| `Float` | `floatValue()` |
| `Double` | `doubleValue()` |

If the reference is `null`, that conversion throws `NullPointerException` — the same exception you get from calling `xxxValue()` on a null variable. See [[What is unboxing]] and [[What method does the compiler insert when unboxing an Integer]].

```d2
direction: down
wrap: "Integer seven = valueOf(57)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
explicit: "seven.intValue()" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
implicit: "int y = seven\nunboxing" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
prim: "primitive int 57" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}

wrap -> explicit
wrap -> implicit
explicit -> prim
implicit -> prim: "also intValue()"
```

**Fig. 1.** Explicit `intValue()` and unboxing extract the same primitive; they are not a second, different conversion.

```java
Integer seven = Integer.valueOf(57);
int primitive = seven.intValue();     // explicit
int also = seven;                     // unboxing → seven.intValue()

Boolean flag = Boolean.TRUE;
boolean b = flag.booleanValue();

Character ch = Character.valueOf('A');
char c = ch.charValue();
```

**Listing 1.** Conceptual: matching `xxxValue` versus assignment unboxing.

## Cross-type `xxxValue` is a primitive conversion

`Byte`, `Short`, `Integer`, `Long`, `Float`, and `Double` extend `Number`, which declares abstract `intValue`, `longValue`, `floatValue`, and `doubleValue`, plus default `byteValue` / `shortValue` that cast from `intValue()`. Those extra methods are **not** unboxing. Unboxing an `Integer` always uses `intValue()`; `seven.floatValue()` is an explicit widening of the wrapped `int` to `float`.

`Number` documents that platform conversions follow widening or narrowing primitive conversion: they may drop magnitude, precision, or even sign. `Integer.floatValue()` is a widening (`(float)value`). `Float.intValue()` is a narrowing (round toward zero, then saturate to `int` range) — not IEEE bit reinterpretation (`floatToIntBits`).

```java
Integer seven = Integer.valueOf(57);
float asFloat = seven.floatValue();           // 57.0f, widening

Float wrapper = Float.valueOf(57.9f);
int truncated = wrapper.intValue();           // 57, narrowing — not the IEEE bits
int bits = Float.floatToIntBits(wrapper);     // bit pattern, unrelated to 57
```

**Listing 2.** Conceptual: `floatValue()` / `intValue()` convert the numeric value; `floatToIntBits` is a different API.

`Integer.byteValue()` / `shortValue()` narrow by discarding high bits (`(byte)value`), which can change sign for values outside the smaller type.

> [!warning] Null wrapper → `NullPointerException`
> `Integer x = null; x.intValue();` and `int y = x;` both throw `NullPointerException`. Unboxing does not produce a default `0`. Map lookups that return a wrapper are a common source — see [[How do you avoid NullPointerException when unboxing a Map value]].

> [!warning] Unboxing uses only the matching method
> `int n = someFloat;` unboxes with `floatValue()` then narrows `float` → `int`. It does **not** call `intValue()` on the `Float`. Conversely, `someInteger.floatValue()` is a method call you wrote, not unboxing. `Boolean` and `Character` have no `intValue()`; they are not `Number` subclasses.

> [!tip] Interview answer
> **Use `intValue()`, `booleanValue()`, `charValue()`, and the other `xxxValue` instance methods to pull the primitive out of a wrapper.** Unboxing is that same call inserted by the language (`Integer` → `intValue()`). Numeric wrappers also inherit extra `Number` conversions that can widen or narrow and lose precision; a null wrapper throws `NullPointerException` either way.
