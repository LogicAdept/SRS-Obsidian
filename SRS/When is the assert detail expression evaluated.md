<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

For `assert(b) : e;` dumps: **`e` is evaluated if and only if `b` is false**. If `b` is true, `e` is not evaluated.

Example: `x == 10` and `assert(x == 10) : ++x;` — with `-ea`, `x` stays `10` because the condition is true.

> [!warning] Unverified traps from the dump
> - With assertions off, dumps say the assert is not executed, so a detail expression that mutates state would not run either.
> - Putting `++x` in the detail is a teaching example, not recommended style.
