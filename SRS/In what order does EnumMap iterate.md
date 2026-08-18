<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `EnumMap` is ordered by the **natural order of the keys**, meaning the order enum constants are **declared**, not the order of `put`.

Dump example: put `RUNNING`, `WAITING`, `NEW`, `FINISHED`; printing / iterating still yields `NEW`, `RUNNING`, `WAITING`, `FINISHED`.

> [!warning] Unverified traps from the dump
> - Reordering constants in the enum type changes iteration order.
> - This is not insertion order (`LinkedHashMap`) and not a `Comparator` (`TreeMap`).
