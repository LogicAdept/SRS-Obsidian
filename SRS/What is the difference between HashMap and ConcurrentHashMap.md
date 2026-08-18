<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Map/HashMap #Java/Versions/8 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps:

| HashMap | ConcurrentHashMap |
|---|---|
| Not synchronized, not thread-safe | Synchronized / thread-safe |
| Iterator is fail-fast (`ConcurrentModificationException`) | Fail-safe; will never throw CME during iteration |
| Allows a null key and null values | No null key or value; **`NullPointerException`** |
| Faster | Slower than `HashMap` |

Another dump: Java **7** used **`Segment` locks**; Java **8+** uses **CAS + `synchronized` on bin heads**. Null keys and values are **forbidden**. `computeIfAbsent` is an atomic check-then-insert.

> [!warning] Unverified traps from the dump
> - One table calls `ConcurrentHashMap` “synchronized”; other dumps mean segment/bin locks, not one lock on the whole map.
> - “Fail-safe never throws CME” is dump wording; other lists say weakly consistent iterators.
