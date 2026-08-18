<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **yes.** Iterators from `IdentityHashMap` (and `HashMap`) are **fail-fast**.

> [!warning] Unverified traps from the dump
> - Fail-fast is not a lock and not `ConcurrentHashMap` weakly-consistent iteration.
> - The dump does not name `ConcurrentModificationException` on this row; it only says fail-fast.
