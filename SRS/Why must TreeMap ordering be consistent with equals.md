<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/HashCodeEquals #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: the `Map` contract is defined in terms of **`equals`**, but `TreeMap` compares keys with **`compareTo` / `compare`**. If that order is **not consistent with `equals`**, the map **fails to obey the general `Map` contract**.

Use TreeMap when you need sorted keys (natural or `Comparator`), and keep `compareTo`/`compare` consistent with `equals`.

> [!warning] Unverified traps from the dump
> - Two keys with `compare == 0` are the same key to the tree even if `equals` is false (or the reverse).
> - This is the same warning dumps give for `SortedMap` / `TreeSet`.
