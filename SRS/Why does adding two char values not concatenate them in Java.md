<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`char` is numeric. `'a' + 'b'` adds code points (`97 + 98`), so the dump prints `195`, not `"ab"`. Concatenation needs a `String` context such as `"" + 'a' + 'b'`.

> [!warning] Unverified traps from the dump
> - `char + char` promotes to `int` addition.
> - `String` concatenation is a different `+` overload involving `String`.
