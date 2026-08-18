<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Caching #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: use **LRU** with `LinkedHashMap` in **access-order**. Access moves the entry to the **end**; least-used entries gather at the **start**. Override `removeEldestEntry` (the dump names `removeEldestEntries`) so `put` / `putAll` can drop the eldest when the cache should shrink.

The same dump then says `LinkedHashMap` **cannot fully implement LRU**, because inserting a key that is **already in the map does not change iteration order**.

> [!warning] Unverified traps from the dump
> - The dump’s own method name is `removeEldestEntries`; other lists say `removeEldestEntry`.
> - The “cannot fully implement LRU” sentence is the insertion-order re-`put` rule, colliding with the same dump’s access-order story.
> - Access-order plus `removeEldestEntry` is the usual interview LRU recipe; the dump still flags a hole on re-insert.
