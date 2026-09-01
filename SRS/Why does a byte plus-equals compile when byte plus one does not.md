<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/NumericPromotion #SRS

# Why does a `byte` plus-equals compile when `byte` plus one does not?

> [!abstract] Short answer
> **`+=` inserts a cast; `+` does not.** `b + 1` is an `int` after numeric promotion, so `b = b + 1` is assigning `int` to `byte` and does not compile. `b += 1` means `b = (byte)(b + 1)` — the narrowing is part of the compound assignment, and `b` is evaluated only once.

## Promotion on `+`, hidden `(byte)` on `+=`

In a numeric arithmetic context the promoted type is `int`, so `byte` (and `short`/`char`) operands widen before `+`. The sum’s type is `int`. Assignment will not narrow a non-constant `int` into `byte` ([[Why does adding two byte values not compile as a byte in Java]], [[How does numeric promotion work in Java arithmetic expressions]]). `b = b + 1` therefore needs an explicit `(byte)` unless you write a constant that already fits (`byte b = 6;` is a different rule).

Compound assignment is defined as:

`E1 op= E2`  →  `E1 = (T)((E1) op (E2))`

with `T` the type of `E1`, except `E1` is evaluated only once. For `byte b += 1`, that is `b = (byte)(b + 1)`. The same hidden narrowing applies to `short` and `char`, and to `++` / `--` on those types. [[Why does assigning 128 to a byte without a cast fail to compile]] is the constant-range check; here the cast is always inserted, **even when the result does not fit**.

That cast is ordinary narrowing: low 8 bits, silent wrap, no exception ([[What happens when you cast 280 to a Java byte]]). `byte b = 127; b += 1;` is `-128`. `short x = 3; x += 4.6;` is `7` — add in `double`, then `(short)`.

```d2
direction: down
plus: "b + 1\ntype int" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
assign: "b = b + 1\ncompile error" {
  width: 200
  height: 70
  style.fill: "#ffebee"
}
comp: "b += 1\n(byte)(b + 1)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

plus -> assign
plus -> comp: "compound adds the cast"
```

**Fig. 1.** The `+` is the same. Compound assignment supplies `(byte)`; simple assignment does not.

```java
public final class BytePlusEquals {
    public static void main(String[] args) {
        byte b = 5;
        // b = b + 1;                 // compile error: int → byte
        b = (byte) (b + 1);           // 6 — explicit narrowing
        b += 1;                       // 7 — same narrowing, implicit
        System.out.println(b);

        byte max = 127;
        max += 1;                     // -128
        System.out.println(max);

        short x = 3;
        x += 4.6;                     // 7
        System.out.println(x);
    }
}
```

**Listing 1.** `+=` is `+` plus a narrowing cast. `127 + 1` as `byte` wraps; `short += 4.6` truncates toward zero to `7`.

> [!warning] `+=` is not “`=` plus `+`” for `byte`/`short`/`char`
> `b += 1` can overflow while still compiling. `b = b + 1` refuses to compile instead of wrapping. `b++` has the same hidden narrow as `+= 1`. Do not use `+=` to “keep it a `byte`” if you needed the range check that simple assignment would have given you — you only get that check for **constants**.

> [!tip] Interview answer
> **`b + 1` is an `int`, so `b = b + 1` does not compile.** `b += 1` is defined as `b = (byte)(b + 1)` with `b` evaluated once, so it compiles. That hidden cast can wrap (`127 += 1` → `-128`) or drop a fraction (`short += 4.6` → `7`).
