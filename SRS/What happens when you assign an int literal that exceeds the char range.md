<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A numeric value may be assigned to `char` when it is in 0..65535. A dump marks `char ch1 = 66000;` as a compiler error. In-range examples such as `char a = 97;` (`'a'`) and `char letterB = 66;` are accepted.
> [!warning] Unverified traps from the dump
> - char is unsigned 16-bit; 66000 is above Character.MAX_VALUE.
> - A non-constant int still needs an explicit (char) cast even if it would fit.
