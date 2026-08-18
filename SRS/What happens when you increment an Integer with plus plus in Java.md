<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps show that autoboxing makes `Integer ten = new Integer(10); ten++;` legal: Java unboxes, increments the primitive, and boxes the result. The increment is not a field mutation of the original `Integer` object (wrappers are described as immutable).

> [!warning] Unverified traps from the dump
> - `++` on a wrapper allocates a new boxed value (and may hit the integer cache for small results).
> - Older dumps still use `new Integer(...)`, which is a separate identity from boxed literals.
