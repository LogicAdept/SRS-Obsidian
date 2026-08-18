<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Operands smaller than `int` (`byte`, `short`, `char`) are promoted to `int` in arithmetic. `a + b` for two `byte` values is therefore an `int`, and assigning that `int` to a `byte` is a narrowing conversion that the compiler rejects without an explicit cast.

```java
byte a = 10, b = 20;
byte c = a + b;         // compile error
byte d = (byte)(a + b); // allowed; may overflow the byte range
```

> [!warning] Unverified traps from the dump
> - This is numeric promotion, not a special `byte` bug.
> - The cast can silently wrap if the `int` sum does not fit in `byte`.
