<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list shifts on integer primitives: `<<` left shift, `>>` right shift (sign-preserving / arithmetic), `>>>` right shift without regard to sign (zero-fill / logical).

```java
1 << 4   // 16
-8 >> 1  // -4  (sign-preserving)
-8 >>> 28 // 15 (zero-filled — treats bits as unsigned)
```

`>>>` is called out as Java-specific among languages without unsigned integer types: it is the shift that ignores the sign bit.

> [!warning] Unverified traps from the dump
> - `>>` keeps the sign bit; `>>>` fills with zeros.
> - Shift operands are integers; dumps describe `>>` as dividing by powers of two.
