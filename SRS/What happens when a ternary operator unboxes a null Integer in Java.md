<!--
reps: 0
priority: 0
-->
#Java/Language/Operators/Ternary #Java/Language/Wrappers/Autoboxing #SRS

# What happens when a ternary operator unboxes a `null` `Integer` in Java?

> [!abstract] Short answer
> Mixing `int` and `Integer` in `? :` makes a **numeric** conditional whose type is **`int`**. The chosen branch is converted to that type — which **unboxes** an `Integer`. If that `Integer` is `null`, you get `NullPointerException`. The other branch is **not** evaluated, so `true ? 0 : nullInteger` is safe; `false ? 0 : nullInteger` is not. Assigning the expression to `Object` does **not** change its type.

## The expression type is chosen from both arms

`? :` is classified from the **second and third** operands. `int` is numeric; `Integer` is convertible to a numeric type, so `0` and an `Integer` variable together are a **numeric conditional**. When one arm is primitive `T` and the other is `T`’s wrapper, the expression type is **`T`** — here `int`.

Only then does the condition pick an arm. That arm is evaluated and converted to `int`. Conversion of `Integer` is unboxing (`intValue()`). Unboxing `null` throws ([[What is unboxing]], [[What method does the compiler insert when unboxing an Integer]]).

```d2
direction: down
mix: "int  0  and  Integer x\nnumeric ?:  type int" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
trueArm: "true → evaluate 0\nno unbox of x" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
falseArm: "false → evaluate x\nunbox null → NPE" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
mix -> trueArm
mix -> falseArm
```

**Fig. 1.** Type is `int` either way; NPE happens only if the `Integer` arm is the one actually evaluated.

```java
Integer x = null;

Object o = true ? 0 : x;    // type int; takes 0; x unused; then box for Object
// int alsoOk = true ? 0 : x;  // also fine: still does not evaluate x

int bad = false ? 0 : x;    // type int; evaluates x; unbox null → NPE
// Integer stillBad = false ? 0 : x;  // same NPE: type is still int
// Object stillBad2 = false ? 0 : x;  // same NPE: Object does not retarget the type
```

**Listing 1.** Conceptual: `int`+`Integer` is a standalone `int` expression; the target variable does not stop unboxing.

Numeric conditionals are **standalone**: they do not take the assignment target as a poly target type. `Object o = false ? 0 : x` still has type `int`.

## When `null` does not explode

Both arms `Integer` → same type `Integer` → **no** unboxing of the result. `false ? x : y` can yield `null`.

The **`null` literal** is not a numeric expression. `false ? 0 : null` is a **reference** conditional (lub of `Integer` and `null` → `Integer`). The result can be `null` with no NPE. That is a different classification from a **variable** of type `Integer` that happens to hold `null`.

`boolean` + `Boolean` is the same trap: the expression type is `boolean`, and a `null` `Boolean` arm unboxes to NPE ([[Why are Integer and Boolean wrapper types dangerous in Java]]).

> [!warning] The unused arm is not “also unboxed”
> Compile-time typing looks at **both** arms; run time evaluates **one**. Dumps that write `Object o = true ? 0 : x` as “fine” are right only because `x` is skipped — not because `Object` prevented unboxing. Flip the condition and the same line throws.

> [!tip] Interview answer
> **If one branch is `int` and the other is `Integer`, the ternary’s type is `int`, so the wrapper branch is unboxed.** A `null` `Integer` on the chosen branch is `NullPointerException`. The other branch is not evaluated. Putting the expression in an `Object` or `Integer` variable does not change that; `? 0 : null` with the `null` *literal* is a different, reference-typed case.
