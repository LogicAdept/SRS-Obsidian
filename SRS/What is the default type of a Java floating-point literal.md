<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/FloatingPoint #SRS

# What is the default type of a Java floating-point literal?

> [!abstract] Short answer
> **`double`.** A floating-point literal is `float` only if it ends with `F` or `f`. Otherwise it is `double`, and you may write an optional `D` or `d`. `3.14`, `1e1`, `2.`, and `.3` are all `double`. `float x = 3.14;` does not compile: assignment will not narrow `double` to `float`.

## Unsuffixed means `double`

The type is on the token, not on the variable you assign into. `F`/`f` selects IEEE binary32 (`float`). Missing suffix, or `D`/`d`, selects IEEE binary64 (`double`). A decimal floating-point token needs at least one digit and a decimal point, an exponent (`e`/`E`), or a type suffix — so `1e1` is already a floating-point literal (and therefore `double`) even without a dot. Hexadecimal floating-point (`0x1.0p3`) follows the same suffix rule; the `p`/`P` exponent is required. [[How do numeric suffixes and bases work for Java literals]] is the full suffix/radix table; [[What is the difference between float and double in Java]] is the two primitive types.

```d2
direction: down
tok: "floating-point token\n3.14  1e1  2.  0x1.0p3" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
f: "suffix F or f → float" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
d: "no suffix, or D / d → double" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}

tok -> f
tok -> d
```

**Fig. 1.** Default is `double`. `D`/`d` is optional sugar, not a change of default.

Assignment allows widening `float` → `double`, not the reverse. There is **no** “fits in `float`” exception the way a small constant `int` may assign to `byte`. Write `3.14f` or `(float) 3.14`. `Float.valueOf` likewise wants a `float` (or a `String`); `Float.valueOf(3.14)` does not compile. [[How would you explain widening and narrowing casts between Java primitive types]] is that conversion; [[What are the autoboxing rules when assigning a primitive to a wrapper]] is why `Float f = 3.14;` fails for the same reason (`double` does not box to `Float`).

```java
public final class FloatingLiteralDefault {
    public static void main(String[] args) {
        double a = 3.14;          // unsuffixed → double
        double b = 1e1;           // exponent form, still double
        double c = 2.;            // double
        double d = 3.14d;         // explicit double
        float e = 3.14f;
        float f = (float) 3.14;   // narrowing cast
        // float g = 3.14;        // does not compile: double → float
        // Float boxed = 3.14;    // does not compile: no double → Float
        System.out.println(a);
        System.out.println(b);
        System.out.println(c);
        System.out.println(d);
        System.out.println(e);
        System.out.println(f);
    }
}
```

**Listing 1.** Unsuffixed and `d` are `double`. A `float` variable needs `f` or a cast. Integer `3` is not a floating-point literal at all (`int`).

> [!warning] `3.14` is not “a float because it has a dot”
> The dot (or `e`) makes it a **floating-point** literal; the missing suffix makes that literal a **`double`**. `1e1` is `double` `10.0`, not `int` `10`. `float x = 3.14;` is a compile error, not a silent truncation.

> [!tip] Interview answer
> Java floating-point literals default to `double`. I write `f` or `F` for `float`; `d` or `D` is optional on a `double`. That is why `float x = 3.14;` does not compile and `3.14f` does. The default is the opposite of integer literals, which default to `int` unless you add `L`.
