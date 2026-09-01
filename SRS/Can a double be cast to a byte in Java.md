<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes, with an explicit cast. A higher-precision floating-point value can be converted to `byte`, but it is a lossy narrowing conversion.

```java
double d = 99.9;
byte b = (byte) d;
```

The dump calls this explicit / narrowing casting.
> [!warning] Unverified traps from the dump
> - The conversion can drop the fractional part and then wrap bits that do not fit in 8 bits.
> - There is no compile error once the cast is written, even when the value is out of range.
