<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# How many bits are in one Java `byte`?

> [!abstract] Short answer
> **8.** `byte` is an 8-bit signed two’s-complement integer. That width is part of the language, not the host C `char`. `Byte.SIZE` is 8; `Byte.BYTES` is 1. The value range is −128…127 — 256 distinct bit patterns.

## Fixed 8-bit integer, not a platform octet guess

The integral types have specified widths: `byte` 8, `short` 16, `int` 32, `long` 64, all signed two’s-complement; `char` is 16-bit unsigned ([[Why is the Java char type 16 bits]], [[Why does the Java int type have a fixed size]]). `Byte.SIZE` is the bit width of that two’s-complement form (**8**); `Byte.BYTES` is **1**. [[What is the value range of the Java byte type]] is −2⁷ … 2⁷−1; [[What are the storage sizes of Java primitive types]] is the full table.

`boolean` is the contrast: it has no specified bit width ([[What is the size of the Java boolean type]]). A Java `byte` always does.

A local `byte` is still an 8-bit *type*. The JVM may compute it as `int` (one local-variable slot). That does not make `byte` 32 bits any more than `byte + byte` being `int` changes `Byte.SIZE`. Use `byte[]` when you need 8-bit cells ([[When should you use the Java byte type]]).

```d2
direction: down
b: "byte\n8-bit two's-complement" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
size: "Byte.SIZE = 8\nByte.BYTES = 1" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
range: "−128 … 127\n256 patterns" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}

b -> size
b -> range
```

**Fig. 1.** The type is 8 bits wide. The range is what those 8 bits mean as signed integers.

```java
public final class ByteBitWidth {
    public static void main(String[] args) {
        System.out.println(Byte.SIZE);   // 8
        System.out.println(Byte.BYTES);  // 1
        System.out.println(Byte.MIN_VALUE); // -128
        System.out.println(Byte.MAX_VALUE); // 127

        byte allBits = (byte) 0xFF;      // -1, not 255
        System.out.println(allBits);
        System.out.println(Byte.toUnsignedInt(allBits)); // 255
    }
}
```

**Listing 1.** Width from `Byte.SIZE`. Eight 1-bits is the signed value −1; `toUnsignedInt` is the 0…255 view of the same pattern.

> [!warning] 8 bits is not “unsigned 0…255”, and it is not C `char`
> High bit set means **negative**. `(byte) 0xFF` is −1. C `char` / `CHAR_BIT` can differ by platform; Java `byte` cannot. `Byte.BYTES` is 1 (how many 8-bit bytes hold a `byte`); do not confuse it with `Byte.SIZE` (bits). Locals promoted to `int` in arithmetic are still `byte` in the type system.

> [!tip] Interview answer
> **Eight — always.** Java `byte` is an 8-bit signed two’s-complement integer; `Byte.SIZE` is 8 and the range is −128 to 127. That is a language rule, not a machine `char`. The JVM may operate on it as `int`, but the type is still 8 bits.
