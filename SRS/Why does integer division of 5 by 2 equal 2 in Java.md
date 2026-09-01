<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# Why does integer division of 5 by 2 equal 2 in Java?

> [!abstract] Short answer
> Both operands are `int`, so `/` is **integer** division. The quotient is truncated **toward zero**: the largest integer *q* with |2 · *q*| ≤ 5, same sign as the dividend — that is **2**, not 2.5. The destination variable does not change the operator. `double e = 5 / 2;` is **2.0**. Use `5 / 2.0`, `5.0 / 2`, or `(double) 5 / 2` for 2.5.

## `/` follows the operands, not the assignment

Binary numeric promotion runs first. Two `int`s stay `int`; `byte`/`short`/`char` widen to `int` and still divide as integers. One `double` (or `float`) operand makes the whole `/` floating-point. Assigning that `int` 2 to a `double` only widens **after** the fraction is already gone. `(double)(i / 2)` is the same trap: the cast wraps the **already truncated** quotient. [[How does numeric promotion work in Java arithmetic expressions]] is that ladder; [[Why does multiplying two int values overflow before assignment to a long]] is the sibling “operation type ignores the destination”; [[What is the default type of a Java floating-point literal]] is why `2.0` is already `double`.

```d2
direction: down
expr: "5 / 2" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
int: "int / int\ntoward zero → 2" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
fp: "5 / 2.0\nIEEE quotient → 2.5" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

expr -> int
expr -> fp
```

**Fig. 1.** Integer `/` drops the fraction before any later widening.

Toward zero is not floor: `(-5) / 2` is **-2**, not −3. `Math.floorDiv(-5, 2)` is the floor (`-3`). Remainder matches the truncated quotient: `(a / b) * b + (a % b)` equals `a`, so `5 % 2` is `1`. Integer `/` or `%` by **zero** throws `ArithmeticException`; floating-point `/` by `0.0` does not. `Integer.MIN_VALUE / -1` overflows to `MIN_VALUE` with no exception. [[What happens on integer overflow in Java]] is that wrap; [[Does floating-point division by zero throw ArithmeticException]] is the IEEE contrast; [[Why does adding two byte values not compile as a byte in Java]] is promotion the other direction.

```java
public final class IntDivisionTruncates {
    public static void main(String[] args) {
        int i = 5;
        System.out.println(i / 2);             // 2
        double lost = i / 2;                   // 2.0 — int / first
        double ok = i / 2.0;                   // 2.5
        double also = (double) i / 2;          // 2.5 — cast before /
        double tooLate = (double) (i / 2);     // 2.0

        System.out.println((-5) / 2);          // -2  (toward zero)
        System.out.println(Math.floorDiv(-5, 2)); // -3
        System.out.println(5 % 2);             // 1

        System.out.println(lost);
        System.out.println(ok);
        System.out.println(also);
        System.out.println(tooLate);
    }
}
```

**Listing 1.** `5 / 2` is `2`. A `double` operand (or a cast of an operand) must be in place **before** `/` if you want 2.5.

> [!warning] `double e = i / 2` looks like real division and is not
> The `double` on the left is a widening of `2`, not a request for a fractional `/`. `float f = 5 / 2;` is `2.0f` for the same reason. Do not “fix” it with `e = (double)(i / 2)`.

> [!tip] Interview answer
> `5 / 2` is `2` because both operands are `int` and integer division truncates toward zero. Storing the result in a `double` does not bring the `.5` back. Put a floating-point operand on the `/` before it runs, and remember `(-5) / 2` is `-2`, not floor.
