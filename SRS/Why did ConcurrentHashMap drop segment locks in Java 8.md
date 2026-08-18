<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Versions/8 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump Q: why did Java 8 `ConcurrentHashMap` abandon segment locks, what was wrong, how would you design it?

Dump A: it dropped the `Segment` (lock-stripe) idea and uses a **new** approach with the **CAS** algorithm. **Segment-lock performance was not high**, and **CAS is a CPU atomic**.

A longer dump: Java 8 looks like an optimized thread-safe `HashMap`: **Node array + list/tree**, concurrency with **`synchronized` and CAS**. JDK 6+ `synchronized` optimizations are the reason they switched from `ReentrantLock`. Red-black trees keep lookup **O(log n)**.

> [!warning] Unverified traps from the dump
> - “CAS instead of segments” is incomplete: the same dumps still lock a bin with `synchronized` when CAS is not enough.
> - “If you were to design it” in the title is not answered beyond “use CAS.”
