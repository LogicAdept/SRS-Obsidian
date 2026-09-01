<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/NumericPromotion #SRS

# Why does multiplying two `int` values overflow before assignment to a `long`?

> [!abstract] Short answer
> `*` is typed from its **operands**, not from the variable you store into. Two `int`s multiply as `int`; if the mathematical product does not fit, Java keeps the **low 32 bits** (silent wrap) and only then widens that wrapped value to `long`. `long bad = 1_000_000 * 1_000_000;` is **-727379968**. Write `1_000_000L * 1_000_000` or `(long) a * b` so promotion happens **before** the multiply.

## The `long` box does not change `int * int`

Binary numeric promotion on two `int`s yields `int`. Integer `*` never throws; overflow is the low-order bits of the two’s-complement product, and the sign can flip. Assignment then widens that already-wrong `int` to `long` — a widening that cannot restore lost high bits. `(long)(a * b)` is the same bug with a cast around the **product**. [[How does numeric promotion work in Java arithmetic expressions]] is why the destination is ignored; [[What happens on integer overflow in Java]] is wrap vs `Math.multiplyExact`; [[How do numeric suffixes and bases work for Java literals]] is the `L` that makes a `long` operand.

```d2
direction: down
mul: "int * int" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
wrap: "32-bit wrap\n1_000_000 * 1_000_000\n→ -727379968" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
assign: "store in long\nstill -727379968L" {
  width: 260
  height: 70
  style.fill: "#fff8e1"
}
fix: "long * int\n1_000_000L * 1_000_000\n→ 1000000000000" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}

mul -> wrap
wrap -> assign
mul -> fix
```

**Fig. 1.** Widen an **operand**, not the finished `int` product.

`+` is left-associative: `1_000_000 * 1_000_000 * 1L` still overflows, then multiplies the wrapped `int` by `1L`. Put the `L` (or a `long` cast) on the **first** multiply: `1L * 1_000_000 * 1_000_000`. Two `int` **variables** need `(long) a * b`, not `a * (long) b` only if you remember both orders — casting **either** operand before `*` is enough. `Math.multiplyExact(a, b)` throws `ArithmeticException` instead of wrapping; `Math.multiplyExact((long) a, b)` checks the 64-bit product. 10¹² fits in `long` (±2⁶³); it does not fit in `int` (±2³¹). [[What is the value range of the Java int type]] vs [[What is the value range of the Java long type]]; [[Why does integer division of 5 by 2 equal 2 in Java]] is the same “`/`/`*` type is the operands.”

```java
public final class IntMulOverflowsBeforeLong {
    public static void main(String[] args) {
        long bad = 1_000_000 * 1_000_000;     // -727379968
        long good = 1_000_000L * 1_000_000;   // 1000000000000
        long tooLate = (long) (1_000_000 * 1_000_000); // still wrapped
        long stillBad = 1_000_000 * 1_000_000 * 1L;    // wrap, then * 1L
        long leftGood = 1L * 1_000_000 * 1_000_000;

        int a = 1_000_000, b = 1_000_000;
        long fromVars = (long) a * b;

        System.out.println(bad);
        System.out.println(good);
        System.out.println(tooLate);
        System.out.println(stillBad);
        System.out.println(leftGood);
        System.out.println(fromVars);
        // Math.multiplyExact(a, b); // ArithmeticException
    }
}
```

**Listing 1.** The `long` variable is too late. An `L` (or a `long` cast) must sit on an **operand** of the overflowing `*`. Left-associative `* 1L` at the end does not save the first multiply.

> [!warning] A `long` local is not a 64-bit multiply
> `long n = 1_000_000; n = n * 1_000_000;` is fine (`long * int` promotes). `n = 1_000_000 * 1_000_000;` is not — the right-hand side is still `int * int`. Compound `n *= 1_000_000` is safe once `n` is already `long`.

> [!tip] Interview answer
> Two `int`s multiply as `int` even when you assign to `long`, so a product past about two billion wraps with no exception. Cast or suffix `L` on an operand *before* `*`. Putting `L` only on the assignment, or wrapping `(long)(a * b)`, leaves the overflow in place.
