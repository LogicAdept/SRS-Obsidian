<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/FloatingPoint #SRS

# What is the difference between `double` and `BigDecimal` for decimal calculations?

> [!abstract] Short answer
> `double` is IEEE **binary64**: a fixed 53-bit significand in **base 2**. Many decimals (`0.1`, `0.2`) are not exact, so `0.1 + 0.2 == 0.3` is `false`. `BigDecimal` is an **immutable object**: an integer unscaled value times **10 to the power of minus scale**, with **arbitrary** decimal precision. Use `add`/`subtract`/`multiply`/`divide`, not `+`. For a decimal you typed, construct from a **`String`**, not from a `double`.

## Binary fraction vs decimal scale

`double` (and `float`) follow IEEE 754 binary floating-point. Finite values are a sign, a significand, and a power of **two**. That is excellent for scientific magnitude and hardware speed, and it is why overflow becomes **infinity** and `0.0/0.0` is **NaN**. It is the wrong representation when the specification is **base-10 digits** (money, tax, “exactly two decimal places”). [[What is the difference between float and double in Java]] is the two binary widths; [[Does floating-point division by zero throw ArithmeticException]] is the IEEE specials.

```d2
direction: down
need: "decimal 0.1" {
  width: 180
  height: 45
  style.fill: "#e3f2fd"
}
d: "double\nbinary64 approximation" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
bd: "BigDecimal(\"0.1\")\nunscaled 1, scale 1" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

need -> d: "not exact"
need -> bd: "exact"
```

**Fig. 1.** Same source decimal. `double` stores the nearest binary64 value. `BigDecimal` from a `String` stores the decimal digits.

`BigDecimal` is `unscaledValue × 10^(-scale)`. Arithmetic is methods; the object does not change. Add/multiply with no `MathContext` are exact. `divide` with a non-terminating expansion (`1/3`) throws `ArithmeticException` unless you pass a **rounding mode** / `MathContext`. Divide-by-zero also throws — `BigDecimal` has **no** NaN or infinities. That is slower and allocates; it is the trade for decimal control.

`new BigDecimal(0.1)` converts the **already inexact** `double`. The API’s own example is `0.1000000000000000055511151231257827021181583404541015625`, not scale-1 `0.1`. `new BigDecimal("0.1")` is exact. If you already have a `double`, `BigDecimal.valueOf(d)` uses `Double.toString` and is the preferred conversion — still not a reason to start from `0.1` as a `double` literal. [[Why should you construct BigDecimal from a String instead of a double]] is that constructor choice; [[What is the default type of a Java floating-point literal]] is why `0.1` is a `double` token.

```java
import java.math.BigDecimal;

public final class DoubleVsBigDecimal {
    public static void main(String[] args) {
        System.out.println(0.1 + 0.2);
        System.out.println(0.1 + 0.2 == 0.3); // false

        BigDecimal sum = new BigDecimal("0.1")
                .add(new BigDecimal("0.2"));
        System.out.println(sum);              // 0.3
        System.out.println(sum.compareTo(new BigDecimal("0.3")) == 0);

        System.out.println(new BigDecimal(0.1)); // long binary expansion
        // sum + sum;                            // does not compile
        // new BigDecimal("1").divide(new BigDecimal("3")); // ArithmeticException
    }
}
```

**Listing 1.** `double` addition is inexact. `String` `BigDecimal`s add to `0.3`. `new BigDecimal(0.1)` keeps the binary error. Use `compareTo` for numeric equality — `equals` also requires the same scale.

> [!warning] `new BigDecimal(0.1)` does not mean decimal one-tenth
> Passing a `double` bakes in the binary rounding. `+` on two `BigDecimal`s does not compile. `1/3` without rounding throws; so does divide-by-zero. `equals` treats `0.3` and `0.30` as different because the scales differ — `compareTo` is the numeric test.

> [!tip] Interview answer
> `double` is binary floating-point, so values like `0.1` are approximations and `0.1 + 0.2` is not `0.3`. `BigDecimal` stores a decimal unscaled integer and a scale, so money and other base-10 totals can be exact if I construct from a `String` and use `add`/`divide` with an explicit rounding mode. I do not write `new BigDecimal(0.1)`, and I do not use `double` for currency.
