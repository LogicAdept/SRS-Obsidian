<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Floating-point literals without a suffix are treated as `double` by default. For example, `3.14` is a `double`. To specify a `float` literal, append `f` or `F`, for example `3.14f`.

`d`/`D` can mark a `double` explicitly.

> [!warning] Unverified traps from the dump
> - `float x = 3.14;` does not compile without a cast or `f`.
