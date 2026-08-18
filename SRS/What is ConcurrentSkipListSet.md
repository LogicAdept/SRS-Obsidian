<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Set #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **sorted concurrent set**, counterpart of `ConcurrentSkipListMap`. Use when you need **thread-safety and sorted / range** behavior. If you only need a hash set, dumps prefer `ConcurrentHashMap.newKeySet()` (faster).

Another dump: `ConcurrentSkipListMap` / `ConcurrentSkipListSet` are **sorted concurrent** structures for ordered maps/sets with multi-threaded access.

> [!warning] Unverified traps from the dump
> - Sibling dump calls `ConcurrentSkipListMap` “synchronized” and “fail-safe”; treat that wording as unverified.
