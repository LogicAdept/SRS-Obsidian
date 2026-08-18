<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Java/Collections/Map/HashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **no.** `LinkedHashMap` does **not** override `HashMap.put`. It overrides hook methods that `put` calls: `recordAccess`, `addEntry`, and `createEntry`, and those hooks maintain the doubly-linked list.

Entry nodes still have HashMap’s `next` (bucket chain) **and** `before` / `after` (iteration list).

> [!warning] Unverified traps from the dump
> - “Does not override `put`” is an older-hook story (`recordAccess` / `addEntry` / `createEntry`); later JDKs renamed those hooks.
> - Bucket `next` is not the same pointer as iteration `after`.
