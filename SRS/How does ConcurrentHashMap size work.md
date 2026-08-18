<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Java 7 dump: each `Segment` has a **`volatile count`**. `size()` sums those counts. A plain sum is racy, but locking every mutator on every `size()` is too slow. The dump: **try summing twice**; if `count` changed, **then lock** and recount. Change detection: each segment’s **`modCount`** increments on `put` / `remove`.

Compilation dumps: because the map is **never globally locked**, `size()` is an **estimate** (entries move while you sum). Prefer **`mappingCount()`** (`long`) for large maps. Do not branch on `size() == capacity` under concurrent writes.

> [!warning] Unverified traps from the dump
> - The two-try-then-lock story is the **Java 7 segment** algorithm in that dump, not necessarily Java 8.
> - “Estimate” and “lock and recount” are different dump generations of the same cue.
