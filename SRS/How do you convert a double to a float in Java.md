<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/FloatingPoint #SRS

# How do you convert a `double` to a `float` in Java?

> [!abstract] Short answer
> **Cast it:** `float f = (float) d;`. Assignment will not narrow a `double` to `float`. The `f` / `F` suffix is a `float` **literal**, not a conversion of an existing `double`. On a `Double`, `floatValue()` is the same narrowing.

## Narrowing, not assignment

`double` → `float` is a **narrowing primitive conversion**. A casting context allows it; an assignment context does not. `float f = d;` is a compile-time error. After `(float) d`, the expression is already `float`, so the assignment is an identity conversion. The same cast is required to pass a `double` into a `float` parameter. [[Can a double be cast to a byte in Java]] is another narrowing that needs `(byte)`; this one stays in floating-point.

The conversion follows IEEE 754 binary64 → binary32, **round to nearest**. It can drop significand bits. It can also drop **range**: a finite `double` too large for `float` becomes a signed infinity; a nonzero `double` too small becomes a `float` zero. `NaN` stays `NaN`; infinities keep their sign. Nothing throws. [[What is the difference between float and double in Java]] is why 64 bits do not fit in 32.

An unsuffixed decimal like `36.01` is already type `double` ([[What is the default type of a Java floating-point literal]]). `36.01f` does not convert a `double`; it writes a `float` directly. `Double.floatValue()` is documented as this same narrowing (IEEE 754 convertFormat).

```d2
direction: down
d: "double d / 36.01" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
cast: "(float) d" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}
fail: "float f = d\ncompile error" {
  width: 200
  height: 70
  style.fill: "#ffebee"
}

d -> cast: "narrowing"
d -> fail
```

**Fig. 1.** Convert a `double` with `(float)`. The `f` suffix is a different spelling of a `float` value, not that conversion.

```java
public final class DoubleToFloat {
    public static void main(String[] args) {
        double num = 3.14159;
        float narrowed = (float) num;
        System.out.println(narrowed);

        // float avg = 36.01;          // compile error: double → float
        float avg = 36.01f;            // float literal
        float also = (float) 36.01;    // narrowing a double literal
        System.out.println(avg);
        System.out.println(also);

        System.out.println((float) 1e100);   // Infinity — finite double, too big
        System.out.println((float) -1e100);  // -Infinity
        System.out.println((float) 1e-50);   // 0.0 — underflow
        System.out.println((float) Double.NaN);

        Double boxed = Double.valueOf(num);
        System.out.println(boxed.floatValue());
        // float boom = 1e100f;        // compile error: float literal → infinity
    }
}
```

**Listing 1.** `(float)` converts. `36.01f` is not a conversion. Overflow of the conversion is `Infinity`; overflow of a `float` **literal** is a compile-time error.

> [!warning] `36.01` is `double`; overflow of a cast is not a compile error
> `float avg = 36.01;` does not compile. Use `36.01f` or `(float) 36.01`. Those are different: the suffix never starts from `double`. `(float) 1e100` compiles and is `Infinity`; `1e100f` does not compile — a nonzero literal that rounds to infinity or to zero is rejected, while the narrowing conversion quietly yields infinity or `0.0`.

> [!tip] Interview answer
> **Cast: `float f = (float) d`.** Java will not assign a `double` to a `float` without that. The conversion can lose digits, overflow to infinity, or underflow to zero, and it does not throw. An `f` suffix is a `float` literal — it is not how you convert a `double` variable.
