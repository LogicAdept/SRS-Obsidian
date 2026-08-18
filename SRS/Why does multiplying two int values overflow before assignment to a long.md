<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Integer arithmetic wraps silently. A dump shows this common bug: overflow happens in `int` before the result is assigned to `long`.

```java
long bad = 1_000_000 * 1_000_000;        // -727379968
long good = 1_000_000L * 1_000_000;      // 1000000000000 (promote first)
```

> [!warning] Unverified traps from the dump
> - The type of `*` is determined by the operands, not by the variable you assign into.
> - Promote at least one operand to `long` before multiplying.
