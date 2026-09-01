<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# What happens on integer overflow in Java?

> [!abstract] Short answer
> Ordinary `int` and `long` arithmetic **wraps** in two’s complement. The result is the **low-order bits** of the mathematical sum or product — no flag, no `ArithmeticException`. `Integer.MAX_VALUE + 1` is `Integer.MIN_VALUE`; `Integer.MIN_VALUE - 1` is `Integer.MAX_VALUE`. The only integer operators that throw for a bad value are `/` and `%` when the divisor is **zero**.

## Wrap in the promoted type, then assign

`+`, `-`, `*`, `++`, and `--` on integers do not report overflow or underflow. After numeric promotion the work is 32-bit (`int`) unless an operand is already `long`. If the mathematical result does not fit, Java keeps the low-order bits; the sign can flip. That is why `1_000_000 * 1_000_000` is `-727379968` even when you store it in a `long`: both operands are `int`, so the wrap happens **before** assignment. Write `1_000_000L * 1_000_000` so promotion is `long` first. [[Why does multiplying two int values overflow before assignment to a long]] is that bug; [[How does numeric promotion work in Java arithmetic expressions]] is why the type of `*` ignores the destination variable.

```d2
direction: down
expr: "int / long + - * ++ --" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
wrap: "low-order two's-complement bits\nsilent wrap, sign may flip" {
  width: 320
  height: 80
  style.fill: "#ffebee"
}
exact: "Math.addExact / multiplyExact / subtractExact" {
  width: 340
  height: 60
  style.fill: "#e8f5e9"
}
ae: "ArithmeticException" {
  width: 220
  height: 50
  style.fill: "#c8e6c9"
}

expr -> wrap
exact -> ae: "overflow"
```

**Fig. 1.** Language operators wrap. Java 8 `Math.*Exact` is the opt-in that throws. Integer `/` by zero throws too — that is not overflow.

Two more silent cases people treat as errors: `-Integer.MIN_VALUE` is still `Integer.MIN_VALUE` (the two’s-complement range is not symmetric), and `Integer.MIN_VALUE / -1` is the same value with **no** exception. Contrast floating-point: overflow there becomes an infinity, and `/ 0.0` is infinity or NaN, not `ArithmeticException`. [[Does floating-point division by zero throw ArithmeticException]] is that split; [[What is the value range of the Java int type]] is why `MAX_VALUE` is 2³¹−1.

To detect overflow, call `Math.addExact`, `subtractExact`, or `multiplyExact` (Java 8). They return the same result when it fits and throw `ArithmeticException` when it does not. `Math.divideExact` (Java 18) is the checked form of `MIN_VALUE / -1`. `toIntExact(long)` throws if the `long` does not fit in `int`.

```java
public final class IntegerOverflow {
    public static void main(String[] args) {
        int max = Integer.MAX_VALUE; // 2_147_483_647
        System.out.println(max + 1); // -2147483648

        int min = Integer.MIN_VALUE; // -2_147_483_648
        System.out.println(min - 1); // 2147483647
        System.out.println(-min);    // still MIN_VALUE
        System.out.println(min / -1); // still MIN_VALUE, no throw

        long tooLate = 1_000_000 * 1_000_000;  // -727379968
        long inTime = 1_000_000L * 1_000_000;  // 1_000_000_000_000
        System.out.println(tooLate);
        System.out.println(inTime);

        try {
            Math.addExact(max, 1);
        } catch (ArithmeticException e) {
            System.out.println("addExact throws");
        }
        // int z = 1 / 0;  // ArithmeticException: divide by zero, not overflow
    }
}
```

**Listing 1.** `+`/`-` wrap through the `int` endpoints. `int * int` wraps before a `long` store. `addExact` is the throwing alternative. `/ 0` is a different exception.

> [!warning] Overflow is not `/ 0`, and a `long` variable does not widen the `*`
> Dumps mix “Java throws on overflow” with C# `checked` or with divide-by-zero. `int`/`long` `+` `-` `*` wrap. `1/0` throws; `MAX_VALUE + 1` does not. `long product = a * b` is still an `int` multiply if `a` and `b` are `int`. `float` overflow is `Infinity`, not wrap.

> [!tip] Interview answer
> Integer overflow in Java wraps in two’s complement: `MAX_VALUE + 1` is `MIN_VALUE`, and you get no exception. The wrap is in the promoted type of the operator, so `int * int` can already be wrong before you assign to `long` — promote an operand first. `/ 0` is `ArithmeticException`; overflow is not. If I need a throw, I use `Math.addExact` or `multiplyExact`.
