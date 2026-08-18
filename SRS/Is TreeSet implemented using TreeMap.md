<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Set #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **yes.** `HashSet` uses a `HashMap` internally; **`TreeSet` uses a `TreeMap` (red-black tree)** internally. Elements are the map keys; uniqueness and sort order come from that tree (`compareTo` / `Comparator`, O(log n), no null element).

> [!warning] Unverified traps from the dump
> - This is the same dummy-value pattern dumps describe for `HashSet` on `HashMap`.
> - Prefer `EnumSet` when the elements are one enum type; that is not a `TreeMap`.
