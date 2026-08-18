<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The `long` data type is a 64-bit signed integer, used for larger numerical values. A long literal is denoted by appending `L` or `l`, e.g. `long num = 123456789L`. Dumps give the range `-2^63` to `2^63 - 1`.

> [!warning] Unverified traps from the dump
> - Unsuffixed integer literals are still `int`; a value past `int` range needs `L`.
