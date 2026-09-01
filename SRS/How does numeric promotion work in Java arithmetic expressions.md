<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/NumericPromotion #SRS

# How does numeric promotion work in Java arithmetic expressions?

> [!abstract] Short answer
> Arithmetic operators pick one **promoted type** for both operands, then compute in that type. After unboxing, the ladder is `double`, else `float`, else `long`, else **`int`**. `byte`, `short`, and `char` therefore become `int` in `+`, `-`, `*`, `/`, `%`, and bitwise `&`/`|`/`^`. A `long`/`float`/`double` operand lifts the whole operation; it does not “average” toward the smaller type.

## One promoted type, then the operator runs

Numeric operands of `*`, `/`, `%`, numeric `+`/`-`, comparisons, and integer bitwise operators undergo **binary** numeric promotion: unbox if needed, then widen every operand to the promoted type. Unary `+`, `-`, and `~` promote a single operand the same way (still to `int` unless it is already `long`/`float`/`double`). The expression’s type is that promoted type. [[Why does adding two byte values not compile as a byte in Java]] is the assignment consequence: `a + b` on two `byte` variables is `int`.

```d2
direction: down
ops: "Arithmetic operands\nafter unboxing" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
d: "any double → double" {
  width: 240
  height: 55
  style.fill: "#ffebee"
}
f: "else any float → float" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
l: "else any long → long" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
i: "else int\nbyte/short/char widen" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}

ops -> d
d -> f: "none"
f -> l: "none"
l -> i: "none"
```

**Fig. 1.** Arithmetic (and array-index) promotion. A numeric `? :` is a **choice** context and can stay `byte`/`short`/`char` when every arm fits; `+` never does.

Shifts are the exception inside arithmetic syntax: each side gets **unary** promotion separately. A `long` shift distance does **not** promote the left operand to `long`. The result type is the promoted left type (`int` or `long`).

```java
public final class NumericPromotion {
    public static void main(String[] args) {
        byte a = 10, b = 20;
        // byte sum = a + b;          // does not compile: a + b is int
        byte sum = (byte) (a + b);
        byte literal = 10 + 20;       // OK: constant 30 fits in byte

        int i = 5;
        double truncated = i / 2;     // 2.0 — int / int, then widen
        double fractional = i / 2.0;  // 2.5 — promoted to double first

        byte s = 1;
        s += 1;                       // compiles: hidden (byte) cast
        int shifted = s << 4L;        // left → int; 4L does not make long

        System.out.println(sum);
        System.out.println(literal);
        System.out.println(truncated);
        System.out.println(fractional);
        System.out.println(s);
        System.out.println(shifted);
    }
}
```

**Listing 1.** Variable `byte + byte` is `int`. A constant `int` that fits may still assign to `byte`. Integer `/` runs before widening to `double`. `+=` inserts a narrowing cast; `<<` does not binary-promote.

Integer `/` and `%` round **toward zero** after that promotion (`5 / 2` is `2`). If both operands stay `int`, the quotient is `int` even when the destination is `double`. Write `2.0` (or cast an operand) so promotion happens **before** the divide. [[Why does integer division of 5 by 2 equal 2 in Java]] is that rule; [[Why does multiplying two int values overflow before assignment to a long]] is the same “compute in the promoted type, assign later” story for `*`.

`E1 op= E2` is `E1 = (T) ((E1) op (E2))` with `T` the type of `E1`, so `byte b = 1; b += 1;` compiles even though `b + 1` is `int`. That hidden cast is not a way to keep the **operator** itself in `byte`.

> [!warning] Promotion is not “use the larger variable”
> `double x = i / 2` does not divide in `double`. Both operands are `int`, so you get truncated `2` and then a widening assignment. `byte + byte` is `int`, not `byte`; `byte + long` is `long`, not “something in between.” `b << 4L` is still an `int` shift of a promoted `byte`. Do not confuse this with `byte b = 10 + 20`, which is allowed only because `10 + 20` is a constant `int` whose value fits — [[How would you explain widening and narrowing casts between Java primitive types]] is that assignment narrowing, not a `byte` add.

> [!tip] Interview answer
> **In arithmetic, Java promotes to `double`, else `float`, else `long`, else `int` — so `byte`/`short`/`char` math is `int` math.** A `float` or `double` operand lifts `/` and `+` before the operation; an `int` quotient is not re-divided just because you assign it to `double`. Shifts promote each side alone, and `+=` on a `byte` compiles only because of a hidden cast back.
