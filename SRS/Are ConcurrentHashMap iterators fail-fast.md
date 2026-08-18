<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **no.** `ConcurrentHashMap` iterators are **fail-safe** and **will never throw `ConcurrentModificationException`**. They operate on a **clone** of the collection (same sentence as `CopyOnWriteArrayList`). Another dump: the `keySet` iterator of `ConcurrentHashMap` is fail-safe.

Compilation dumps: iteration is **weakly consistent** (may see a mix of updates), not fail-fast.

> [!warning] Unverified traps from the dump
> - “Clone of the collection” is the CopyOnWrite story; weakly-consistent CHM iterators are not the same mechanism.
> - Fail-safe here means “no CME,” not “you see a frozen snapshot of the whole map.”
