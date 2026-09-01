<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #Java/Performance #SRS

# Why are `Integer` and `Boolean` wrapper types dangerous in Java?

> [!abstract] Short answer
> They are **nullable objects**, not bits. Unboxing `null` (`int x = i`, `if (flag)`) throws **`NullPointerException`**. `==` is **identity**: interned `Integer`s in **-128..127** and `Boolean.TRUE`/`FALSE` can look equal, then fail outside the cache. They **allocate** (an `Integer` is much larger than 4-byte `int`) and a loop `+=` boxes every trip. Use primitives for arithmetic and flags; wrappers for collections and true absence.

## Null, identity, and allocation

A wrapper field defaults to `null`, not `0`/`false` ([[What default values do wrapper-typed fields receive in Java]]). Any unbox is `xxxValue()` ([[What is unboxing]]). That is the first interview crash: `Integer i = null; int x = i;` and `Boolean flag = null; if (flag) { … }`.

```d2
direction: down
npe: "null Integer / Boolean\nunbox → NPE" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
id: "== is identity\ncache / TRUE-FALSE lie" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
heap: "object per box\nloops allocate" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Three ways wrappers bite: `null`, `==`, heap.

```java
Integer i = null;
// int x = i;                    // NPE

Boolean flag = null;
// if (flag) { }                 // NPE — unbox in the condition

Integer a = 127, b = 127;
boolean cacheHit = (a == b);     // true
Integer c = 128, d = 128;
boolean cacheMiss = (c == d);    // typically false

Boolean t1 = true, t2 = true;
boolean bothTrue = (t1 == t2);   // true — TRUE interned; still do not use == for value
```

**Listing 1.** Conceptual: unbox NPE and `==` that depends on interning ([[How would you explain Integer cache valueOf(100)==valueOf(100) true, valueOf(200) false]], [[What are Boolean.TRUE and Boolean.FALSE]], [[How do you compare primitive and wrapper values in Java]]).

`Integer` in a hot `sum += x` boxes every iteration ([[Why prefer primitives over wrappers in hot loops in Java]]). The object is a heap header plus the `int` payload, not 4 bytes ([[How much memory does an Integer object use compared with int]]). `Boolean` does not have a range cache to “go wrong” at 128, but `null` in `if` is enough, and `new Boolean(true)` (deprecated) is a **third** instance besides `TRUE`/`FALSE`.

Wrappers are value-based: do not `synchronized (someInteger)` — especially not on `Boolean.TRUE`, which is shared VM-wide.

They remain the right type for `List<Integer>`, nullable bean properties, and “unknown flag.” The danger is using them **as if they were** `int`/`boolean`.

> [!warning] `if (boxedBoolean)` is not a safe boolean test
> It unboxes. `null` throws; it does not mean `false`. Write `Boolean.TRUE.equals(flag)` (false for `null`) or keep a primitive `boolean` when the value is always present.

> [!tip] Interview answer
> **`Integer` and `Boolean` are dangerous because they can be `null`, because `==` tests identity (the cache and `TRUE`/`FALSE` hide that), and because boxing allocates.** Unboxing `null` is NPE, not `0`/`false`. Compute with primitives; use wrappers when you need an object or a real empty value.
