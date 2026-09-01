<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. A `byte` can be assigned to a `double` without a cast. The dump calls this implicit / widening casting: a lower-precision integer is stored in a wider floating-point type, with no data loss.

```java
byte b = 1;
double d = b;
```
> [!warning] Unverified traps from the dump
> - Widening primitive conversion is automatic; the reverse (double to byte) is not.
