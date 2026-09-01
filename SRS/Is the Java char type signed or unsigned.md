<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# Is the Java char type signed or unsigned?

> [!abstract] Short answer
> **Unsigned.** `char` is a 16-bit **unsigned** integral type: values run from `'\u0000'` (0) through `'\uffff'` (65535). It holds one UTF-16 code unit. The other integral primitives (`byte`, `short`, `int`, `long`) are **signed** two’s-complement.

## The only unsigned integral primitive

Among Java’s integral types, `byte`/`short`/`int`/`long` are signed; `char` is specified as unsigned 16-bit integers that represent UTF-16 code units. `Character.MIN_VALUE` is `'\u0000'` and `Character.MAX_VALUE` is `'\uFFFF'` — there is no negative `char`. [[What is the value range of the Java char type]] is that 0…65535 box; [[Why is the Java char type 16 bits]] is why the width is 16.

```d2
direction: down
intg: "Integral primitives" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
signed: "byte short int long\nsigned two's-complement" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
ch: "char\n16-bit unsigned\nUTF-16 code unit" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}

intg -> signed
intg -> ch
```

**Fig. 1.** `char` is numeric and unsigned. Signedness is why `'\uFFFF'` widens to `65535`, not `-1`.

Widening `char` to `int`/`long` **zero-extends**. Widening a signed integer **sign-extends**. That is the practical difference: a high `char` stays non-negative as `int`. Arithmetic still promotes `char` to `int`, so `c + 1` is a signed `int` expression. Narrowing a `char` to `byte` or `short` keeps the low bits and **can be negative**, even though the `char` itself was unsigned. [[How does the Java char type relate to int]] is that conversion story; [[How does numeric promotion work in Java arithmetic expressions]] is why `char` math is done as `int`.

```java
public final class CharSignedness {
    public static void main(String[] args) {
        char max = '\uFFFF';
        int asInt = max;              // 65535 — zero-extend, not -1
        short asShort = (short) max;  // -1 — 16 bits reinterpreted as signed

        System.out.println(asInt);
        System.out.println(asShort);
        System.out.println((int) Character.MIN_VALUE); // 0
        System.out.println((int) Character.MAX_VALUE); // 65535
    }
}
```

**Listing 1.** A `char` is never negative. Casting it to `short` (the other 16-bit *signed* type) can be.

`int` and `long` gained **unsigned operations** (`Integer.parseUnsignedInt`, `Integer.toUnsignedString`, and so on) in later libraries; those types remain signed. That is not a second unsigned primitive. `char` is the language-level unsigned 16-bit type.

> [!warning] Unsigned `char` does not mean unsigned arithmetic
> `'a' + 1` is an `int` add after promotion. `(short) '\uFFFF'` is `-1`. Do not treat `char` as “C `unsigned short` that stays unsigned through every operator” — Java promotes it to signed `int` for `+`, `-`, `*`, `/`. Do not confuse it with `byte`, which *is* signed (−128…127) despite also being “small.”

> [!tip] Interview answer
> **`char` is unsigned; `byte`, `short`, `int`, and `long` are signed.** Its range is 0 through 65535, one UTF-16 code unit. Widening to `int` zero-fills, so `'\uFFFF'` becomes 65535, not −1. Arithmetic still happens in `int`, so you can get negatives only after a narrowing cast to a signed type.
