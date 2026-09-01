<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Explicit narrowing keeps only the bits that fit. A dump example:

```java
int bigValue = 280;
byte small = (byte) bigValue;
System.out.println(small); // 24. Only 8 bits remain.
```

280 is 256 + 24; the high bits are discarded. No rounding and no exception.
> [!warning] Unverified traps from the dump
> - Narrowing a value that does not fit is silent wrap, not a runtime error.
> - The same bit truncation applies to other integral narrowings (int to short, long to int).
