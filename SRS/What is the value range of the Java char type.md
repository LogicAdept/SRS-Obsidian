<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The `char` data type in Java is a 16-bit Unicode character. Dumps give the range `'\u0000'` (0) to `'\uffff'` (65,535 inclusive).

> [!warning] Unverified traps from the dump
> - `char` cannot hold a negative value in the language model dumps describe.
> - One dump also claims emoji fit in `char`; another says characters beyond the BMP need a surrogate pair.
