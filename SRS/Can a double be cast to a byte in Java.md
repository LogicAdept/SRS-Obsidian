<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/Conversions #SRS

# Can a `double` be cast to a `byte` in Java?

> [!abstract] Short answer
> **Yes, with an explicit cast.** `double` → `byte` is a **narrowing primitive conversion**. Assignment will not do it for you (`byte b = d;` does not compile). `(byte) d` does compile. The conversion is **lossy**: it may drop the fraction, change magnitude, and wrap. It does **not** throw.

## Two steps, then the low eight bits

A cast expression is a **casting context**, which allows narrowing. Assignment is not that context, except for a constant `byte`/`short`/`char`/`int` that already fits in the target. A `double` expression never gets that exception — even `byte b = 1.0;` is a compile-time error. See [[Can a byte be assigned to a double without a cast in Java]] for the opposite direction, which *is* widening and needs no cast.

The conversion itself is two steps:

1. Convert the `double` to `int`: **toward zero** (not half-up). `NaN` becomes `0`. Overflow and infinities become `Integer.MIN_VALUE` or `Integer.MAX_VALUE`.
2. Narrow that `int` to `byte` by keeping the **low 8 bits** — the same wrap as any other `int` → `byte` ([[What happens when you cast 280 to a Java byte]], [[What is the value range of the Java byte type]]).

So `99.9` becomes `99`, `-99.9` becomes `-99`, and `128.7` becomes `-128` (truncate to `128`, then wrap). The result is not clamped to −128…127. [[How would you explain widening and narrowing casts between Java primitive types]] is the full widening/narrowing map.

```d2
direction: down
d: "double d" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
i: "int, toward zero\nNaN → 0, inf → MIN/MAX" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
b: "byte = low 8 bits" {
  width: 200
  height: 55
  style.fill: "#e8f5e9"
}

d -> i: "(byte) d, step 1"
i -> b: "step 2, wrap"
```

**Fig. 1.** Narrowing `double` → `byte` is truncate-to-`int`, then wrap. No exception.

```java
public final class DoubleToByteCast {
    public static void main(String[] args) {
        double d = 99.9;
        byte b = (byte) d;            // 99
        System.out.println(b);

        System.out.println((byte) -99.9);                     // -99
        System.out.println((byte) 128.7);                     // -128
        System.out.println((byte) Double.NaN);                // 0
        System.out.println((byte) Double.POSITIVE_INFINITY);  // -1
        System.out.println((byte) Double.NEGATIVE_INFINITY);  // 0

        // byte lost = d;             // compile error: no assignment narrowing
        // byte one = 1.0;            // compile error: 1.0 is double, not int
    }
}
```

**Listing 1.** The cast is required. Toward zero, then 8-bit wrap. `NaN` → `0`; infinities follow `int` saturation then wrap to `0` and `-1`.

> [!warning] The cast does not round, clamp, or throw
> `(byte) 99.9` is `99`, not `100`. `(byte) 128.7` is `-128`, not `127`. Out-of-range and `NaN` still compile; you get a silent `byte`. A compile error happens only when the cast is **missing**, including `byte b = 1.0;` — a `double` constant is not eligible for the in-range `int`-literal narrowing.

> [!tip] Interview answer
> **Yes — write `(byte) d`. Assignment will not narrow a `double`.** The value is truncated toward zero to `int`, then the low 8 bits become the `byte`, so fractions disappear and values outside −128…127 wrap. Nothing throws; `NaN` becomes `0`.
