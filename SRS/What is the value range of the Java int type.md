<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# What is the value range of the Java `int` type?

> [!abstract] Short answer
> **−2 147 483 648 through 2 147 483 647**, inclusive: −2³¹ … 2³¹−1. That is `Integer.MIN_VALUE` … `Integer.MAX_VALUE`. `int` is a **32-bit signed** two’s-complement primitive (`Integer.SIZE` is 32, `Integer.BYTES` is 4). About ±2.1 billion. `Integer.MAX_VALUE + 1` wraps to `MIN_VALUE`; it does not throw.

## 32-bit signed, not “whatever fits in the variable”

`int` is the default integer type: unsuffixed integer literals are `int`, and `byte`/`short`/`char` arithmetic promotes to `int`. The language range is −2147483648 … 2147483647. The wrapper publishes the same endpoints. There is no unsigned `int` type; `Integer.toUnsignedLong` / `parseUnsignedInt` interpret the **same bits** as 0 … 2³²−1 in a wider type. [[What is the value range of the Java long type]] is ±2⁶³; [[What is the value range of the Java byte type]] is −128…127; [[What is the difference between int and Integer in Java]] is primitive vs wrapper.

```d2
direction: down
i: "int\n32-bit two's-complement" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
r: "-2147483648 … 2147483647\nInteger.MIN_VALUE … MAX_VALUE" {
  width: 360
  height: 70
  style.fill: "#e8f5e9"
}
w: "MAX_VALUE + 1 → MIN_VALUE\nsilent wrap" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}

i -> r
r -> w
```

**Fig. 1.** Fixed 32-bit box. Overflow does not widen to `long` unless an operand already is `long`.

A decimal literal larger than 2147483648 is a compile-time error even if you assign to `long` — the **token** is still `int` unless it has `L`. `2147483648` is legal **only** as the operand of unary `-` (so you can write `-2147483648`). Hex/binary/octal `int` literals must fit in 32 bits instead (`0x8000_0000` is `MIN_VALUE`). [[How do numeric suffixes and bases work for Java literals]] is that literal typing; [[What happens on integer overflow in Java]] and [[Why does multiplying two int values overflow before assignment to a long]] are wrap in the **promoted** type (`1_000_000 * 1_000_000` is already an `int` product). `Object.hashCode` returns `int`, so hash codes live in this range — that is the return type, not a second “hash range.”

```java
public final class IntRange {
    public static void main(String[] args) {
        System.out.println(Integer.MIN_VALUE); // -2147483648
        System.out.println(Integer.MAX_VALUE); // 2147483647
        System.out.println(Integer.SIZE);      // 32
        System.out.println(Integer.BYTES);     // 4

        System.out.println(Integer.MAX_VALUE + 1); // MIN_VALUE
        System.out.println(Integer.MIN_VALUE - 1); // MAX_VALUE

        int minLit = -2147483648;
        // int tooBig = 2147483648;           // does not compile
        // long stillIntToken = 10_000_000_000; // does not compile: needs L
        long ok = 10_000_000_000L;

        System.out.println(minLit);
        System.out.println(ok);
        System.out.println(Integer.toUnsignedLong(-1)); // 4294967295
    }
}
```

**Listing 1.** Endpoints and wrap. The unsuffixed decimal `2147483648` is not an `int` literal except beside unary `-`. Unsigned view of `-1` is 2³²−1 as a `long`.

> [!warning] “About 2.1 billion” is the type, not a reason `int * int` stays in range
> 2³¹−1 is 2 147 483 647, not a round 2 billion. A `long` variable does not save `a * b` when `a` and `b` are `int`. `Integer` is a heap object around this same range; `Integer.BYTES` is still 4 for the payload, not the object size ([[How much memory does an Integer object use compared with int]]).

> [!tip] Interview answer
> `int` is 32-bit signed two’s-complement from −2³¹ to 2³¹−1, `Integer.MIN_VALUE` to `MAX_VALUE` — about ±2.1 billion. Adding one to the maximum wraps to the minimum with no exception. Unsuffixed integer literals are `int`, so a number that does not fit needs `L`, not just a `long` variable.
