<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Versions/8 #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: Java 8 dropped segment locks. Data structure matches `HashMap` 1.8: **array + list / red-black tree**. Nodes use **`volatile` `val` / `next`**. Concurrency: **CAS + `synchronized`**.

`put` (dump steps): hash the key; init table if needed; if the bin Node `f` is empty, **CAS** the write (spin on failure); if hash is **`MOVED` (−1)**, help **resize**; otherwise **`synchronized`** to write; if the bin is longer than **`TREEIFY_THRESHOLD`**, treeify.

`get`: hash to a bin; return if the node is there; else tree walk or list walk. No lock named on that path.

> [!warning] Unverified traps from the dump
> - Empty-bin CAS and occupied-bin `synchronized` are different paths in the same `put`.
> - `MOVED == -1` is dump resize signaling, not a user hash.
