<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #Java/JVM/Memory #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `WeakHashMap` is a **hash table** `Map` with **weak keys**. An entry is **automatically removed** when its key is no longer in ordinary use. **Null key and null values** are supported. Performance is described as similar to `HashMap`, with the same **initial capacity** and **load factor** knobs.

A dump of the four Java reference kinds: if an object is reachable **only** through `WeakReference`s (no strong or soft refs), it is marked for collection. `WeakHashMap` stores keys in `WeakReference`s, so the pair is removed when the key has **no strong references**.

> [!warning] Unverified traps from the dump
> - “No longer in ordinary use” is dump wording, not a `System.gc()` contract.
> - One dump contrasts only strong refs; another also says a **soft** ref to the key still lets you look the value up.
