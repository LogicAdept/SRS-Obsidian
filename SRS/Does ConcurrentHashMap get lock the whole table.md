<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **no.** `get()` on `ConcurrentHashMap` has **no locks**. `Hashtable` synchronizes **every** operation, including independent reads.

Java 7 dump: `get` is efficient because the **whole process needs no lock**; `volatile` value gives visibility.

> [!warning] Unverified traps from the dump
> - “No locks on get” is not “no memory barriers”; dumps still name `volatile` on the value.
> - `put` in the same dumps still locks a segment or a bin.
