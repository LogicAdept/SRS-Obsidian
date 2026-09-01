<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Valid boolean literals are only `true` and `false`. Dumps mark `boolean b = TRUE;` and `boolean b = 0;` as compilation errors: this is not C. `TRUE`/`FALSE` are not keywords, and integers are not booleans.
> [!warning] Unverified traps from the dump
> - Boolean.TRUE is a wrapper constant, not a primitive literal.
> - boolean b = 1 is also illegal; there is no integer-to-boolean conversion.
