<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# Why does the Java `int` type have a fixed size?

> [!abstract] Short answer
> The language **defines** `int` as a **32-bit** signed two’s-complement type, not as “the machine word.” Every implementation uses the same width so the same source has the same range and the same overflow on every JVM — including a 64-bit one. `Integer.SIZE` is 32 and `Integer.BYTES` is 4. The 64-bit integer primitive is `long`, not a wider `int`.

## Specified 32 bits, not native word size

Primitive types are predefined. `int` values are 32-bit signed two’s-complement integers: −2147483648 … 2147483647. That width is part of the type, the same way `byte` is 8 bits and `long` is 64. A 64-bit OS or HotSpot build does not change `int`; it still occupies the 32-bit box and still wraps at 2³¹−1. [[What is the value range of the Java int type]] is that box; [[What is the value range of the Java long type]] is the 64-bit one; [[Why do Java primitive types have bounded numeric ranges]] is why all numeric primitives are finite.

```d2
direction: down
lang: "int = 32-bit two's-complement\nsame on every JVM" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
vm: "computational type int\niadd / imul / …" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
not: "not CPU word size\nlong is the 64-bit integer" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}

lang -> vm
lang -> not
```

**Fig. 1.** Fixed size is the spec. Hardware word width is not `int`.

The JVM matches that definition: `int` values are 32-bit signed two’s-complement. Arithmetic instructions are typed (`iadd` vs `ladd`). `int` is a **computational type**; `byte`, `short`, `char`, and `boolean` load as `int` on the operand stack, so everyday integer math is 32-bit even when the variable is narrower. There is no “word-sized `int`” opcode. [[Where is the authoritative reference for Java primitive types]] names Primitive Types and Values for the language widths.

```java
public final class FixedIntSize {
    public static void main(String[] args) {
        System.out.println(Integer.SIZE);   // 32 — bits, not host word
        System.out.println(Integer.BYTES);  // 4
        System.out.println(Long.SIZE);      // 64 — separate type

        int wrap = Integer.MAX_VALUE + 1;   // still 32-bit add
        long n = Integer.MAX_VALUE * 2;     // int * int, then widen
        System.out.println(wrap);           // Integer.MIN_VALUE
        System.out.println(n);              // wrapped int, stored in long
    }
}
```

**Listing 1.** `Integer.SIZE` is 32 on every platform. A `long` variable does not make `*` a 64-bit multiply.

Because the width is fixed, overflow is wrap of 32 bits, not “grow to the register.” `1_000_000 * 1_000_000` is an `int` product. Use `L`, a `long` operand, or `Math.multiplyExact` when 32 bits is the constraint. [[What happens on integer overflow in Java]] and [[Why does multiplying two int values overflow before assignment to a long]] are that wrap.

> [!warning] 64-bit JVM ≠ 64-bit `int`
> Pointers and object headers may be 64-bit; `int` is still 32. Do not size counters or IDs from “this is a 64-bit machine.” Do not assume `long n = a * b` widens before the multiply.

> [!tip] Interview answer
> `int` is 32-bit by specification so a program’s arithmetic is the same on every JVM, not whatever the CPU’s word is. `Integer.SIZE` is 32 even on a 64-bit runtime; `long` is the 64-bit integer type. Overflow wraps in those 32 bits unless you change the type of the operation.
