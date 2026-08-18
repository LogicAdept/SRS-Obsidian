<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **no**. `EnumMap` is not synchronized. For concurrent use, wrap it with `Collections.synchronizedMap`, and do that **at creation** so nothing else keeps an unsynchronized reference.

> [!warning] Unverified traps from the dump
> - Same story as most `java.util` maps: not a concurrent map; wrapping is external synchronization, not `ConcurrentHashMap` semantics.
