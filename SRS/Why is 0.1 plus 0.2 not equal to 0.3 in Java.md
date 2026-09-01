<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/FloatingPoint #SRS

# Why is 0.1 plus 0.2 not equal to 0.3 in Java?

> [!abstract] Short answer
> `0.1` and `0.2` are **`double`** (IEEE 754 **binary64**) literals. 1/10 is not a finite binary fraction, so each literal is stored as the **nearest** representable value, not the exact decimal. Adding those approximations yields a sum whose bits are **not** the same as the approximation of `0.3`. `0.1 + 0.2 == 0.3` is **`false`**; `System.out.println(0.1 + 0.2)` typically shows `0.30000000000000004`. This is binary floating point, not a Java-only bug.

## Binary fractions, not decimal tenths

A finite `double` is s · m · 2^(e−N+1) with a 53-bit significand. Powers of ten that are not powers of two (0.1, 0.2, 0.3) do not land on that grid. Unsuffixed `0.1` is already `double`; `0.1f` is the same issue at binary32. `==` on `double` is IEEE equality: two distinct finite values compare unequal. The compiler does not “use decimals” because you wrote a decimal literal. [[What is the default type of a Java floating-point literal]] is that default; [[What is the difference between float and double in Java]] is 24- vs 53-bit significand; [[What is the difference between double and BigDecimal for decimal calculations]] is the exact-decimal type.

```d2
direction: down
src: "0.1 + 0.2" {
  width: 180
  height: 40
}
bin: "each literal rounded\nto a binary64 value" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
sum: "IEEE add of approximations\n≠ rounded 0.3" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
dec: "new BigDecimal(\"0.1\")\n.add(\"0.2\") → 0.3 exactly" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

src -> bin
bin -> sum
src -> dec
```

**Fig. 1.** The literals are already rounded. `BigDecimal` from a **String** keeps decimal tenths.

For money and other exact decimals, construct `BigDecimal` from a **String** (or integers), not from a `double`. `new BigDecimal(0.1)` is an exact picture of the **already inexact** `double` (the API warns it is 0.10000000000000000555…). `BigDecimal.valueOf(0.1)` goes through `Double.toString` and is closer to what you printed, still not a reason to start from `double`. `==` on `double` is also the wrong tool for “almost”: `NaN == NaN` is false; `0.0 == -0.0` is true. Use a documented tolerance / `Math.ulp` when you mean approximate, not a guessed epsilon copied from a blog. [[How do numeric suffixes and bases work for Java literals]] is `D`/`F`; [[Does floating-point division by zero throw ArithmeticException]] is IEEE specials, not decimal error.

```java
import java.math.BigDecimal;

public final class PointOnePlusPointTwo {
    public static void main(String[] args) {
        System.out.println(0.1 + 0.2);            // 0.30000000000000004
        System.out.println(0.1 + 0.2 == 0.3);     // false

        BigDecimal exact = new BigDecimal("0.1").add(new BigDecimal("0.2"));
        System.out.println(exact);                 // 0.3
        System.out.println(exact.compareTo(new BigDecimal("0.3")) == 0); // true

        BigDecimal fromDouble = new BigDecimal(0.1); // not 0.1
        System.out.println(fromDouble);
        // new BigDecimal(0.1).add(new BigDecimal(0.2)) is still the binary error
    }
}
```

**Listing 1.** `double` `==` sees two different binary values. `BigDecimal("0.1")` is the decimal tenth. `new BigDecimal(0.1)` is not.

> [!warning] `new BigDecimal(0.1)` does not rescue `0.1`
> The `double` constructor records the binary approximation. Use `"0.1"`. Do not “fix” `==` by rounding to two printed digits in your head — `println` already rounds for display. Integer `1/10` is a different operator ([[Why does integer division of 5 by 2 equal 2 in Java]]); it does not produce `0.1` either.

> [!tip] Interview answer
> `0.1` cannot be stored exactly in IEEE binary `double`, so `0.1 + 0.2` is the sum of two rounded values and is not bit-equal to `0.3`. That is why `==` is false. For money, add `BigDecimal` built from strings, not from `double` literals.
