<!--
reps: 0
priority: 0
-->
#Java/Language/Operators/Bitwise #SRS

# Which bitwise operation you do you know?

> [!abstract] Short answer
> On integers: unary `~` (complement), `&` `|` `^` (AND, inclusive OR, XOR), and the shifts `<<` `>>` `>>>`. Each binary form has a compound assignment: `&=` `|=` `^=` `<<=` `>>=` `>>>=`. There is no `~=`. These work on two's-complement bits after promotion to `int` or `long`, not on `float` / `double`.

## The integer bitwise catalog

**Invert.** `~` flips every bit of one integral operand. After unary numeric promotion the result is `int` or `long`. `~x` equals `(-x) - 1`. Not `!`, which is boolean.

**Combine.** `&` is 1 only where **both** bits are 1. `|` is 1 where **either** is 1. `^` is 1 where they **differ**. Binary numeric promotion first; `byte & byte` is `int`. The same three tokens on two `boolean`s are **logical**, not bitwise, and they evaluate both sides. [[How would you explain logical operators in Java expressions]] is that reading; [[How would you explain bitwise operators on integers in Java]] is promotion, flags, and `&` versus `==`.

**Shift.** `<<` left, zeros in — equivalent to multiply by two to the power s, wrapping on overflow. `>>` signed right, **sign-extend** — floor-divide by that power of two (not the same as Java `/` on negatives). `>>>` unsigned right, **zero-fill**. Each operand is unary-promoted separately. The distance is masked: 0…31 for `int`, 0…63 for `long`. [[What is the difference between signed right shift and unsigned right shift in Java]] is `>>` versus `>>>`.

**Compound.** `E1 op= E2` is `E1 = (T)((E1) op (E2))` with `E1` evaluated once. That hidden cast is why `byte b &= 0x0f` compiles. Unary `~` has no compound form.

```d2
direction: down
ops: "integer bitwise ops" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
not: "~  invert" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
andor: "& | ^  combine\n&= |= ^=" {
  width: 260
  height: 70
  style.fill: "#fff8e1"
}
sh: "<< >> >>>  shift\n<<= >>= >>>=" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

ops -> not
ops -> andor
ops -> sh
```

**Fig. 1.** Three families: invert, combine, shift. Compound `op=` exists only for the binary ones.

```java
public final class BitwiseOperationsCatalog {
    public static void main(String[] args) {
        System.out.println(~0);             // -1
        System.out.println(~5);            // -6

        System.out.println(0b1100 & 0b1010); // 8   AND
        System.out.println(0b1100 | 0b1010); // 14  inclusive OR
        System.out.println(0b1100 ^ 0b1010); // 6   XOR

        System.out.println(1 << 4);         // 16  * 16, wrap if it overflows
        System.out.println(-8 >> 1);       // -4  sign-extend
        System.out.println(-1 >>> 1);      // 2147483647  zero-fill
        System.out.println(1 << 32);       // 1   distance & 0x1f

        byte b = 0b0011_1100;
        b &= 0x0f;                          // 0x0c; hidden (byte) cast
        System.out.println(b);

        int flags = 0;
        flags |= 0b0100;
        flags ^= 0b0100;
        flags <<= 1;
        System.out.println(flags);
    }
}
```

**Listing 1.** One example per operator family, plus compound `&=` / `|=` / `^=` / `<<=`. `1 << 32` is still `1`.

> [!warning] `>>` is not Java `/`, and `&=` is not `&&=`
> `-5 >> 1` is `-3` (floor); `-5 / 2` is `-2` (toward zero). `1 << 32` on `int` is `1`, not `0`. `&` `|` `^` on `boolean` are eager logical operators, not bit ops, and there is no `&&=`. `~` on a `byte` is an `int`.

> [!tip] Interview answer
> I list three families on integers: `~` inverts bits, `&` `|` `^` combine them, and `<<` `>>` `>>>` shift them, with compound `op=` for every binary one. `>>` sign-extends, `>>>` zero-fills, and the shift distance is masked to 5 or 6 bits. Same tokens `&` `|` `^` on booleans are logical, not bitwise, and `~` is not `!`.
