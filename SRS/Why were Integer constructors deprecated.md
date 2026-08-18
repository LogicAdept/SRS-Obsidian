<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A dump: `new Integer()` is deprecated since Java 9 and removed in Java 17. It always allocates a new object and bypasses the cache. Prefer `Integer.valueOf` (autoboxing uses that). For strings, `parseInt` vs `valueOf`.

Older dumps still compile examples with `new Integer(55)` and `new Integer("55")`.

> [!warning] Unverified traps from the dump
> - Confirm whether constructors are merely deprecated or actually removed on the JDK you use.
> - `new` never participates in `IntegerCache`.
