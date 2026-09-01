<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# Why do Java primitive types have bounded numeric ranges?

> [!abstract] Short answer
> A primitive is a **fixed-width bit pattern**, not an arbitrary mathematical integer. The language **predefines** those widths: 8/16/32/64-bit two’s-complement (`byte`/`short`/`int`/`long`), 16-bit unsigned `char`, IEEE 754 **binary32**/**binary64** (`float`/`double`), and a two-value `boolean`. Every implementation uses the **same** ranges so a program’s arithmetic does not depend on the CPU. When a result does not fit, integer `+`/`*` **wrap**; `float`/`double` follow IEEE (infinity/NaN). Use `long`, `Math.*Exact`, `BigInteger`, or `BigDecimal` when the bound is the problem.

## Specified finite types, not “as wide as the machine”

Java is strongly typed: a type **limits** the values a variable can hold and the meaning of operators. Numeric primitives are those finite sets — 2⁸ `byte` values, 2³² `int` values, 2⁶⁴ `long` values, and the IEEE grids for `float`/`double`. That is why `int` is always −2³¹…2³¹−1, including on a 64-bit JVM: the type is not “native word.” `char` is 16-bit because it is a UTF-16 unit, not an unbounded character. [[Where is the authoritative reference for Java primitive types]] is JLS Primitive Types and Values; [[What is the value range of the Java int type]] and [[What is the value range of the Java long type]] are the integer boxes; [[What is the difference between float and double in Java]] is 24- vs 53-bit significand; [[What is the value range of the Java char type]] is 0…65535.

```d2
direction: down
spec: "JLS predefined widths\n8 / 16 / 32 / 64 / IEEE" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
ops: "operators on that many bits\nwrap or IEEE specials" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
esc: "BigInteger / BigDecimal\nMath.*Exact / wider primitive" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

spec -> ops
ops -> esc
```

**Fig. 1.** Bounds are the type. Overflow is what operators do at those bounds, not a reason the bounds exist.

Integer overflow keeps the low-order bits (sign can flip). `1_000_000 * 1_000_000` does not grow to `long` unless an operand is already `long`. Floating-point overflow becomes infinities, not a bigger `double`. `BigInteger` is **arbitrary-precision** integers (two’s-complement conceptually, no fixed word); `>>>` is omitted there because an infinite-width sign makes no sense. `BigDecimal` is decimal scale, not a bigger `double`. [[What happens on integer overflow in Java]] and [[Why does multiplying two int values overflow before assignment to a long]] are wrap; [[Why is 0.1 plus 0.2 not equal to 0.3 in Java]] and [[What is the difference between double and BigDecimal for decimal calculations]] are the IEEE/decimal split.

```java
import java.math.BigInteger;

public final class BoundedPrimitives {
    public static void main(String[] args) {
        System.out.println(Integer.MAX_VALUE);           // 2147483647
        System.out.println(Integer.MAX_VALUE + 1);       // wrap: MIN_VALUE
        System.out.println(Long.MAX_VALUE);              // still finite

        int product = 1_000_000 * 1_000_000;             // wrapped int
        BigInteger wide = BigInteger.valueOf(1_000_000)
                .multiply(BigInteger.valueOf(1_000_000)); // 10^12 exactly

        System.out.println(product);
        System.out.println(wide);
        // Math.multiplyExact(1_000_000, 1_000_000);     // ArithmeticException
    }
}
```

**Listing 1.** The `int` box does not grow. `BigInteger` is the library type with no language-fixed width.

> [!warning] A bigger variable is not a bigger `*`
> `long n = Integer.MAX_VALUE * 2;` still multiplies as `int`. Bounds are per **operation type**, then assignment. Do not expect primitives to throw on overflow (except `/` `%` by zero and `*Exact`). `boolean` is bounded too: only `true` and `false`.

> [!tip] Interview answer
> Primitive ranges are bounded because each type is a fixed-width encoding the JLS specifies for every JVM — 32-bit `int`, 64-bit `long`, IEEE `float`/`double`. That makes arithmetic portable and maps to hardware operations. When you need more, you change type (`long`, `BigInteger`), you do not get a silent wider `int`.
