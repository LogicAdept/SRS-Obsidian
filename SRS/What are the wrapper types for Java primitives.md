<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# What are the wrapper types for Java primitives?

> [!abstract] Short answer
> There are **eight** language wrappers, one per primitive: **`Boolean`**, **`Byte`**, **`Short`**, **`Character`**, **`Integer`**, **`Long`**, **`Float`**, **`Double`**. Boxing conversion is that closed list. The six numeric wrappers extend `Number`; `Boolean` and `Character` do not. `Void` is not a primitive wrapper and does not autobox.

## One wrapper per primitive

| Primitive | Wrapper | Superclass |
| --- | --- | --- |
| `boolean` | `Boolean` | `Object` |
| `byte` | `Byte` | `Number` |
| `short` | `Short` | `Number` |
| `char` | `Character` | `Object` |
| `int` | `Integer` | `Number` |
| `long` | `Long` | `Number` |
| `float` | `Float` | `Number` |
| `double` | `Double` | `Number` |

They live in `java.lang`. Autoboxing/`valueOf` and unboxing/`xxxValue` pair each row ([[What are autoboxing and unboxing in Java]], [[What is the difference between int and Integer in Java]]). That is why `List<Integer>` works and `List<int>` does not ([[Why are wrapper classes needed in Java]]).

```d2
direction: down
prim: "8 primitives" {
  width: 160
  height: 40
}
wrap: "8 java.lang wrappers" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
num: "Byte Short Integer\nLong Float Double\nextend Number" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
other: "Boolean Character" {
  width: 200
  height: 50
}
prim -> wrap
wrap -> num
wrap -> other
```

**Fig. 1.** Closed set of eight; only the numeric six are `Number`.

```java
Boolean  bo = true;
Byte     b  = (byte) 1;
Short    s  = (short) 1;
Character c = 'A';
Integer  i  = 1;
Long     l  = 1L;
Float    f  = 1.0f;
Double   d  = 1.0;

Number n = i;                    // Integer is a Number
// Number n2 = bo;               // Boolean is not
```

**Listing 1.** Conceptual: each primitive boxes to exactly one class.

All eight are `final`, immutable, and value-based. Several intern small values (`Boolean` both; `Byte` all; `Character` ASCII; `Short`/`Integer`/`Long` **-128..127**) ([[Which wrapper types besides Integer cache boxed values]]). Constructors are deprecated; use `valueOf` / autoboxing.

`Void` wraps the keyword `void` as `Class<Void>` (`Void.TYPE`). It is not in the boxing table: there is no `void` value to box.

> [!warning] `Character` and `Integer` are not named `Char` and `Int`
> Interview spelling traps. `char` → `Character`, `int` → `Integer`. There is no `Char` wrapper in `java.lang`.

> [!tip] Interview answer
> **Eight wrappers: `Boolean`, `Byte`, `Short`, `Character`, `Integer`, `Long`, `Float`, `Double`.** Autoboxing only goes to those types. The numeric six extend `Number`; `Boolean` and `Character` do not. `Void` is something else.
