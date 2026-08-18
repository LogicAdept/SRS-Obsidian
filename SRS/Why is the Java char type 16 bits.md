<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps describe `char` as a 16-bit Unicode character so it can hold letters, digits, symbols, and characters from many writing systems. It uses 2 bytes. Characters are written in single quotes.

Related dumps: Java uses Unicode for character representation; `char` holds a UTF-16 code unit, and characters outside the BMP may need two `char`s.

> [!warning] Unverified traps from the dump
> - `char` is not an 8-bit C `char`.
> - Dumps disagree on whether every emoji fits in one `char`.
