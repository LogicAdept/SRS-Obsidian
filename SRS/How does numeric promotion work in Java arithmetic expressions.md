<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

In arithmetic, operands smaller than `int` (`byte`, `short`, `char`) are first promoted to `int`, and if any operand is `long`/`float`/`double` the whole expression is promoted to the widest type. This is why byte arithmetic returns an `int`.

```java
byte a = 10, b = 20;
byte c = a + b;        // won't compile — a + b is int
byte d = (byte)(a + b); // cast back

int i = 5;
double e = i / 2;      // 2.0 — int division happens FIRST, then widens
double f = i / 2.0;    // 2.5 — one double operand promotes the division
```

The `5 / 2 == 2` integer-division surprise is the most common version of this in interviews.

> [!warning] Unverified traps from the dump
> - `byte + byte` is `int`, so assignment back to `byte` needs a cast.
> - Integer division truncates toward zero before any widening to `double`.
