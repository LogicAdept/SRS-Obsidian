<!--
reps: 0
priority: 0
-->
#Java/Language/Operators/Bitwise #SRS

# How would you explain bitwise operators on integers in Java?

> [!abstract] Short answer
> `&`, `|`, and `^` combine corresponding bits of two integers (AND, inclusive OR, XOR). Unary `~` inverts every bit of one integer — `~x` is `(-x) - 1`. `<<`, `>>`, and `>>>` move those bits. After promotion the work is 32-bit `int` or 64-bit `long` two's-complement. These are not `&&` / `||` / `!`; those stay on `boolean`.

## Bitwise combine, invert, or shift the two's-complement bits

`byte`, `short`, `int`, and `long` are signed two's-complement. `char` is a 16-bit unsigned code unit, but `&` / `|` / `^` / `~` / shifts still run after **numeric promotion** to `int` or `long`. If any operand of `&`, `|`, or `^` is `long`, the operation is 64-bit; otherwise it is 32-bit `int`. `float` and `double` are rejected. `null` wrappers unbox first and throw `NullPointerException`. Integer bitwise operators never throw for overflow; bits wrap. [[How does numeric promotion work in Java arithmetic expressions]] is the ladder; [[What happens on integer overflow in Java]] is wrap, not a flag.

**Combine (`&`, `|`, `^`).** Binary numeric promotion first. The expression type **is** that promoted type, so `byte a & byte b` is `int`. `&` keeps a 1 only where **both** bits are 1; `|` where **either** is 1; `^` where they **differ**. Precedence among the three is `&` above `^` above `|`, and all three sit **below** `==` / `!=`. Write `(flags & MASK) == 0`, not `flags & MASK == 0` — the latter parses as `flags & (MASK == 0)` and does not compile. The same three tokens on two `boolean` operands are **logical**, not bitwise, and they still evaluate both sides. [[How would you explain logical operators in Java expressions]] is `&&` / `||` / `!`; [[Why cannot Java logical operators be applied to integers]] is why `5 || 6` is a compile-time error.

**Invert (`~`).** Unary numeric promotion. `~` is legal only on an integral type (or a wrapper that unboxes to one), never on `boolean` — that is `!`. The result type is the promoted type: `~` on a `byte` is `int`.

**Shift (`<<`, `>>`, `>>>`).** Unary promotion on **each** operand separately — a `long` distance does not widen an `int` left operand. The type is the promoted **left** type. The distance is masked: low **5** bits for `int` (`0`…`31`), low **6** for `long` (`0`…`63`). `n << s` multiplies by two to the power s (wrap). `>>` sign-extends (floor-divide by that power of two). `>>>` zero-fills. [[What is the difference between signed right shift and unsigned right shift in Java]] is sign-extend versus zero-fill.

Compound forms `&=`, `|=`, `^=`, `<<=`, `>>=`, `>>>=` are `E1 = (T)((E1) op (E2))` with `E1` evaluated once — the hidden cast is why `byte b &= 0x0f` compiles when `b = b & 0x0f` does not. [[Why does adding two byte values not compile as a byte in Java]] is the same hidden-cast story for `+=`.

```d2
direction: down
bits: "two's-complement bits\nint or long after promotion" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
combine: "&  AND\n|  inclusive OR\n^  exclusive OR" {
  width: 280
  height: 90
  style.fill: "#fff8e1"
}
invert: "~  invert every bit\n~x equals (-x) - 1" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
shift: "<<  left, zeros in\n>>  right, sign-extend\n>>>  right, zero-fill" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}

bits -> combine
bits -> invert
bits -> shift
```

**Fig. 1.** Integer bitwise operators either combine bits, invert them, or slide them. Shifts are a separate family with their own promotion and distance mask.

Typical flag code: `flags |= MASK` sets bits, `(flags & MASK) != 0` tests, `flags &= ~MASK` clears, `flags ^= MASK` toggles.

```java
public final class BitwiseOnIntegers {
    static final int MASK = 0b0100;

    public static void main(String[] args) {
        int flags = 0b1100;
        int other = 0b1010;

        System.out.println(flags & other); // 8   0b1000
        System.out.println(flags | other); // 14  0b1110
        System.out.println(flags ^ other); // 6   0b0110
        System.out.println(~0);            // -1
        System.out.println(~5);           // -6

        flags |= MASK;                      // set
        boolean on = (flags & MASK) != 0;  // test
        flags &= ~MASK;                     // clear
        flags ^= MASK;                      // toggle

        System.out.println(0xff00 & 0xf0f0); // 0xf000
        System.out.println(0xff00 ^ 0xf0f0); // 0x0ff0
        System.out.println(0xff00 | 0xf0f0); // 0xfff0

        System.out.println(1 << 4);   // 16
        System.out.println(1 << 32);  // 1   distance & 0x1f == 0
        System.out.println(-1 >> 1);  // -1  sign-extend
        System.out.println(-1 >>> 1);  // 2147483647

        byte a = 1, b = 2;
        int promoted = a & b;        // 0; type is int
        // byte c = a & b;           // does not compile
        b &= 0x0f;                    // hidden (byte) cast

        // if (flags & MASK == 0) {} // does not compile: == before &
        if ((flags & MASK) == 0) {
            System.out.println("no overlap");
        }

        System.out.println(on);
        System.out.println(promoted);
        System.out.println(flags);
    }
}
```

**Listing 1.** Bitwise combine, invert, shift, and flag idioms. Promotion, the shift-distance mask, and `&` versus `==` precedence are the compile-time surprises.

> [!warning] `==` binds tighter than `&`, and a shift of 32 is not a shift of 32
> `flags & MASK == 0` is `flags & (MASK == 0)`, mixing `int` with `boolean`. Parenthesize the mask test. `1 << 32` is `1`, not `0`, because only the low five bits of an `int` distance count. `~` on a `byte` is an `int`; assigning back needs a cast, and that cast keeps only eight bits. `Integer` operands unbox: a `null` throws before any bit is computed.

> [!tip] Interview answer
> Bitwise operators on integers are `&`, `|`, `^`, unary `~`, and the three shifts. They work on two's-complement bits after promotion to `int` or `long` — `byte & byte` is `int`, and `~x` is `-x - 1`. Shifts promote each side separately and mask the distance to 0…31 or 0…63, with `>>` sign-extending and `>>>` zero-filling. I always parenthesize `(flags & MASK) == 0`, and I do not confuse these with `&&` / `||`, which cannot take integers.
