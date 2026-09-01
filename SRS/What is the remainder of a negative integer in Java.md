<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The `%` operator yields the remainder of integer division. A dump prints `10 % 4` as 2, `15 % 4` as 3, and `-15 % 4` as -3 — the result takes the sign of the dividend.
> [!warning] Unverified traps from the dump
> - Java remainder is not a always-non-negative mathematical modulo.
> - Do not confuse this with integer division truncation toward zero (5 / 2 == 2).
