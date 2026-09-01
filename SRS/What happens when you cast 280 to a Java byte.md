<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/Conversions #SRS

# What happens when you cast 280 to a Java `byte`?

> [!abstract] Short answer
> **You get `24`.** `(byte) 280` is a narrowing primitive conversion: it keeps the **low 8 bits** of the `int` and drops the rest. 280 = 256 + 24, so the result is `24`. There is no rounding, no clamp to 127, and no exception.

## Low eight bits, two’s-complement `byte`

`byte` is signed 8-bit, range −128…127 ([[What is the value range of the Java byte type]]). 280 does not fit, so assignment without a cast does not compile (`byte b = 280;` and `byte b = bigValue;` are errors). The **cast** is what makes it legal ([[Why does assigning 128 to a byte without a cast fail to compile]]).

Narrowing a signed integer to `byte` **discards all but the lowest 8 bits**. The remaining pattern is read as two’s-complement. 280 is `0x00000118`; the low byte is `0x18` = 24. Same rule for `int` → `short` / `char` and `long` → `int`: keep `n` low bits, where `n` is the target width. [[What happens on integer overflow in Java]] is wrap in arithmetic; this is wrap on **conversion**.

If bit 7 of that byte is set, the `byte` is **negative** even though the `int` was positive: `(byte) 255` is `-1`, `(byte) 128` is `-128`. 280 happens to land on 24, which is still positive — that is not a general “remainder in 0…255” result. [[Can a double be cast to a byte in Java]] does this same 8-bit wrap after truncating the `double` to `int`.

```d2
direction: down
i: "int 280\n0x00000118" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
bits: "keep low 8 bits\n0x18" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
b: "byte 24" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}

i -> bits: "(byte)"
bits -> b
```

**Fig. 1.** `(byte) 280` is bit truncation, not modulo-into-unsigned or clamp-to-`Byte.MAX_VALUE`.

```java
public final class Cast280ToByte {
    public static void main(String[] args) {
        int bigValue = 280;
        byte small = (byte) bigValue;
        System.out.println(small);          // 24

        System.out.println((byte) 280);     // 24
        System.out.println((byte) 255);     // -1
        System.out.println((byte) 128);     // -128

        // byte tooBig = 280;               // compile error: constant does not fit
        // byte fromVar = bigValue;         // compile error: not a constant narrowing
    }
}
```

**Listing 1.** 280 → 24. 255 and 128 show the same 8-bit keep when the high bit of the byte is set.

> [!warning] Silent wrap, not `127` and not `ArithmeticException`
> Out-of-range narrowing is defined, not a runtime error. `(byte) 280` is `24`, not `127`. Do not treat the result as an unsigned 0…255 remainder — `(byte) 255` is `-1`. A missing cast is a **compile** error; a present cast never throws.

> [!tip] Interview answer
> **`(byte) 280` is `24`.** The cast keeps the low 8 bits of the `int` (280 = 256 + 24) and does not round, clamp, or throw. Assignment without the cast does not compile. If those 8 bits have the sign bit set, the `byte` is negative — 280 just happens not to.
