<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #Java/Performance #SRS

# Why prefer primitives over wrappers in hot loops in Java?

> [!abstract] Short answer
> A primitive `int`/`long` accumulator is **arithmetic on bits**. An `Integer` accumulator **unboxes, adds, and boxes on every `+=` / `++`**, allocating once you leave the **-128..127** cache and stressing GC. Wrappers also cannot be used as a `null`-safe number: a `null` `Integer` in the loop is `NullPointerException`. Use primitives in the loop; box **once** if an API needs `Integer`.

## The loop pays object tax

`Integer sum += x` is `sum = Integer.valueOf(sum.intValue() + x)` — not an in-place add ([[What happens when you use Integer as a loop accumulator in Java]], [[What happens when you increment an Integer with plus plus in Java]]). Each boxed result is a heap object (commonly much larger than 4-byte `int`) unless the cache or escape analysis eats it ([[How much memory does an Integer object use compared with int]], [[Is autoboxing always a performance problem in Java]]).

```d2
direction: down
wrap: "Integer sum += x\nunbox + add + box" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
prim: "int sum += x\nadd only" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Same addition; only the wrapper path allocates.

```java
int[] xs = /* many values */;

Integer boxed = 0;
for (int x : xs) {
    boxed += x;                  // valueOf every trip after 127
}

int sum = 0;
for (int x : xs) {
    sum += x;                    // primitive
}
Integer once = sum;              // box if List / API needs it
```

**Listing 1.** Conceptual: keep the hot accumulator primitive.

Prefer wrappers **outside** the loop when the type system demands an object: `List<Integer>`, a nullable field, a generic API ([[Why cannot Java collections store primitive types]], [[Why are wrapper classes needed in Java]]). That is not a reason to type the **counter** as `Integer`.

Escape analysis can sometimes scalar-replace a wrapper that never escapes. That is a JIT maybe, not a style rule. Write `int`.

> [!warning] `null` is not “slower” — it throws
> `Integer acc = null; acc += x` unboxes `null` and throws `NullPointerException` on the first iteration. A primitive field would have been `0`. Do not describe that as a performance trade-off.

> [!tip] Interview answer
> **In a hot loop, use `int` or `long` because wrapping every add allocates and can throw on `null`.** Autoboxing is for collection boundaries, not for inner-loop math. Sum in a primitive, then box a single result if you must.
