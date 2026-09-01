<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# What is the value range of the Java short type?

> [!abstract] Short answer
> **−32768 through 32767.** `short` is a **16-bit signed** two’s-complement integer: `Short.MIN_VALUE` is −2¹⁵, `Short.MAX_VALUE` is 2¹⁵−1. That is the same width as `char`, but `char` is unsigned.

## Sixteen bits, signed

`Short.SIZE` is 16; `Short.BYTES` is 2 ([[What are the storage sizes of Java primitive types]]). Two’s complement means the high bit is the sign: 0x7FFF is 32767, 0x8000 is −32768. Adding one to `MAX_VALUE` wraps to `MIN_VALUE` if you cast back to `short`.

An `int` literal in range may be assigned to a `short` without a cast (`short s = 32_767`). 32768 is not representable, so `short s = 32_768` does not compile — same constant-narrowing rule as `byte` and 128 ([[Why does assigning 128 to a byte without a cast fail to compile]]). A non-constant `int` always needs `(short)`.

`byte` is the 8-bit signed neighbor (−128…127) ([[What is the value range of the Java byte type]]). Arithmetic still promotes `short` to `int`, so `s + 1` is an `int`.

```d2
direction: down
s: "short 16-bit signed" {
  width: 180
  height: 40
}
lo: "-32768" {
  width: 100
  height: 40
}
hi: "32767" {
  width: 100
  height: 40
}

s -> lo: "MIN_VALUE"
s -> hi: "MAX_VALUE"
```

**Fig. 1.** Inclusive bounds: `Short.MIN_VALUE` … `Short.MAX_VALUE`.

```java
public final class ShortRange {
    public static void main(String[] args) {
        System.out.println(Short.MIN_VALUE);      // -32768
        System.out.println(Short.MAX_VALUE);      // 32767
        short wrap = (short) (Short.MAX_VALUE + 1);
        System.out.println(wrap);                 // -32768
        short ok = 32_767;
        System.out.println(ok);
        // short bad = 32_768;                    // does not compile
    }
}
```

**Listing 1.** Range constants, wrap of `MAX_VALUE + 1`, and a representable literal. `32_768` needs `(short)`.

> [!warning] Same width as `char`, opposite sign
> `char` is also 16 bits but **unsigned** (0…65535). `(char) (-1)` is not a `short` −1 you can round-trip without a cast. Do not treat `short` as a tiny `int` in expressions: `short + short` is `int`.

> [!tip] Interview answer
> **`short` is −32768 to 32767** — 16-bit signed two’s complement. Quote `Short.MIN_VALUE` / `MAX_VALUE`. It is not an unsigned 16-bit type; that is `char`.
