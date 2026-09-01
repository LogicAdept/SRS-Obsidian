<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use an explicit cast. A dump example: `double num = 3.14159; float floatValue = (float) num;` The conversion may lose precision. Unsuffixed decimal literals are `double`, so assigning them to `float` without a cast or an `f`/`F` suffix is a compile error.
> [!warning] Unverified traps from the dump
> - float avg = 36.01 does not compile; 36.01f or (float) 36.01 does.
> - A double magnitude too large for float becomes Infinity rather than a compile error at runtime.
