<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/EnumSet #Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **no.** `EnumSet` does not allow null. Adding null throws **`NullPointerException`**.

> [!warning] Unverified traps from the dump
> - Contrast with `HashSet`, which dumps say allows one null.
