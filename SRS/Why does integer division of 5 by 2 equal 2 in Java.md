<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

If both operands are integers, division is integer division and truncates. Widening to `double` after the division does not restore the fraction.

```java
int i = 5;
double e = i / 2;      // 2.0 — int division happens FIRST, then widens
double f = i / 2.0;    // 2.5 — one double operand promotes the division
```

Dumps call `5 / 2 == 2` the most common interview version of numeric promotion / mixed-type arithmetic.

> [!warning] Unverified traps from the dump
> - The result type of `/` follows the operands, not the variable you assign into.
> - Cast or use a `double` operand *before* dividing if you want a fractional result.
