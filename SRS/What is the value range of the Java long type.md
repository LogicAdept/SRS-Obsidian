<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# What is the value range of the Java `long` type?

> [!abstract] Short answer
> **−9 223 372 036 854 775 808 through 9 223 372 036 854 775 807**, inclusive: −2⁶³ … 2⁶³−1. That is `Long.MIN_VALUE` … `Long.MAX_VALUE`. `long` is a **64-bit signed** two’s-complement primitive (`Long.SIZE` is 64, `Long.BYTES` is 8). `Long.MAX_VALUE + 1` wraps to `MIN_VALUE`; it does not throw.

## 64-bit signed; the `L` is on the literal, not the variable

`long` is the wide integral primitive. Mixed `int`/`long` arithmetic promotes to `long` and then wraps in 64 bits. The language range is −9223372036854775808 … 9223372036854775807. The wrapper publishes the same endpoints. There is no unsigned `long` type; `Long.toUnsignedString` / `divideUnsigned` interpret the **same bits** as 0 … 2⁶⁴−1. [[What is the value range of the Java int type]] is ±2³¹; [[How does numeric promotion work in Java arithmetic expressions]] is why one `long` operand widens the other.

```d2
direction: down
l: "long\n64-bit two's-complement" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
r: "-9223372036854775808 … 9223372036854775807\nLong.MIN_VALUE … MAX_VALUE" {
  width: 400
  height: 70
  style.fill: "#e8f5e9"
}
s: "unsuffixed 10000000000\nstill an int literal — needs L" {
  width: 320
  height: 70
  style.fill: "#fff8e1"
}

l -> r
r -> s
```

**Fig. 1.** Fixed 64-bit box. A `long` **variable** does not change the type of an unsuffixed integer token.

An unsuffixed integer literal is `int`. `10_000_000_000` does not compile even when the destination is `long` — the **token** is out of `int` range. Write `10_000_000_000L`. Prefer `L` over `l` (`l` looks like digit `1`). `9223372036854775808L` is legal **only** as the operand of unary `-` (so you can write `-9223372036854775808L`). Hex/binary/octal `long` literals must fit in 64 bits (`0x8000_0000_0000_0000L` is `MIN_VALUE`). [[How do numeric suffixes and bases work for Java literals]] is that typing; [[Why does multiplying two int values overflow before assignment to a long]] is wrap in `int` **before** the `long` store; [[What happens on integer overflow in Java]] is silent wrap for `long` too.

```java
public final class LongRange {
    public static void main(String[] args) {
        System.out.println(Long.MIN_VALUE); // -9223372036854775808
        System.out.println(Long.MAX_VALUE); // 9223372036854775807
        System.out.println(Long.SIZE);      // 64
        System.out.println(Long.BYTES);     // 8

        System.out.println(Long.MAX_VALUE + 1); // MIN_VALUE
        System.out.println(Long.MIN_VALUE - 1); // MAX_VALUE

        long minLit = -9223372036854775808L;
        // long tooBigIntToken = 10_000_000_000; // does not compile: needs L
        long ok = 10_000_000_000L;
        // long stillTooBig = 9223372036854775808L; // does not compile except as -9223372036854775808L

        System.out.println(minLit);
        System.out.println(ok);
        System.out.println(Long.toUnsignedString(-1L)); // 18446744073709551615
    }
}
```

**Listing 1.** Endpoints and wrap. The unsuffixed decimal `10000000000` is not a `long` just because the variable is. Unsigned view of `-1L` is 2⁶⁴−1 as a decimal string.

> [!warning] A `long` box does not rescue an `int` product
> `1_000_000 * 1_000_000` is still an `int` multiply. One operand must already be `long` (`1_000_000L * 1_000_000`) or the wrap happens first. `Long.MAX_VALUE + 1` is `MIN_VALUE`, not a `BigInteger`. `System.currentTimeMillis()` and epoch millis fit in `long`; they are not a second range.

> [!tip] Interview answer
> `long` is 64-bit signed two’s-complement from −2⁶³ to 2⁶³−1, `Long.MIN_VALUE` to `MAX_VALUE`. Adding one to the maximum wraps to the minimum with no exception. Unsuffixed integer literals are still `int`, so a number past about two billion needs an `L` suffix even when you assign it to a `long` variable.
