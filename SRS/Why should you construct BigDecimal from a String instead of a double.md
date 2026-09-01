<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/FloatingPoint #SRS

# Why should you construct `BigDecimal` from a `String` instead of a `double`?

> [!abstract] Short answer
> `new BigDecimal(0.1)` does **not** mean decimal one tenth. The `double` constructor stores the **exact decimal of the binary64 bits**, which for `0.1` is 0.10000000000000000555…. `new BigDecimal("0.1")` is scale-1 one tenth, as written. The API recommends the **String** constructor for that reason. If you already have a `double`, `BigDecimal.valueOf(d)` (via `Double.toString`) is the usual conversion — still not a substitute for typing the decimal you meant.

## The `double` is already rounded before `BigDecimal` sees it

`0.1` is a `double` literal: IEEE binary64 cannot hold 1/10, so the value passed into `BigDecimal(double)` is already the nearest representable number. That constructor then prints that bit pattern as a long decimal. It is an **exact** conversion of the wrong quantity. The String constructor parses decimal digits (optional sign, fraction, exponent) and sets scale from the fraction; `"0.1"` is unscaled 1 with scale 1. Adding `"0.2"` yields `"0.3"`. [[Why is 0.1 plus 0.2 not equal to 0.3 in Java]] is why the bits differ; [[What is the difference between double and BigDecimal for decimal calculations]] is when to use each type; [[What is the default type of a Java floating-point literal]] is why `0.1` is already `double`.

```d2
direction: down
lit: "0.1 in source" {
  width: 180
  height: 40
}
dbl: "double constructor\nexact bits of binary64 0.1" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}
str: "String constructor\ndecimal 0.1, scale 1" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

lit -> dbl
lit -> str
```

**Fig. 1.** Same digits in the source, two meanings. Quotes keep the decimal; a `double` argument does not.

`BigDecimal.valueOf(0.1)` uses `Double.toString` then the String constructor — what you would see from `println(0.1)`, not the 50-digit `double` expansion. Prefer that over `new BigDecimal(d)` when the input **is** a `double`. Prefer `BigDecimal(long)` / integers (cents) when you can avoid floating input entirely. `Infinity` and `NaN` make `BigDecimal(double)` throw `NumberFormatException`. Spaces in the string are illegal. [[What is the difference between float and double in Java]] is still binary; [[How do numeric suffixes and bases work for Java literals]] is `F`/`D` — they do not make a decimal `BigDecimal`.

```java
import java.math.BigDecimal;

public final class BigDecimalFromString {
    public static void main(String[] args) {
        BigDecimal fromString = new BigDecimal("0.1");
        BigDecimal fromDouble = new BigDecimal(0.1);
        BigDecimal viaValueOf = BigDecimal.valueOf(0.1);

        System.out.println(fromString);  // 0.1
        System.out.println(fromDouble);  // 0.10000000000000000555…
        System.out.println(viaValueOf);  // 0.1  (canonical double text)

        System.out.println(fromString.add(new BigDecimal("0.2"))); // 0.3
        System.out.println(fromString.equals(fromDouble));         // false
    }
}
```

**Listing 1.** Quotes vs a `double` argument. `valueOf` follows `Double.toString`, not the raw binary expansion.

> [!warning] `new BigDecimal(0.1).add(new BigDecimal(0.2))` is still binary error
> Both arguments are already rounded `double`s; adding them in `BigDecimal` preserves that error at huge scale. Do not “fix” money by wrapping literals you already typed as `0.1`. Write `"0.1"` or pass an integer number of minor units.

> [!tip] Interview answer
> Construct `BigDecimal` from a `String` so the decimal you typed is the value you get. `new BigDecimal(0.1)` copies the inexact `double` for 0.1. If the value starts as `double`, use `valueOf`; if you control the source, never put it through `double` at all.
