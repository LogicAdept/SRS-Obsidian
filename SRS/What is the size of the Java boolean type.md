<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview dumps disagree on `boolean` width. Cheat-sheet tables often list it as 1 bit. Other dumps say the size is unknown, JVM-dependent, or “usually 1 byte”. The language only defines the two values `true` and `false`; it does not fix a storage size the way it does for `byte`/`short`/`int`/`long`/`float`/`double`/`char`.
> [!warning] Unverified traps from the dump
> - A table that says 1 bit is not a JLS guarantee of 1-bit fields or packed arrays.
> - HotSpot typically stores a boolean field or boolean[] element in a byte, not a bit.
> - A local boolean may occupy a 32-bit operand-stack / local slot in bytecode.
