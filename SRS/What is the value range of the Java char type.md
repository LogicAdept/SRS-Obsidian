<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# What is the value range of the Java `char` type?

> [!abstract] Short answer
> **0 through 65535**, inclusive: `'\u0000'` … `'\uffff'`. That is `Character.MIN_VALUE` … `Character.MAX_VALUE`. `char` is the **only unsigned** integral primitive — **16 bits**, one UTF-16 **code unit**, **65536** distinct values. It cannot be negative. A Unicode code point above U+FFFF is **not** one `char`; it needs a **surrogate pair** (two `char`s) or an `int`.

## Unsigned 16-bit code unit, not “any Unicode character”

The integral types list `char` with range `'\u0000'` to `'\uffff'` (0…65535). `Character.SIZE` is **16**; the encoding is unsigned binary, not two’s-complement. There is no negative `char`. A character literal is always exactly one of those units (`'A'`, `'\u03a9'`, `'\uFFFF'`). [[Is the Java char type signed or unsigned]] is that signedness; [[Why is the Java char type 16 bits]] is why the width is 16; [[What is the value range of the Java byte type]] is the signed 8-bit contrast (−128…127).

```d2
direction: down
ch: "char\n16-bit unsigned" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
bmp: "0 … 65535\nBMP code unit" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
sup: "U+10000 … U+10FFFF\ntwo char units or int" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

ch -> bmp
ch -> sup: "not one char"
```

**Fig. 1.** `char` range is the Basic Multilingual Plane as UTF-16 units. Supplementary code points start at `Character.MIN_SUPPLEMENTARY_CODE_POINT` (U+10000) and go to `Character.MAX_CODE_POINT` (U+10FFFF).

`Character.isBmpCodePoint(cp)` is true exactly when `cp` lies between `MIN_VALUE` and `MAX_VALUE` — those code points fit in **one** `char`. `Character.charCount(cp)` returns **2** when `cp >= 0x10000`. Emoji and other supplementary characters are that second case. [[How does the Java char type relate to int]] is zero-extension to `int` (`'\uFFFF'` is `65535`, not `-1`); [[What is the difference between char and String in Java]] is a `String` that can hold the pair.

A constant `int` assigns to `char` only if it is representable (`char c = 65;` is `'A'`; `char c = -1;` and `char c = 65536;` do not compile). `(char) -1` is `'\uFFFF'`. Arithmetic promotes `char` to `int`, so `c + 1` is `int`. A `char` field defaults to `'\u0000'`.

```java
public final class CharRange {
    public static void main(String[] args) {
        System.out.println((int) Character.MIN_VALUE); // 0
        System.out.println((int) Character.MAX_VALUE); // 65535
        System.out.println(Character.SIZE);            // 16

        char omega = '\u03a9';
        char max = '\uFFFF';
        // char neg = -1;                 // does not compile
        char fromBits = (char) -1;        // '\uFFFF'
        // char emoji = '😀';             // not one char (supplementary)

        System.out.println((int) omega);
        System.out.println((int) max);
        System.out.println(fromBits == max);
        System.out.println(Character.isBmpCodePoint('A'));     // true
        System.out.println(Character.charCount(0x1F600));      // 2
        System.out.println("\uD83D\uDE00".length());           // 2
    }
}
```

**Listing 1.** Endpoints 0 and 65535. `-1` is not a `char` constant; the cast is `MAX_VALUE`. One grinning-face code point is two UTF-16 units.

> [!warning] 65535 is the max `char`, not the max Unicode scalar
> Unicode scalars go to U+10FFFF. `char` stops at U+FFFF. “Emoji fit in `char`” is false for anything outside the BMP. `char c = -1` does not compile; there is no signed `char`. Widening to `int` does not produce a negative number.

> [!tip] Interview answer
> `char` runs from 0 to 65535 — `'\u0000'` to `'\uffff'` — an unsigned 16-bit UTF-16 code unit. That is 65536 values and no negatives. It is not the full Unicode range: supplementary characters need two `char`s or an `int` code point. `'A'` is one unit; many emoji are two.
