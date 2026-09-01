<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# What is the difference between the `short` primitive and the `Short` wrapper?

> [!abstract] Short answer
> **`short` is the 16-bit signed primitive.** **`Short` is the immutable wrapper object** for that value: a heap reference, nullable, usable as `List<Short>`. Assignment boxing is `Short.valueOf`. A `short` field defaults to `0`; a `Short` field to `null`. Arithmetic promotes `short` to `int`. `Short` interned **-128..127**, not the full 16-bit range.

## Primitive bits vs wrapper object

| | `short` | `Short` |
| --- | --- | --- |
| Kind | 16-bit two’s-complement primitive | `java.lang.Short` (`Number`) |
| Range | **-32768..32767** | same payload, plus `null` |
| Field default | `0` | `null` |
| Generics | `List<short>` illegal | `List<Short>` |
| `==` | value | identity (cache **-128..127**) |

That is the same primitive/wrapper split as `int` / `Integer` ([[What is the difference between int and Integer in Java]], [[What are the wrapper types for Java primitives]], [[What default values do wrapper-typed fields receive in Java]]).

```d2
direction: down
prim: "short n = 10\n16-bit value" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
wrap: "Short n = 10\nheap object (valueOf)" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Same number; `short` is bits, `Short` is a reference.

```java
short primitive = 10;
Short boxed = primitive;             // Short.valueOf(primitive)
short back = boxed;                  // shortValue(); NPE if boxed is null

Short fromConst = 10;                // constant int, fits → narrow + box
short v = 10;
Short fromShort = v;                 // short → Short
// Short fromIntExpr = v + 1;        // int ↛ Short
// new Short(10);                    // compile error: int ↛ short in invocation

List<Short> list = new ArrayList<>();
list.add(primitive);                 // autobox
```

**Listing 1.** Conceptual: boxing, constant narrowing, no `Short(int)` constructor.

`Short.valueOf(short)` always caches **-128..127** and may cache more — not all 65536 values, unlike `Byte` ([[Which wrapper types besides Integer cache boxed values]]). `new Short((short) 10)` (deprecated) never hits that cache.

`short` + `short` is **`int`** (binary numeric promotion). `s = s + 1` needs a cast; `s += 1` narrows back. `Short` `++` unboxes, adds as `int`, narrows, boxes ([[What happens when you increment an Integer with plus plus in Java]]).

> [!warning] `new Short(10)` and `m(10)` for `m(Short)` fail for the same reason as `Character`
> `10` is `int`. Invocation will not narrow it to `short`/`Short`. Assignment `Short x = 10` can. Cast `(short) 10` or use a `short` variable ([[What are the autoboxing rules when assigning a primitive to a wrapper]], [[Why does Character reject an int constructor argument]]).

> [!tip] Interview answer
> **`short` is a 16-bit primitive; `Short` is the object that wraps it.** Use `short` for compact values and math (know that `+` promotes to `int`). Use `Short` for collections and `null`. Boxing uses `valueOf`, which interned only **-128..127**, not the whole `short` range.
