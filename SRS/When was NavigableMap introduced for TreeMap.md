<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A collections interview dump: `TreeMap` is internally a red-black tree and **`NavigableMap`, introduced in JDK 6**. The red-black tree keeps the order from `Comparable` or a constructor `Comparator`.

> [!warning] Unverified traps from the dump
> - `TreeMap` itself is older than JDK 6; dumps attach **JDK 6** to the `NavigableMap` interface, not to the first appearance of `TreeMap`.
