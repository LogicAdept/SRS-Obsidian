<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/HashCodeEquals #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Harp-style dump: `HashMap` compares keys with **`equals()`**; `TreeMap` compares with **`compareTo()`**. Duplicate `put` of the same key **replaces the value**.

Search does not use `hashCode`.

> [!warning] Unverified traps from the dump
> - “Same key” for the tree means `compareTo`/`compare` returns 0, not necessarily `equals`.
> - Dumps that say HashMap tree-bins are “structured similarly to TreeMap” are talking about **bucket** trees after Java 8, not that `HashMap` became a `TreeMap`.
