<!--
reps: 0
priority: 0
-->
#Java/Collections/List #Java/Collections/Set #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **`Set` — unique things only.** Does not allow duplication; if two objects are equal, only one can be in the set. **`List`** is ordered and may contain duplicates; it has positional access.

Related dump: `Set` has no index. Membership is `contains`. Duplicate means `equals` (and `hashCode` for hash sets, or `compareTo` / `Comparator` for sorted sets), not reference identity.

> [!warning] Unverified traps from the dump
> - `LinkedHashSet` is still a Set: unique, insertion-ordered — not a List.
> - Fast membership is the Set story; a List `contains` scan is O(n) in another dump.
