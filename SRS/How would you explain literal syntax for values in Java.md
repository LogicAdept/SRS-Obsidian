<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/String #SRS

# How would you explain literal syntax for values in Java?

> [!abstract] Short answer
> **A literal is source text for a primitive value, a `String`, or `null`.** Integers default to `int` (`L`/`l` → `long`). Floating-point defaults to `double` (`F`/`f` → `float`). Booleans are only `true` and `false`. Characters use `'…'`; strings use `"…"` or a text block `"""…"""`. There is no `byte`/`short` suffix.

## Lexical literals vs `Type.class`

Lexical literals are the tokens that denote values: integer, floating-point, boolean, character, string (including text blocks), and `null`. `int.class` is a **class literal** (an expression), not that kind of token.

**Integers.** Decimal, hex (`0x`/`0X`), octal (leading `0`), binary (`0b`/`0B`). Underscores may separate digits, but not after `0x`/`0b` or at the ends. Unsuffixed → `int`; `L` preferred over `l`. Hex/octal/binary `int` literals that do not fit in 32 bits are compile errors. `byte b = 5;` works because a fitting **constant** `int` may narrow ([[Why does assigning 128 to a byte without a cast fail to compile]]).

**Floating-point.** Unsuffixed `3.14` is `double` ([[What is the default type of a Java floating-point literal]]). `F`/`f` makes `float`. Hex floats use `p`/`P` exponents. A nonzero literal that rounds to infinity or to zero is a compile-time error.

**Boolean / null / char.** Only `true` and `false` ([[Why cannot you assign 0 or TRUE to a Java boolean]]). `null` is the null type, not a keyword. `'a'` is one UTF-16 code unit; `'\n'` and octal escapes are allowed.

**Strings.** `"…"` cannot contain a raw newline. A text block is `"""` … `"""` and may contain newlines and unescaped `"`. Both evaluate to `String`. Many of these forms are compile-time constants ([[What is a compile-time constant in Java]]).

```d2
direction: down
lit: "literal token" {
  width: 160
  height: 45
  style.fill: "#fff3e0"
}
prim: "int long float double\nboolean char" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
str: "String / text block" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
n: "null" {
  width: 120
  height: 45
  style.fill: "#ffebee"
}

lit -> prim
lit -> str
lit -> n
```

**Fig. 1.** Lexical literals write primitive, `String`, or `null` values. `Type.class` is a separate expression.

```java
public final class Literals {
    public static void main(String[] args) {
        int dec = 1_000;
        int hex = 0xFF;
        int bin = 0b1010;
        int oct = 010;              // 8 — leading zero is octal
        long big = 1L;
        double d = 3.14;            // double, not float
        float f = 3.14f;
        boolean ok = true;
        char c = 'A';
        String s = "line\n";
        String block = """
                hello
                """;
        Object nobody = null;

        System.out.println(dec);
        System.out.println(oct);
        System.out.println(d);
        System.out.println(f);
        System.out.println(ok);
        System.out.println(c);
        System.out.println(s);
        System.out.println(block);
        System.out.println(nobody);
        System.out.println(hex + bin + big);
    }
}
```

**Listing 1.** Bases, suffixes, underscores, `true`, `char`, string vs text block, `null`. `010` is eight.

> [!warning] `010` is eight, `3.14` is `double`, and `l` looks like `1`
> A leading `0` starts octal, not a padded decimal. `float x = 3.14;` does not compile. Prefer `L` on longs. Underscores cannot sit next to `0x`/`0b` or at the end (`0x_FF`, `1_`). `TRUE` and `0` are not boolean literals. There is no `42b` for `byte`.

> [!tip] Interview answer
> **Literals are how you write primitive values, strings, and `null` in source.** Integers are `int` unless marked `L`; `3.14` is `double` unless marked `f`. Booleans are only `true`/`false`; `char` uses quotes; strings use `"…"` or text blocks. Watch octal `0…` and the missing `byte`/`short` suffixes.
