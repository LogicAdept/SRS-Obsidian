<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# What is the value range of the Java `byte` type?

> [!abstract] Short answer
> **−128 through 127**, inclusive: `Byte.MIN_VALUE` is −2⁷ and `Byte.MAX_VALUE` is 2⁷−1. That is an **8-bit signed** two’s-complement integer — **256** distinct values. It is **not** 0…255. `byte b = 128;` does not compile; `(byte) 128` is **−128**.

## Signed 8-bit, not an unsigned octet

`byte` is an integral primitive alongside `short`, `int`, `long`, and `char`. Only `char` is unsigned. The language range is −128…127. The wrapper publishes the same endpoints as `Byte.MIN_VALUE` / `Byte.MAX_VALUE`. `Byte.SIZE` is the bit width of that two’s-complement pattern; `Byte.BYTES` is `1`. [[How many bits are in one Java byte]] is the width; [[Is the Java char type signed or unsigned]] is the unsigned contrast; [[What is the value range of the Java short type]] is the 16-bit signed neighbour (−32768…32767).

```d2
direction: down
b: "byte\n8-bit two's-complement" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
r: "-128 … 127\nByte.MIN_VALUE … MAX_VALUE" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
no: "not 0 … 255\nthat is toUnsignedInt" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

b -> r
b -> no
```

**Fig. 1.** The type is signed. `Byte.toUnsignedInt(b)` maps a `byte` onto 0…255 as an `int`; it does not change what `byte` can store.

A constant `int` that **fits** may be assigned to `byte` (`byte x = 127;`). `128` does not fit, so it needs a cast, and the cast **wraps**: the low 8 bits of 128 are the two’s-complement pattern for −128. Arithmetic promotes `byte` to `int` first, so `a + b` is `int`; storing it back needs `(byte)` and can wrap the same way. Overflow of the `byte` range is silent wrap, not an exception. [[Why does adding two byte values not compile as a byte in Java]] is the promotion; [[What happens on integer overflow in Java]] is wrap in the promoted type. For a 0…255 **view** of the same bits, `Byte.toUnsignedInt` / `compareUnsigned` exist — the variable is still a signed `byte`.

```java
public final class ByteRange {
    public static void main(String[] args) {
        System.out.println(Byte.MIN_VALUE); // -128
        System.out.println(Byte.MAX_VALUE); // 127
        System.out.println(Byte.SIZE);      // 8
        System.out.println(Byte.BYTES);     // 1

        byte max = 127;
        byte min = -128;
        // byte tooBig = 128;               // does not compile
        byte wrapped = (byte) 128;          // -128
        byte overflow = (byte) (max + 1);   // -128

        System.out.println(wrapped);
        System.out.println(overflow);
        System.out.println(Byte.toUnsignedInt(min)); // 128
        System.out.println(min);
        System.out.println(max);
    }
}
```

**Listing 1.** Endpoints and width from `Byte`. A constant `128` is not a `byte`; the cast and `127 + 1` wrap to `MIN_VALUE`. Unsigned view is an `int`.

> [!warning] `byte` is not 0…255, and `128` is not “almost in range”
> C and some network APIs treat an octet as unsigned. Java `byte` does not. High bit set means **negative**. `parseByte("128")` throws `NumberFormatException`. Arrays of `byte` used as binary data often need `& 0xff` or `toUnsignedInt` when you print or compare them as 0…255.

> [!tip] Interview answer
> `byte` is an 8-bit signed two’s-complement integer from −128 to 127 — `Byte.MIN_VALUE` to `Byte.MAX_VALUE`. That is 256 values, not an unsigned 0…255 type. `128` does not fit; a cast wraps to −128. I promote or use `toUnsignedInt` when I need the octet as 0…255.
