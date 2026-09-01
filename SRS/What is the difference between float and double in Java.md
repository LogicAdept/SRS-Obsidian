<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/FloatingPoint #SRS

# What is the difference between `float` and `double` in Java?

> [!abstract] Short answer
> Both are IEEE 754 **binary** floating-point primitives. `float` is **binary32**: `Float.SIZE` is **32** bits (`Float.BYTES` is **4**), significand **24** bits (`Float.PRECISION`). `double` is **binary64**: **64** bits / **8** bytes, significand **53** bits. Unsuffixed literals (`3.14`, `1e1`) are **`double`**. `float` needs `f`/`F` or a narrowing cast. `double` is the type mixed arithmetic promotes to when either operand is `double`.

## Width, exponent, and the literal default

`float` maps to IEEE binary32 (`N` = 24, exponent field 8 bits, `Float.MAX_EXPONENT` = 127). `double` maps to binary64 (`N` = 53, exponent field 11 bits, `Double.MAX_EXPONENT` = 1023). That is why the finite ranges differ: largest finite `float` rounds from `3.4028235e38f`; largest finite `double` from `1.7976931348623157e308`. Smallest positive nonzero values are the subnormals `1.4e-45f` and `4.9e-324`. Both types have signed zeros, infinities, and NaN. [[What is the default type of a Java floating-point literal]] is why `3.14` is not a `float`; [[How do numeric suffixes and bases work for Java literals]] is `F`/`f` vs optional `D`/`d`.

```d2
direction: down
fp: "binary floating-point" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
fl: "float  binary32\n32 bits, 4 bytes\n24-bit significand" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
db: "double  binary64\n64 bits, 8 bytes\n53-bit significand" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

fp -> fl
fp -> db
```

**Fig. 1.** Same IEEE model, different format. Decimal “about 7 digits vs about 15” is just log₁₀ of those significand widths — not a separate language constant.

Widening `float` → `double` is allowed on assignment; every finite `float` is a `double`. The other direction is narrowing: `float x = 3.14;` does not compile. In an expression, if either operand is `double`, the operation is `double`. Both still **round in binary**, so neither is a decimal money type. [[How does numeric promotion work in Java arithmetic expressions]] is that ladder; [[What is the difference between double and BigDecimal for decimal calculations]] is when binary is the wrong base; [[Does floating-point division by zero throw ArithmeticException]] is infinity/NaN vs integer `/ 0`.

Use `double` as the default local and API type. Use `float` when you are storing many values and have measured that 4 bytes vs 8 matters (large arrays, some graphics buffers). The language does **not** say `float` arithmetic is faster; on a lot of hardware the opposite is true, and it is not a Java rule.

```java
public final class FloatVsDouble {
    public static void main(String[] args) {
        System.out.println(Float.BYTES + " " + Double.BYTES);       // 4 8
        System.out.println(Float.SIZE + " " + Double.SIZE);         // 32 64
        System.out.println(Float.PRECISION + " " + Double.PRECISION); // 24 53
        System.out.println(Float.MAX_VALUE);
        System.out.println(Double.MAX_VALUE);

        double d = 3.14;            // unsuffixed → double
        float f = 3.14f;
        double widened = f;         // exact widen
        // float narrowed = 3.14;   // does not compile
        float cast = (float) d;
        System.out.println(d);
        System.out.println(f);
        System.out.println(widened);
        System.out.println(cast);
    }
}
```

**Listing 1.** Sizes and significand widths from the wrapper constants. `3.14` is `double`; `3.14f` is `float`. Widen is assignment; narrow needs a cast or `f`.

> [!warning] `3.14` is a `double`, and “7 decimal digits” is not a field
> `float x = 3.14;` is a compile error. `Float.PRECISION` is **24 bits**, not 7. The “~7 vs ~15 decimal digits” slogan is an approximation of those significands. `float` is not “the fast one”; it is the **narrower** binary32 format. Neither type is exact for `0.1`.

> [!tip] Interview answer
> `float` is 32-bit IEEE binary32 and `double` is 64-bit binary64 — 4 vs 8 bytes, 24- vs 53-bit significand, and a much wider exponent on `double`. Literals without a suffix are `double`, so I write `f` for `float`. I use `double` unless I have a storage reason for `float`, and I do not use either for exact decimal money.
