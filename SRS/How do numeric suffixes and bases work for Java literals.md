<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# How do numeric suffixes and bases work for Java literals?

> [!abstract] Short answer
> An **integer** literal is `int` unless you add `L` or `l` (`long`). A **floating-point** literal is `double` unless you add `F` or `f` (`float`); `D`/`d` is an optional `double` marker. Integer bases are decimal (default), hex (`0x`/`0X`), binary (`0b`/`0B`), and octal (a leading `0` plus more `0`–`7` digits). Underscores may sit **between** digits as separators; they do not change the value.

## Type comes from the suffix; radix from the prefix

There is no suffix for `int`, `byte`, or `short`. The only integer suffix letters are `L` and `l`. Prefer `L`: lowercase `l` is easy to misread as digit `1`. Floating-point suffixes are `F`/`f` and optional `D`/`d`. An unsuffixed `1.5` or `1e1` is already `double`; `1.5f` is `float`. [[What is the default type of a Java floating-point literal]] is the floating half of that defaulting rule.

```d2
direction: down
lit: "Numeric literal" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
intg: "Integer form\ndefault type int" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
fp: "Floating form\ndefault type double" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
base: "0x / 0X  hex\n0b / 0B  binary\n0…     octal\nelse    decimal" {
  width: 240
  height: 120
  style.fill: "#e8f5e9"
}
lsuf: "L or l → long" {
  width: 200
  height: 60
  style.fill: "#ffebee"
}
fsuf: "F or f → float\nD or d optional" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}

lit -> intg
lit -> fp
intg -> base
intg -> lsuf
fp -> fsuf
```

**Fig. 1.** Suffix picks `long` / `float` / optional `double`. Prefix picks integer radix. Unsuffixed integer stays `int`; unsuffixed floating-point stays `double`.

Hex digits are `0`–`9` and `a`–`f` / `A`–`F`. Binary digits are `0` and `1`. A lone `0` is a **decimal** zero; octal always has two or more digits (`00`, `0372`). Decimal and hexadecimal floating-point also exist: decimal uses `e`/`E` for a power of ten; hex floating-point uses `p`/`P` for a power of two (`0x1.0p3` is `8.0`) and that binary exponent is required.

```java
public final class NumericLiterals {
    public static void main(String[] args) {
        int decimal = 255;
        int hex = 0xFF;
        int binary = 0b1111_1111;
        int octal = 0377;                 // 255, not three hundred seventy-seven
        long tenBillion = 10_000_000_000L;
        float rate = 1.5f;
        double plain = 1.5;
        double hexFloat = 0x1.0p3;        // 8.0
        int minInt = 0x8000_0000;         // Integer.MIN_VALUE; no L
        System.out.println(decimal == hex && hex == binary && binary == octal);
        System.out.println(tenBillion);
        System.out.println(rate);
        System.out.println(plain);
        System.out.println(hexFloat);
        System.out.println(minInt);
    }
}
```

**Listing 1.** Same `int` value in four radices; `L` on a decimal that cannot be an `int`; `F` on a `float`; hex `int` bit pattern `0x8000_0000` is legal without `L`.

A decimal `int` literal may be at most `2147483648`, and that exact value is legal **only** as the operand of unary `-` (so you can write `-2147483648`). Any larger unsuffixed decimal is a compile-time error — including `long n = 10_000_000_000;`, because the **literal** is still typed `int`. Hex, octal, and binary `int` literals instead must **fit in 32 bits**; `0x8000_0000` and `0xffff_ffff` are valid `int`s (`MIN_VALUE` and `-1`), not “too big, add `L`.” The same split applies to `long` at 64 bits (`9223372036854775808L` only beside unary `-`). [[What is the value range of the Java int type]] is that 32-bit box; [[Why does multiplying two int values overflow before assignment to a long]] is the related runtime mistake of computing in `int` and only then storing a `long`.

Underscores are separators **between** digits: `1_000_000`, `0x00_FF__00_FF`, `2_147_483_648L` are fine; `_1`, `1_`, `0x_FF`, `0b_1`, and `1_L` are not, because an underscore must not sit before the first digit, after the last digit, or immediately after `0x`/`0b`.

> [!warning] `L` is about the literal’s type, not the variable’s type
> `long n = 10_000_000_000;` does not compile: the unsuffixed token is an `int` literal larger than `2147483648`. Write `10_000_000_000L`. Do **not** treat “bigger than `Integer.MAX_VALUE` ⇒ need `L`” as a rule for every radix: `0x8000_0000` is a 32-bit `int`. A leading `0` on a multi-digit integer is octal (`010` is `8`); `08` is illegal because `8` is not an octal digit.

> [!tip] Interview answer
> **Unsuffixed integer literals are `int`; unsuffixed floating-point literals are `double`.** Add `L` for `long` and `F` for `float`. Write hex as `0x`, binary as `0b`, octal as a leading `0`, and use underscores only between digits. A huge decimal still needs `L` even when the variable is `long`, because the suffix types the literal itself.
