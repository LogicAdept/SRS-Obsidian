<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #Java/String #SRS

# What is the difference between `Integer.parseInt` and `Integer.valueOf`?

> [!abstract] Short answer
> **`parseInt` returns `int`. `valueOf` returns `Integer`.** On a `String`, `valueOf` is parse-then-box: `Integer.valueOf(Integer.parseInt(s))`. Both throw `NumberFormatException` on bad text (including `null`). Radix overloads exist for both (`parseInt("111", 2)` and `valueOf("111", 2)` → `7` — [[How do you parse an int from a binary String in Java]]). Need a primitive? `parseInt`. Need a wrapper (or the cache)? `valueOf`.

## Primitive parse vs boxed factory

`parseInt(String)` / `parseInt(String, int radix)` interpret signed text and return a **primitive**. `valueOf(String)` / `valueOf(String, int radix)` use that same parse, then `valueOf(int)` to produce an **`Integer`**. Autoboxing an `int` also calls `valueOf(int)` ([[What method does the compiler insert when autoboxing an int]], [[What are the different ways of creating a Java wrapper instance]]).

```d2
direction: down
text: "String \"42\"" {
  width: 160
  height: 40
}
parse: "parseInt → int 42" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
box: "valueOf(int) → Integer" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
text -> parse
parse -> box
```

**Fig. 1.** `valueOf(String)` is `parseInt` plus boxing; `parseInt` stops at the primitive.

```java
int n = Integer.parseInt("42");           // primitive
Integer w = Integer.valueOf("42");        // wrapper; cache hit for 42
Integer same = Integer.valueOf(n);        // boxing factory, no parsing

int bin = Integer.parseInt("111", 2);     // 7
Integer binW = Integer.valueOf("111", 2); // Integer 7

// Integer.parseInt(null);                // NumberFormatException, not NPE
// Integer.parseInt(" 42 ");              // NumberFormatException (spaces)
```

**Listing 1.** Conceptual: return types, radix, and the usual parse failures.

Because `valueOf(int)` reuses **-128..127** (and a possibly raised high end), `valueOf("127") == valueOf("127")` can be true by identity. `parseInt` never allocates. Past the cache, `valueOf` allocates a new `Integer` ([[How can you extend the Integer autobox cache maximum]]).

The same split exists on the other numeric wrappers (`Long.parseLong` / `Long.valueOf`, `Double.parseDouble` / `Double.valueOf`, …). `Boolean` has `parseBoolean` (primitive) and `valueOf` (wrapper) with its own `"true"` rule — not `NumberFormatException`.

`String.valueOf(42)` is the **other direction** (value → text). It is not a parse, and it is not `Integer.valueOf`.

> [!warning] `parseInt` does not return `Integer`
> Writing `Integer x = Integer.parseInt("42");` compiles only because of autoboxing — you parsed to `int` and boxed again. If you wanted a wrapper, call `valueOf`. If you wanted a primitive, keep `parseInt` and do not assign it to `Integer` in a hot loop.

> [!tip] Interview answer
> **`parseInt` gives you an `int`; `valueOf` gives you an `Integer`.** The string overloads of `valueOf` parse with `parseInt` and then box, so they share `NumberFormatException` and radix rules, and they can hit the integer cache. Use `parseInt` unless you actually need the object.
