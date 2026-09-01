<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/String #SRS

# How do you convert an `int` to a binary, hex, or octal `String`?

> [!abstract] Short answer
> Use `Integer`’s static converters on the primitive (a wrapper unboxes): **`toBinaryString`**, **`toHexString`**, **`toOctalString`**. They print the value as an **unsigned** 32-bit magnitude in base 2 / 16 / 8, lowercase hex, no extra leading zeros. For a **signed** radix string (minus sign when negative), use **`Integer.toString(i, radix)`** — that is not the same as `toBinaryString` when `i < 0`.

## Dedicated unsigned converters

Each of `toBinaryString`, `toHexString`, and `toOctalString` takes an `int`. If the argument is negative, the unsigned magnitude is that argument **plus 2³²**; otherwise it is the argument itself. Digits are ASCII `0`/`1` (binary), `01234567` (octal), or `0123456789abcdef` (hex). Uppercase hex is `Integer.toHexString(n).toUpperCase()`. A zero magnitude is a single `'0'`. The inverse is `Integer.parseUnsignedInt(s, radix)` with radix 2, 8, or 16 — see [[How do you parse an int from a binary String in Java]].

```d2
direction: down
val: "int i  (wrapper unboxes)" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
unsigned: "toBinaryString / toHexString / toOctalString\nunsigned, no leading zeros" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}
signed: "toString(i, radix)\nminus sign if i < 0" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}

val -> unsigned
val -> signed
```

**Fig. 1.** Same `int`, two families: unsigned dedicated methods versus signed `toString(i, radix)`.

```java
int eight = 8;
Integer.toHexString(eight);    // "8"
Integer.toOctalString(eight);  // "10"
Integer.toBinaryString(eight); // "1000"
Integer.toBinaryString(42);    // "101010"
```

**Listing 1.** Conceptual: positive values; no `0x` / `0` prefix and no padding.

## Signed `toString(int, int)` is the general radix form

`Integer.toString(i, radix)` prints a **signed** representation. A negative `i` starts with `'-'`. Digits are `0123456789abcdefghijklmnopqrstuvwxyz`; radix 16 therefore uses `a`–`f`. If `radix` is outside `Character.MIN_RADIX`..`Character.MAX_RADIX` (**2..36**), the method silently uses radix **10** — it does not throw. `parseInt` with a bad radix is the opposite: it throws `NumberFormatException` (see [[What is the difference between Integer.parseInt and Integer.valueOf]]).

```java
Integer.toString(8, 2);   // "1000"  — same as toBinaryString(8)
Integer.toString(-8, 2);  // "-1000" — signed
Integer.toBinaryString(-8);
// "11111111111111111111111111111000" — unsigned 32-bit
Integer.toHexString(-8);  // "fffffff8"
```

**Listing 2.** Conceptual: `toString(i, 2)` is not `toBinaryString` for negatives.

Java 8 also added `Integer.toUnsignedString(i, radix)` for unsigned output in any legal radix. `toHexString`’s API note points at `java.util.HexFormat` when you need padding, delimiters, or mixed case on bytes.

> [!warning] Unsigned dedicated methods vs signed `toString`
> Treating `toBinaryString` as “`toString(i, 2)` with a shorter name” is wrong for any negative `int`. `toBinaryString(-1)` is thirty-two `'1'` characters, not `"-1"`. Recover those strings with `parseUnsignedInt`, not `parseInt`, or the leading bits look like a huge positive value.

> [!warning] No padding, lowercase hex, out-of-range radix
> `toHexString(10)` is `"a"`, not `"0A"` or `"0000000a"`. Pad or uppercase yourself (or use `HexFormat`). `Integer.toString(i, 1)` and `Integer.toString(i, 37)` both fall back to decimal. These factories take the numeric `int`; they do not format an `Integer` object’s identity or a raw IEEE bit pattern (`floatToIntBits` is a different API).

> [!tip] Interview answer
> **`Integer.toBinaryString`, `toHexString`, and `toOctalString` turn an `int` into an unsigned base-2 / 16 / 8 string with no extra zeros and lowercase hex.** `Integer.toString(i, radix)` is the signed general form (radix 2..36, otherwise decimal). For negatives those two families disagree, so do not treat `toBinaryString` as a nickname for `toString(i, 2)`.
