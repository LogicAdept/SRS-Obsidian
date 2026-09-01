<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/Conversions #SRS

# Can a `byte` be assigned to a `double` without a cast in Java?

> [!abstract] Short answer
> **Yes.** `byte` → `double` is a **widening primitive conversion**. Assignment conversion applies that conversion automatically, so `double d = b;` compiles with no cast. Every `byte` value (−128…127) becomes the **same numeric value** as a `double`.

## Widening in assignment, not a cast

A cast is the `(T)` operator. Assignment does not need one when the conversion is **widening**. From `byte`, widening targets are `short`, `int`, `long`, `float`, and `double`. The same widening is allowed when you pass a `byte` argument to a `double` parameter.

The reverse — `double` → `byte` — is a **narrowing** conversion. Assignment does not apply general narrowing. `byte b = d;` is a compile-time error; you write `(byte) d`. That cast may drop the fraction, change magnitude, and wrap the low 8 bits of the integer result. It still does not throw. See [[Can a double be cast to a byte in Java]] and [[How would you explain widening and narrowing casts between Java primitive types]].

```d2
direction: right
b: "byte" {
  width: 100
  height: 50
  style.fill: "#e3f2fd"
}
d: "double" {
  width: 110
  height: 50
  style.fill: "#e8f5e9"
}
back: "needs (byte)" {
  width: 140
  height: 50
  style.fill: "#ffebee"
}

b -> d: "assignment, no cast"
d -> back: "narrowing"
```

**Fig. 1.** Assignment widens `byte` to `double`. Going back is a cast, and it is lossy.

Exact preservation here is specific to this pair (and to `byte`/`short`/`char` → `float`/`double`). Widening does **not** mean “always lossless”: `int` → `float` and `long` → `double` may round. `byte` → `char` is not a widening conversion at all — it needs a cast even though both are 16 bits or fewer.

`byte b = 1;` is a different rule: the literal `1` is `int`, and a **constant** that fits may narrow into `byte` without a cast. That is not why `double d = b` works. [[What is the value range of the Java byte type]] is the −128…127 box that `1` fits; [[Why does assigning 128 to a byte without a cast fail to compile]] is the constant that does not.

```java
public final class ByteToDoubleAssign {
    public static void main(String[] args) {
        byte b = 1;
        double d = b;                 // 1.0 — widening, no cast
        System.out.println(d);

        byte min = -128;
        double exact = min;           // -128.0 — value preserved
        System.out.println(exact);

        // byte lost = d;             // compile error: narrowing
        byte truncated = (byte) 99.9; // 99 — fraction discarded
        System.out.println(truncated);

        Byte boxed = b;
        double fromWrapper = boxed;   // unbox byte, then widen
        System.out.println(fromWrapper);
        // Double asDouble = b;       // compile error: no byte → Double
    }
}
```

**Listing 1.** Primitive assignment widens (`1.0`, `-128.0`). The wrapper `Byte` can unbox into `double`; a `byte` cannot be assigned to `Double`.

> [!warning] “Wider type” is not the test, and `Double` is not `double`
> `byte` → `char` needs a cast. `double` → `byte` needs a cast and can wrap. `Double asDouble = b;` does not compile: boxing a `byte` yields `Byte`, not `Double`, and assignment will not widen the primitive and then box. `double d = boxedByte;` does compile (unbox, then widen). Arithmetic is a third story: `byte + byte` is `int` ([[How does numeric promotion work in Java arithmetic expressions]]), which is not assignment conversion.

> [!tip] Interview answer
> **Yes — `double d = b` is a widening primitive conversion, so no cast.** The numeric value is preserved for every `byte`. The reverse is narrowing: you need `(byte)`, it can lose the fraction and wrap, and it still compiles once the cast is there. Do not treat “bigger type” as the rule, and do not confuse `double` with `Double`.
