<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Java has two primitive data types to handle floating-point numbers: `float` and `double`. `float` is a 32-bit single-precision type (~7 decimal digits); `double` is a 64-bit double-precision type (~15 decimal digits). By default, floating-point literals are treated as `double` unless explicitly specified as `float` using the `f` or `F` suffix.

Memory: `float` uses 4 bytes, `double` uses 8 bytes. Range: dumps quote about `1.4e-45` to `3.4e38` for `float` and a much larger range for `double`.

Usage claimed by dumps: use `float` when memory conservation is critical; use `double` for most calculations. One dump also claims arithmetic on `float` can be slower than on `double` because modern hardware prefers double-precision.

> [!warning] Unverified traps from the dump
> - A literal like `3.14` is `double`; `3.14f` is `float`.
> - Assigning a `double` literal to `float` needs a cast or `f` suffix.
> - A dump claims `float` math can be slower than `double` on modern CPUs — verify against hardware/JVM behavior.
