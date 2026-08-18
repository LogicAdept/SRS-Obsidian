<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The `int` data type in Java is a 32-bit signed integer, 4 bytes. Dumps give the range `-2^31` to `2^31 - 1` (about `-2.1` billion to `2.1` billion), i.e. `Integer.MIN_VALUE` … `Integer.MAX_VALUE`.

> [!warning] Unverified traps from the dump
> - This is the type range, not the range of `hashCode()` answers.
