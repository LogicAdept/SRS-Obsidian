<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Language/Primitives/FloatingPoint #SRS

# Does floating-point division by zero throw `ArithmeticException`?

> [!abstract] Short answer
> **No.** `float`/`double` `/` follows IEEE 754: a nonzero finite value divided by zero is a signed **infinity**, and `0.0/0.0` is **NaN**. That evaluation never throws a run-time exception. `ArithmeticException` is for **integer** `/` (and `%`) when the divisor is zero — for example `1/0`.

## Integer `/` vs floating-point `/`

After binary numeric promotion, if both operands are integers and the divisor is `0`, `/` throws `ArithmeticException` (a `RuntimeException`). The platform API gives integer “divide by zero” as the example of that class ([[What is ArithmeticException]], [[What are common kinds of unchecked exceptions in Java]]).

If the operands are floating-point, the result is determined by IEEE 754, including infinities and NaN. Overflow, underflow, division by zero, or lost bits still **do not** throw. `2.0/0` is `Infinity`. Signed zeros and signed infinities follow the signs of the operands.

```d2
direction: down
div: "a / b" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
ints: "int / long\ndivisor 0" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
fp: "float / double\ndivisor 0.0" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
ae: "ArithmeticException" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
inf: "signed Infinity\nor NaN if 0.0/0.0" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
div -> ints
div -> fp
ints -> ae
fp -> inf
```

**Fig. 1.** Same `/` token; the operand types decide exception vs infinity/NaN.

```java
class Demo {
    static void show() {
        System.out.println(1 / 0);       // ArithmeticException
        System.out.println(2.0 / 0);     // Infinity
        System.out.println(-1.0 / 0.0);  // -Infinity
        System.out.println(0.0 / 0.0);   // NaN
    }
}
```

**Listing 1.** `1/0` is `int` division. `2.0/0` promotes to `double`. `0.0/0.0` is NaN, not an exception. Test NaN with `Double.isNaN` — `x == Double.NaN` is always false.

Integer `%` with a zero divisor also throws `ArithmeticException`. Floating-point `%` with a zero divisor yields NaN and does not throw.

> [!warning] `1.0/0` is not `1/0`
> `1/0` is `int`. `1.0/0` is floating-point (the `int` `0` is converted). Interview snippets that “look like” divide-by-zero differ by a decimal point. Integer overflow on `Integer.MIN_VALUE / -1` also does **not** throw.

> [!warning] Infinity is not an exception you `catch`
> `catch (ArithmeticException e)` around `double` division will not run for `/ 0.0`. Use `Double.isInfinite` / `Double.isNaN` if you must detect those results. `ArithmeticException` is unchecked, so a handler is optional when integer `/` really can throw ([[Does catch Exception also catch RuntimeException]]).

> [!tip] Interview answer
> **No. Floating-point division by zero yields `Infinity` or `NaN` and never throws. `ArithmeticException` is what integer `1/0` throws. `0.0/0.0` is NaN, not an exception.**
