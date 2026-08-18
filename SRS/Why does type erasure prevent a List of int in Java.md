<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Generics #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A dump: Java does generics using type-erasure of reference types. For example a `List` is really a `List` of objects/references at run time. Primitives are not reference types, so generic collections cannot store `int` directly. Wrappers (`Integer`) are references, so `List<Integer>` is legal and autoboxing fills it.

> [!warning] Unverified traps from the dump
> - This is the same type-erasure story as “no `List<int>`,” not a special `ArrayList` limitation.
