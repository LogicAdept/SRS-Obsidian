<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #Java/JVM/Memory #Java/JVM/GarbageCollector #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump example: put two keys into a `WeakHashMap`, then **`key1 = null` and `System.gc()`**. Iteration afterward prints **only** the key that still has a live local variable (`INACTIVE`). The entry whose last ordinary reference was cleared is gone.

> [!warning] Unverified traps from the dump
> - The dump presents `System.gc()` as producing that output. GC need not run, and need not collect immediately.
> - `final Key key2` in the sample stays reachable; that is why that mapping survives, not because `WeakHashMap` treats some keys as strong.
