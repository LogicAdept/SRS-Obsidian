<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Operations on `int`-sized or smaller types produce `int`. So `b = b + 1` for a `byte` (or `short n1 + n2`) is an `int` result and needs an explicit narrowing cast.

Compound assignment is different: `byte b = 5; b += 5;` compiles because the compound operators include an implicit conversion back to the variable's type (the dump's wording: “compiles because of implicit conversion”).
> [!warning] Unverified traps from the dump
> - For byte, short, and char, += is not the same as = ... + ....
> - The hidden cast can silently overflow the byte range.
