<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/FloatingPoint #SRS

# What does the Java strictfp modifier do?

> [!abstract] Short answer
> **Nothing, on Java 17 and later.** `strictfp` used to force IEEE 754 **binary32 / binary64** evaluation of enclosed `float` and `double` expressions (no extra exponent range). Since Java 17 every floating-point expression is already strict, so the modifier is **obsolete**: still a legal keyword on classes, interfaces, and methods, with **no compile-time or run-time effect**.

## What it used to lock down

Java 1.0–1.1 required **strict** floating-point: each `float` value is a binary32, each `double` a binary64, and matching IEEE operators produce the IEEE result ([[What is the difference between float and double in Java]]).

From Java 1.2 through 16, a JVM was allowed to use an **extended-exponent** value set for non-`strictfp` code (same significand width, wider exponents — historically cheap on x87). Intermediate overflow or underflow could then differ from a pure binary32/binary64 machine. Putting `strictfp` on a **class**, **interface**, or **method** forbade that for enclosed expressions, restoring 1.0/1.1 predictability.

Java 17 restored always-strict evaluation. `strictfp` remains a keyword with the old placement rules, but compilers are encouraged to warn that it is obsolete. It may be redefined or removed later.

It never changed `float` vs `double`, never added extra mantissa bits, and never applied to constructors, fields, or local variables ([[How do you convert a double to a float in Java]]).

```d2
direction: down
old: "Java 1.2–16\nstrictfp = lock IEEE formats" {
  width: 280
  height: 70
}
now: "Java 17+\nalways strict; modifier is a no-op" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

old -> now: "since Java 17"
```

**Fig. 1.** The modifier was an exponent-range lock. Today all FP is already that lock.

```java
public strictfp class StrictFpDemo {
    public strictfp double tenth(double x) {
        return x * 0.1;            // same as without strictfp (Java 17+)
    }

    public static void main(String[] args) {
        System.out.println(new StrictFpDemo().tenth(1.0));
    }

    // public strictfp StrictFpDemo() {}  // constructors cannot be strictfp
    // abstract strictfp void g();        // abstract cannot be strictfp
    // native strictfp void h();          // native cannot be strictfp
}
```

**Listing 1.** Legal `strictfp` on a class and a method. Illegal on constructors, `abstract`, and `native`. Behavior matches dropping the modifier.

> [!warning] It is not “more precise `double`”
> `strictfp` never turned `float` into `double` and never added significand bits. It only forbade **wider exponents** on intermediates. On current Java it does not change results at all. You cannot mark a constructor `strictfp`; mark the class instead — and even that is a no-op now.

> [!tip] Interview answer
> **Obsolete no-op since Java 17.** Historically it forced IEEE 754 `float`/`double` formats so x87-style extra exponent range could not leak into results. Today all floating-point is already strict; keep the keyword off new code.
