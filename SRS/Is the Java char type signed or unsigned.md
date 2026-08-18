<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps describe `char` as a 16-bit unsigned integer holding a single UTF-16 code unit (`'A'`, `'7'`, `'€'`), range `0` … `65535`. Because it is numeric under the hood, it participates in arithmetic and auto-promotes to `int`.

> [!warning] Unverified traps from the dump
> - Among the integral primitives, dumps single out `char` as unsigned; `byte`/`short`/`int`/`long` are signed.
