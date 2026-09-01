<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #Java/Performance #SRS

# What happens when you use `Integer` as a loop accumulator in Java?

> [!abstract] Short answer
> `Integer sum = 0; sum += x;` is a **compound assignment**: unbox `sum`, add, **box** the result, store a new reference. In a loop that happens **every iteration**. Past the **-128..127** cache each box is a fresh object. A `null` accumulator throws `NullPointerException` on the first `+=`. Use a primitive `int` / `long` accumulator; box once at the end if you need a wrapper.

## `+=` is unbox, add, box — not an in-place add

`E1 += E2` means `E1 = (T) ((E1) + (E2))` with `T` the type of `E1`. For `T = Integer` the `+` unboxes, the assignment boxes ([[What happens when you increment an Integer with plus plus in Java]] is the same pipeline for `++`).

```d2
direction: down
loop: "each iteration" {
  width: 200
  height: 40
}
unbox: "unbox sum → int" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
add: "int + x" {
  width: 160
  height: 50
}
box: "valueOf(sum) → Integer" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
store: "sum = that reference" {
  width: 220
  height: 50
}
loop -> unbox -> add -> box -> store
```

**Fig. 1.** One trip of `Integer sum += x`: the wrapper is never mutated.

```java
int[] xs = { 1, 2, 3 /* … */ };

Integer sum = 0;                 // boxed 0 (cached)
for (int x : xs) {
    sum += x;                    // unbox, add, box, assign
}

int fast = 0;
for (int x : xs) {
    fast += x;                   // primitive add only
}
Integer boxedOnce = fast;        // box if an API wants Integer
```

**Listing 1.** Conceptual: wrapper accumulator versus primitive accumulator.

`for (Integer i = 0; i < n; i++)` pays twice per trip: unbox for `i < n`, then unbox/box for `i++`. The `Integer` object from last time is discarded ([[Are Java wrapper types immutable]]).

Values in **-128..127** reuse interned instances, so a tiny loop may allocate nothing visible. A running **sum** leaves that range immediately. Escape analysis can sometimes scalar-replace a wrapper that never leaves the method — that is why boxing is not *always* a measured problem ([[Is autoboxing always a performance problem in Java]]) — but it is not a reason to write `Integer` counters.

> [!warning] A field `Integer sum;` starts as `null`
> `sum += x` unboxes that `null` and throws `NullPointerException` before any add. Primitive `int sum` would have been `0`. Same crash if a map/list yields a missing `Integer` you then `+=` ([[What default values do wrapper-typed fields receive in Java]], [[Why prefer primitives over wrappers in hot loops in Java]]).

> [!tip] Interview answer
> **An `Integer` accumulator unboxes, adds, and boxes on every `+=` or `++` — it does not mutate the old object.** That creates garbage once you leave the small-integer cache, and `null` explodes. Sum with `int` or `long`, then box a single result if you must.
