<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **no.** `Hashtable` is **internally synchronized and cannot be unsynchronized.** You *can* make a `HashMap` synchronized with `Collections.synchronizedMap(hashMap)`.

> [!warning] Unverified traps from the dump
> - “Cannot unsynchronize” means there is no unsynchronized mode of the same class, not that you cannot wrap a different map.
> - The concurrent-map dump still contrasts whole-table `synchronized` with `ConcurrentHashMap` retrievals that do not lock.
