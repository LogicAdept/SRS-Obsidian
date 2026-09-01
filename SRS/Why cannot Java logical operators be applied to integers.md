<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Operators/Logical #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Short-circuit `&&` / `||` and `!` work only with `boolean`. A dump marks `5 || 6` as a compiler error: logical operators are not C-style “nonzero is true”. Bitwise `|`, `&`, and `^` are the operators that apply to integer primitives.
> [!warning] Unverified traps from the dump
> - boolean & and | exist but they are not short-circuit; they still require boolean operands.
> - Mixing this up with bitwise | on ints is a common C/Java confusion.
