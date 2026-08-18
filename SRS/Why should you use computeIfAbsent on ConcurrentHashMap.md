<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Versions/8 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **`computeIfAbsent` is the atomic “check and insert.”** Do not use `containsKey` + `put` (race). Same dump’s cache example: `ConcurrentHashMap` (not `HashMap` — infinite loop in Java 7, lost updates) and `computeIfAbsent`.

Compilation dumps: `putIfAbsent`, `computeIfAbsent`, `compute`, `merge` run as **one atomic step** with the bin locked. Per-call thread safety is not a transaction: `get` then `put` still races.

> [!warning] Unverified traps from the dump
> - `HashMap.putIfAbsent` in other dumps is **not** a thread-safe substitute.
> - `computeIfAbsent` mapping function dumps do not discuss reentrancy / recursion on the same map.
