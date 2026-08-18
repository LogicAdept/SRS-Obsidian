<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps say primitives store the raw value and cannot be `null`; wrappers are heap objects with identity and overhead, needed for generics, collections, and nullable fields. Autoboxing in a tight loop creates throwaway objects and GC pressure. Classic trap: `Integer sum = 0; for (...) sum += x;` vs a primitive `int` accumulator.

Operations with primitive types are described as faster than with class objects.

> [!warning] Unverified traps from the dump
> - Use wrappers when the API requires an object (`List<Integer>`, nullable fields).
> - Unboxing `null` in a loop is an NPE, not a slow path.
