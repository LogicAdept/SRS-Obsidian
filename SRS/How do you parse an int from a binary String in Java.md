<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #Java/String #SRS

# How do you parse an `int` from a binary `String` in Java?

> [!abstract] Short answer
> Call **`Integer.parseInt(s, 2)`** for a primitive, or **`Integer.valueOf(s, 2)`** for a boxed `Integer`. The second argument is the **radix**, not a length. Digits are those for which `Character.digit(ch, radix)` is nonnegative (`0` and `1` in binary). `valueOf(s, 2)` is `Integer.valueOf(Integer.parseInt(s, 2))`. Strings produced by `toBinaryString` for a **negative** `int` need **`parseUnsignedInt(s, 2)`**, not signed `parseInt`.

## Signed parse with radix 2

`parseInt(String s, int radix)` reads a **signed** integer. Every character must be a digit of that radix, except that the first character may be `'-'` or `'+'` when the string is longer than one character. Radix **2** is binary; omit the radix (or pass 10) for decimal. Official examples include `parseInt("1100110", 2)` → `102` and `parseInt("111", 2)` → `7`.

Failure is **`NumberFormatException`**, including: `null` or empty `s`; radix outside `Character.MIN_RADIX`..`MAX_RADIX` (2..36); a character that is not a digit of that radix; a magnitude that is not a value of type `int`. See [[What is NumberFormatException]] and [[What is the difference between Integer.parseInt and Integer.valueOf]].

```d2
direction: down
s: "String of 0/1\noptional leading + or -" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
parse: "parseInt(s, 2)" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
box: "valueOf(s, 2)\n= valueOf(parseInt(s, 2))" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
nfe: "NumberFormatException" {
  width: 240
  height: 60
  style.fill: "#ffebee"
}

s -> parse
parse -> box: "in range"
parse -> nfe: "null, bad digit, overflow, bad radix"
```

**Fig. 1.** Binary parse is radix 2; boxing is a second step after the primitive parse.

```java
int seven = Integer.parseInt("111", 2);           // 7
Integer boxed = Integer.valueOf("111", 2);        // Integer 7
int decimal = Integer.parseInt("100");            // 100, radix 10
int also = Integer.parseInt("1100110", 2);        // 102
```

**Listing 1.** Conceptual: radix 2 for binary; no-arg `parseInt` is decimal.

## Unsigned inverse of `toBinaryString`

`toBinaryString` / `toHexString` / `toOctalString` print an **unsigned** 32-bit magnitude. `parseUnsignedInt(s, 2)` (Java 8) is the matching parse: a leading `'+'` is allowed, a leading `'-'` is not, and the magnitude may be up to 2³²−1 (those values land in the negative `int` range). That is how you round-trip the strings from [[How do you convert an int to a binary hex or octal String]].

```java
String bits = Integer.toBinaryString(-8);
// "11111111111111111111111111111000"
int back = Integer.parseUnsignedInt(bits, 2); // -8

Integer.parseInt(bits, 2); // NumberFormatException: not a signed int
```

**Listing 2.** Conceptual: a 32-bit unsigned binary string overflows signed `parseInt`.

> [!warning] Radix is not a width, and `0b` is not accepted
> `parseInt("111", 2)` does not mean “three bits of padding.” There is no `0b` / `0x` prefix on `parseInt`; `"0b111"` with radix 2 throws because `'b'` is not a binary digit (`parseInt("99", 8)` is the same idea). `Integer.decode` is a different API for `0x` / `#` / leading `0` octal on decimal-looking strings.

> [!warning] `parseInt` throws `NumberFormatException`, not `NullPointerException`, for `null`
> `parseInt(null, 2)` and `parseInt("", 2)` both throw `NumberFormatException`. Out-of-range radix does too — unlike `Integer.toString(i, radix)`, which silently falls back to 10. Leading minus is illegal on `parseUnsignedInt`.

> [!tip] Interview answer
> **Parse binary with `Integer.parseInt(s, 2)` for an `int`, or `Integer.valueOf(s, 2)` for a wrapper — the `2` is the radix.** Invalid digits, `null`, empty strings, and overflow throw `NumberFormatException`. To parse a `toBinaryString` of a negative value, use `parseUnsignedInt(s, 2)` instead of signed `parseInt`.
