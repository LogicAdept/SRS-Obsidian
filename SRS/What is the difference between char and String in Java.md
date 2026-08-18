<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/String #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The `char` data type represents a single 16-bit Unicode character. Characters are enclosed in single quotes, e.g. `'A'`. You can compare `char` values with relational operators based on their Unicode values.

A `String` is a reference type representing a sequence of characters, enclosed in double quotes. Memory depends on length plus object overhead. Compare strings with `equals` / `compareTo`, not `==`.

`char` stores one character; `String` stores many.

> [!warning] Unverified traps from the dump
> - `'A'` is `char`; `"A"` is `String`.
> - Dumps still describe `char` as one Unicode character; supplementary-plane characters may need two `char` units (see related char/int dumps).
