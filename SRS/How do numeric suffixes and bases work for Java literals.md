<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Literals default to `int` (integers) and `double` (decimals); suffixes change that: `L`/`l` for `long`, `f`/`F` for `float`, `d`/`D` for `double`. You can also write binary (`0b`), octal (`0`), and hex (`0x`) literals, and use underscores as digit separators for readability.

```java
long big   = 10_000_000_000L;  // L needed — exceeds int range
float rate = 1.5f;
int  mask  = 0xFF;             // 255 in hex
int  bits  = 0b1010;           // 10 in binary
int  million = 1_000_000;      // underscores ignored by the compiler
```

Forgetting the `L` on a large literal is a classic bug: `10_000_000_000` alone won't compile because it overflows `int`.

> [!warning] Unverified traps from the dump
> - Unsuffixed integer literals are `int`; unsuffixed decimals are `double`.
> - A numeric literal larger than `Integer.MAX_VALUE` needs `L` or it is a compile error.
