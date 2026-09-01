<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/Conversions #SRS

# How would you explain widening and narrowing casts between Java primitive types?

> [!abstract] Short answer
> **Widening goes to a “larger” numeric type and is allowed in assignment without a cast. Narrowing goes the other way and needs `(T)`.** Widening never throws. Narrowing never throws either — it can drop bits, fractions, or range. `boolean` does not convert to or from the numeric types.

## Two directions, two contexts

**Widening** (19 conversions): `byte` → `short`/`int`/`long`/`float`/`double`; `short` → `int`/`long`/`float`/`double`; `char` → `int`/`long`/`float`/`double`; `int` → `long`/`float`/`double`; `long` → `float`/`double`; `float` → `double`. Assignment and invocation apply this automatically, so `double d = someByte;` compiles ([[Can a byte be assigned to a double without a cast in Java]]).

The numeric value is preserved exactly for integral→integral, for `byte`/`short`/`char` → `float`/`double`, for `int` → `double`, and for `float` → `double`. **Not** always lossless: `int` → `float` and `long` → `float`/`double` may round.

**Narrowing** (22 conversions) is the reverse set, including `double` → `float` and every integer shrink. Assignment will not do it (except a constant `int` that already fits in `byte`/`short`/`char`). A cast expression will ([[Can a double be cast to a byte in Java]], [[How do you convert a double to a float in Java]]). Integer narrowing keeps the low *n* bits ([[What happens when you cast 280 to a Java byte]]). `double` → `byte` is two steps: toward zero to `int`, then 8-bit wrap. `double` → `float` can yield infinity or `0.0` from a finite value.

**`byte` → `char`** is both: widen to `int`, then narrow to `char`. It is **not** a widening conversion, so it needs a cast even though both are small.

`boolean` sits alone: no widening, no narrowing, no `(int) true` ([[Why cannot you assign 0 or TRUE to a Java boolean]]).

Compound assignment inserts the narrowing cast for you (`b += 1` is `(byte)(b + 1)`) ([[Why does a byte plus-equals compile when byte plus one does not]]).

```d2
direction: right
b: "byte" {
  width: 90
  height: 45
  style.fill: "#e3f2fd"
}
i: "int" {
  width: 80
  height: 45
  style.fill: "#e3f2fd"
}
d: "double" {
  width: 100
  height: 45
  style.fill: "#e8f5e9"
}

b -> i: "widen, no cast"
i -> d: "widen, no cast"
d -> b: "(byte), lossy"
```

**Fig. 1.** Assignment follows widening. The reverse is a cast, and it can wrap or drop a fraction.

```java
public final class WidenNarrow {
    public static void main(String[] args) {
        byte b = 1;
        int i = b;                 // widen
        double d = i;              // widen
        System.out.println(d);

        // byte back = d;          // compile error
        byte truncated = (byte) 99.9; // 99
        byte wrapped = (byte) 280;    // 24
        System.out.println(truncated);
        System.out.println(wrapped);

        // char ch = b;            // compile error: byte → char is not widening
        char ch = (char) b;
        System.out.println((int) ch);

        int big = 1234567890;
        float approx = big;        // widen, may lose bits
        System.out.println(big - (int) approx);

        // byte tooBig = 128;      // compile error: constant does not fit
        byte min = (byte) 128;     // -128
        System.out.println(min);
    }
}
```

**Listing 1.** Widening in assignment. Narrowing with a cast. `byte` → `char` needs `(char)`. `int` → `float` can change the value; `(byte) 128` wraps.

> [!warning] “Larger type” is not the test, and a cast is not a round or a clamp
> `byte` → `char` needs a cast. `int` → `float` is widening and can still round. `(byte) 280` is `24`, not `127`. `(float) 1e100` is `Infinity`; `1e100f` as a literal is a compile-time error. Out-of-range narrowing compiles once the cast is written — it does not throw. `128` as a `byte` without a cast does not compile ([[Why does assigning 128 to a byte without a cast fail to compile]]).

> [!tip] Interview answer
> **Widening is automatic on assignment (`byte` to `double`); narrowing needs a cast and can lose data without throwing.** The ladder is `byte`/`short`/`char` → `int` → `long` → `float` → `double`, with `char` unsigned. `byte` to `char` is a special both-ways conversion. `boolean` does not participate.
