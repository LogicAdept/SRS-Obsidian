<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `TreeMap` implements **`NavigableMap`** (and **`SortedMap`**), plus `Cloneable` and `Serializable`. It is described as a red-black-tree `NavigableMap`.

`HashMap` in the same tables implements `Map`, `Cloneable`, `Serializable` — not `NavigableMap`.

One short interview list also says TreeMap implements NavigableMap, SortedMap, and “indirectly Map, Collection, and Iterable.”

> [!warning] Unverified traps from the dump
> - `Map` does not extend `Collection`; “indirectly Collection / Iterable” is a dump slip.
> - Another dump says TreeMap adds sorting “on top of hashing offered by the Map interface.” `TreeMap` lookup is compare-based, not hashing.
> - `NavigableMap` is the extra surface (`floorKey`, `ceilingKey`, `pollFirstEntry`, range maps) beyond a plain `Map`.
