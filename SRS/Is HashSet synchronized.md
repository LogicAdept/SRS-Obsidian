<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **HashSet is not synchronized.** Not suitable for thread-safe use unless you synchronize it explicitly.

Same dump: default capacity **16**, load factor **0.75**; no insertion order; hashing; unique elements only; **null allowed**; good for search.

> [!warning] Unverified traps from the dump
> - Explicit wrap is `Collections.synchronizedSet`; concurrent dumps prefer `ConcurrentHashMap.newKeySet()` instead of a locked `HashSet`.
