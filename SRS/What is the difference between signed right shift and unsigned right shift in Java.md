<!--
reps: 0
priority: 0
-->
#Java/Language/Operators/Bitwise #SRS

# What is the difference between signed right shift and unsigned right shift in Java?

> [!abstract] Short answer
> `>>` is **signed** (arithmetic): it fills on the left with the **sign bit**. A negative value stays negative; the result is **floor**(n / 2^s). `>>>` is **unsigned** (logical): it fills on the left with **zeros**, so a negative `int` becomes a large **non-negative** `int`. For n ≥ 0 they match. Java has no unsigned integer type; `>>>` is how you treat the bits as unsigned.

## Sign-extend vs zero-fill

Shift operators are `<<`, `>>`, and `>>>`. Each operand gets **unary** promotion separately (`byte`/`short`/`char` → `int`). The expression’s type is the promoted **left** type (`int` or `long`). A `long` distance does **not** make an `int` left operand `long`. Only the low **5** bits of the distance count for `int` (`& 0x1f`, 0…31) and the low **6** for `long` (`& 0x3f`, 0…63). [[How does numeric promotion work in Java arithmetic expressions]] is that unary-vs-binary split.

```d2
direction: down
n: "two's-complement bits of n" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
sar: ">>  sign-extend\nfill with the sign bit" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
shr: ">>>  zero-extend\nfill with 0" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

n -> sar
n -> shr
```

**Fig. 1.** Same shift distance. `>>` copies bit 31 (or 63) inward. `>>>` inserts zeros, which is why `-1 >>> 1` is `Integer.MAX_VALUE`.

`n << s` is multiply by 2^s (wrap on overflow). `n >> s` is floor-divide by 2^s. For **non-negative** n that matches `n / (1 << s)`. For **negative** n, Java `/` truncates **toward zero**, so `-5 / 2` is `-2` but `-5 >> 1` is `-3`. `>>>` on a negative `int` is the same as `>>` **plus** a term that cancels the propagated sign bits — the high bits become 0. Positive n: `>>` and `>>>` are equal. [[What happens on integer overflow in Java]] is the wrap on `<<`; [[How would you explain bitwise operators on integers in Java]] is `&`/`|`/`^` beside shifts.

Because unary promotion **sign-extends** a `byte` to `int` first, `(byte) -1 >>> 1` is **not** `127`. The `byte` becomes `int` `-1` (`0xffffffff`), then `>>> 1` is `0x7fffffff`. To logical-shift only 8 bits, mask after promoting: `(b & 0xff) >>> 1`.

```java
public final class SignedVsUnsignedRightShift {
    public static void main(String[] args) {
        System.out.println(1 << 4);       // 16
        System.out.println(-8 >> 1);      // -4  sign-extend
        System.out.println(-8 >>> 28);    // 15  zero-fill
        System.out.println(-1 >> 1);      // -1
        System.out.println(-1 >>> 1);     // 2147483647

        byte b = -1;
        System.out.println(b >>> 1);      // 2147483647, not 127
        System.out.println((b & 0xff) >>> 1); // 127

        System.out.println(-5 >> 1);      // -3  floor
        System.out.println(-5 / 2);       // -2  toward zero
        System.out.println(1 >> 32);      // 1   distance & 0x1f == 0
    }
}
```

**Listing 1.** `>>` keeps the sign. `>>>` zeros the high bits. A `byte` is promoted to `int` before `>>>`. Distance 32 on an `int` is masked to 0.

> [!warning] `>>` is not `/ 2` for negatives, and `>>>` is not an 8-bit operation on `byte`
> `-5 >> 1` is `-3`, not `-2`. `n >> 32` on `int` is `n`, not `0`. `>>>` on `byte`/`short` still runs on the promoted `int`. There is no `>>>` for `float`/`double`.

> [!tip] Interview answer
> `>>` sign-extends: negatives stay negative and you get floor-division by two. `>>>` zero-fills: the sign bit is treated as data, so a negative `int` becomes a large positive value. They agree when the value is ≥ 0. I also mention that the shift distance is masked to 5 or 6 bits, and that `byte` promotes to `int` before the shift.
