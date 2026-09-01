<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/NumericPromotion #SRS

# Why does adding two `byte` values not compile as a `byte` in Java?

> [!abstract] Short answer
> `+` on two `byte` values is an **`int` expression**. Numeric promotion widens every arithmetic operand smaller than `int` (`byte`, `short`, `char`) to `int` first. `byte c = a + b;` is therefore an `int` assigned to a `byte` — a narrowing conversion the compiler rejects. Write `byte c = (byte)(a + b);`. The same rule is not a `byte` bug: `short + short` and `char + char` are `int` too.

## Arithmetic promotes to `int`; assignment does not shrink it back

In a numeric arithmetic context, if neither operand is `double`, `float`, or `long`, the promoted type is `int`. Both `byte`s widen, `+` runs as `int` addition, and the type of the additive expression **is** that promoted type. Storing the result in a `byte` needs an explicit narrowing cast. The cast keeps the low 8 bits; a sum outside −128…127 **wraps** (`(byte)(100 + 100)` is −56). [[How does numeric promotion work in Java arithmetic expressions]] is the full ladder; [[What is the value range of the Java byte type]] is why 200 does not fit; [[What happens on integer overflow in Java]] is wrap, not an exception.

```d2
direction: down
ops: "byte a + byte b" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
prom: "both widen to int\nint + int → int" {
  width: 260
  height: 70
  style.fill: "#fff8e1"
}
fail: "byte c = that int\ncompile-time error" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
ok: "(byte)(a + b)\nnarrow; may wrap" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

ops -> prom
prom -> fail
prom -> ok
```

**Fig. 1.** The sum is `int`. A cast is required to store it in a `byte`.

`byte c = 10 + 20;` **does** compile: `10` and `20` are `int` literals, `30` is a **constant** `int` representable in `byte`, and assignment allows that narrowing. `final byte a = 10, b = 20; byte c = a + b;` is the same idea once `a` and `b` are constant variables. Ordinary variables are not constants, so `a + b` stays a non-constant `int`. Compound assignment hides the cast: `c += a` is `c = (byte)(c + a)`. `++c` also narrows on the way back. [[What is a compile-time constant in Java]] is why literals sneak through; [[Why does multiplying two int values overflow before assignment to a long]] is the sibling “operation type ignores the destination”; [[How does the Java char type relate to int]] is `char` arithmetic in `int`.

```java
public final class BytePlusByte {
    public static void main(String[] args) {
        byte a = 10, b = 20;
        // byte c = a + b;           // does not compile: int → byte
        byte d = (byte)(a + b);      // 30
        byte wrap = (byte)(100 + 100); // -56

        byte lit = 10 + 20;          // OK: constant int 30
        final byte fa = 10, fb = 20;
        byte fromFinals = fa + fb;   // OK: constant expression

        d += a;                      // hidden (byte) cast
        // byte e = a + 1;           // does not compile unless a is constant

        short s = 1, t = 2;
        // short u = s + t;          // same rule: int sum

        System.out.println(d);
        System.out.println(wrap);
        System.out.println(lit);
        System.out.println(fromFinals);
        System.out.println(s + t);   // prints int 3
    }
}
```

**Listing 1.** Variable `byte + byte` needs a cast. Constant sums and `+=` do not look like they need one.

> [!warning] The cast is not a fix for overflow — only for the type
> `(byte)(a + b)` compiles even when the mathematical sum does not fit. Prefer `int` for the sum unless you truly want an 8-bit wrap. `Byte` + `Byte` unboxes, then the same `int` promotion applies; a `null` operand NPEs before the add.

> [!tip] Interview answer
> `byte + byte` is `int` because Java promotes every arithmetic operand smaller than `int` to `int`. Assigning that sum to a `byte` is a narrowing conversion, so you need `(byte)(a + b)`. The same happens for `short` and `char`. A constant like `10 + 20` can still initialize a `byte` because assignment allows narrowing of a representable constant.
