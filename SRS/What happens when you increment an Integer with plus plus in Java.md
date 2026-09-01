<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #SRS

# What happens when you increment an `Integer` with plus plus in Java?

> [!abstract] Short answer
> `ten++` on an `Integer` variable is **legal**. Java **unboxes** to `int`, adds one, then **boxes** the sum and **stores a new reference** in the variable. The original `Integer` object is **not** mutated — wrappers are immutable. `++` on `null` throws `NullPointerException`. Prefer `int` for a counter; boxing on every increment is extra work.

## Unbox, add, box, assign

The operand of `++` / `--` must be a **variable** whose type is convertible to a numeric type. `Integer` qualifies via unboxing. The expression’s type is still `Integer` (the variable’s type). Run time:

1. Read the variable and **unbox** (`intValue()`).
2. Add `1` (binary numeric promotion with the literal `1`).
3. **Box** the sum (`valueOf`) and write that reference back.

Prefix `++ten` is the same store; it yields the **new** boxed value. Postfix `ten++` yields the **old** boxed value, then stores.

```d2
direction: down
var: "Integer ten → object 10" {
  width: 240
  height: 50
}
unbox: "unbox → int 10" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
add: "10 + 1 → 11" {
  width: 180
  height: 50
}
box: "valueOf(11) → new/cached Integer" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
old: "object 10 unchanged" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
var -> unbox -> add -> box
var -> old
```

**Fig. 1.** `++` rebinds the variable; the previous `Integer` instance stays `10`.

```java
Integer ten = Integer.valueOf(10);
Integer same = ten;
ten++;                       // unbox 10, add, box 11, store
// ten.intValue() == 11
// same.intValue() == 10     // distinct object; wrappers are immutable

Integer n = null;
// n++;                      // NullPointerException on unbox
```

**Listing 1.** Conceptual: increment replaces the reference; `same` still points at `10` ([[Are Java wrapper types immutable]], [[Can wrapping a primitive let a Java method change the caller value]]).

`new Integer(10)` (deprecated) is never interned. After `ten++`, `ten` may be a cache hit (`11` is in **-128..127**) while `same` is still the unique `new` object. Do not use `==` to reason about “the incremented value.”

A method `void bump(Integer n) { n++; }` increments only the **local** copy of the reference. The caller’s variable is unchanged — same pass-by-value story as mutating a reassigned local.

`final Integer ten = 10; ten++;` does not compile: `++` needs a variable, and a `final` access is a value.

> [!warning] A loop `Integer` counter boxes every trip
> `for (Integer i = 0; i < n; i++)` unboxes and boxes on each `i++`. That is the accumulator trap in [[What happens when you use Integer as a loop accumulator in Java]] and [[Is autoboxing always a performance problem in Java]]. Use `int`, or `AtomicInteger` when the point is shared mutation ([[Why is the Java increment operator not atomic]]).

> [!tip] Interview answer
> **`Integer x; x++` unboxes, adds one, and boxes the result back into `x`.** The old object is untouched because wrappers are immutable. `null++` is a `NullPointerException`. It looks like a field mutation; it is a reassignment — so a method that does `n++` on its parameter does not change the caller’s wrapper.
