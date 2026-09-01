<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #SRS

# What are the autoboxing rules when assigning a primitive to a wrapper?

> [!abstract] Short answer
> Assignment boxing is a **fixed conversion chain**, not “any primitive into any wrapper.” A primitive boxes to **its own** wrapper (`int`→`Integer`, `long`→`Long`, …). You may then **widen the reference** (`Integer`→`Number`). For a **constant** `byte`/`short`/`char`/`int` whose value fits, you may **narrow then box** into `Byte`, `Short`, or `Character` only. There is **no** “widen the primitive then box,” so `Long n = 1;` does not compile. Method arguments do **not** get that constant narrowing.

## What assignment conversion allows

The target is the wrapper variable. Allowed chains that involve boxing:

1. **Boxing** — `boolean`→`Boolean`, `byte`→`Byte`, `short`→`Short`, `char`→`Character`, `int`→`Integer`, `long`→`Long`, `float`→`Float`, `double`→`Double`.
2. **Boxing then widening reference** — `int`→`Integer`→`Number` / `Object`.
3. **Constant narrowing then boxing** — only if the right-hand side is a constant expression of type `byte`, `short`, `char`, or `int`, the target is `Byte`, `Short`, or `Character`, and the value is representable in `byte` / `short` / `char` respectively.

Anything else is a compile-time error. The compiler typically implements boxing as `valueOf` ([[What method does the compiler insert when autoboxing an int]], [[When does autoboxing occur in Java]]).

```d2
direction: down
match: "int x → Integer\nboxing only" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
wide: "int x → Number\nbox then widen reference" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
narrow: "42 → Byte\nconstant, value fits" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
bad: "1 → Long  /  byteVar → Integer\nno widen-then-box" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
```

**Fig. 1.** Matching box, box-then-`Number`, constant-to-`Byte`/`Short`/`Character`; no `int`→`Long`.

```java
Integer a = 5;              // boxing int → Integer
Number n = 5;               // boxing then widening reference
Byte b = 42;                // constant int, fits in byte → narrow + box
Character c = 65;           // constant, fits in char

// Long big = 1;            // does not compile: int ↛ Long
// Double d = 1;            // does not compile
Long big = 1L;              // boxing long → Long

byte v = 1;
// Short s = v;             // does not compile: byte variable ↛ Short
Short s = (short) v;        // primitive conversion, then boxing
```

**Listing 1.** Conceptual: legal assignment boxing versus the usual compile errors.

A **`final int`** initialized with a constant *is* a constant expression, so `final int x = 5; Byte b = x;` is legal. A non-`final` `int y = 5; Byte b = y;` is not: `int` boxes to `Integer`, and `Integer` is not a `Byte`.

## Assignment vs method invocation

Invocation conversion allows boxing, but **not** the extra constant narrowing that assignment allows. `void m(Byte b)` cannot be called as `m(42)` without a cast; `Byte b = 42;` is fine. That is why “it works with `=` so it should work as an argument” is false ([[How does adding an int to an ArrayList of Integer autobox]] is a *matching* `int`→`Integer` box, which both contexts allow).

Constant boxing of `true`/`false`, `'\u0000'`..`'\u007f'`, and integers **-128..127** must yield `==` identical references. That is the cache story in [[How can you extend the Integer autobox cache maximum]] — identity is a language rule only for those constants, not for every boxed `int`.

> [!warning] `Long x = 1;` is the classic compile error
> `1` has type `int`. Boxing would produce `Integer`, and `Integer` is not a subtype of `Long`. Assignment does not widen `int` to `long` *and then* box. Write `1L`, `(long) 1`, or `Long.valueOf(1L)`. The same hole forbids `Float f = 1;` and `Double d = 1;`.

> [!warning] `==` on boxed assignment is not value equality
> `Integer a = 127; Integer b = 127; a == b` is true for those constants. `Integer a = 128; Integer b = 128;` need not be. Prefer `equals` / `intValue()`. `new Integer(5)` (deprecated) is never required for assignment boxing.

> [!tip] Interview answer
> **You can assign a primitive to its own wrapper (`int`→`Integer`) and then to a supertype like `Number`.** Constants that fit may also narrow into `Byte`, `Short`, or `Character` on assignment only — not as method arguments. There is no widen-then-box, so `Long x = 1;` does not compile; use `1L`. Small integer constants in **-128..127** box to interned instances.
