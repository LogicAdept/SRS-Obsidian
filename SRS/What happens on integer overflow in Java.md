<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Integer arithmetic wraps around silently using two's-complement — no exception is thrown. Exceeding `Integer.MAX_VALUE` rolls over to `Integer.MIN_VALUE`.

```java
int max = Integer.MAX_VALUE;   // 2_147_483_647
System.out.println(max + 1);   // -2147483648  (wraps, no error)

int minValue = Integer.MIN_VALUE; // -2147483648
int underflow = minValue - 1;     // Wraps around to 2147483647
```

A common bug: the overflow happens in `int` math before the result is stored in a `long`.

```java
long bad = 1_000_000 * 1_000_000;        // -727379968
long good = 1_000_000L * 1_000_000;      // 1000000000000 (promote first)
```

Mitigations claimed by dumps: promote to `long`, use `Math.addExact` / `multiplyExact` (throw `ArithmeticException` on overflow), or `BigInteger` for unbounded math.

> [!warning] Unverified traps from the dump
> - Java does not throw on ordinary `int`/`long` overflow; the value wraps.
> - `int * int` overflows before assignment to `long` unless a literal or operand is already `long`.
> - Dumps also mention underflow as wrap from `MIN_VALUE` to `MAX_VALUE`.
