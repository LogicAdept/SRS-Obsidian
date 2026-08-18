<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`float` and `double` are binary IEEE-754 floating point. Many decimal fractions (like `0.1`) have no exact binary representation, so they are stored as the nearest approximation and tiny errors accumulate.

```java
System.out.println(0.1 + 0.2);   // 0.30000000000000004
System.out.println(0.1 + 0.2 == 0.3); // false
```

For money or anything needing exact decimals, dumps say use `BigDecimal` (and construct it from a String, not a double):

```java
new BigDecimal("0.1").add(new BigDecimal("0.2")); // 0.3 exactly
```

Never compare floats with `==`; compare within a small epsilon instead.

> [!warning] Unverified traps from the dump
> - `0.1 + 0.2 == 0.3` is false for `double`.
> - `new BigDecimal(0.1)` is not the same as `new BigDecimal("0.1")` because the double is already rounded.
