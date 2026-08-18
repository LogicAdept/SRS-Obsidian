<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: TreeMap **values** (and even key objects) are mutable in the Java sense, but **changing a key’s comparison fields after `put` breaks the tree**. The map still holds the object, but the red-black order is no longer valid, so later lookup/iteration can be wrong.

Dump advice: keep keys **immutable**, or **remove and re-insert** after a change.

> [!warning] Unverified traps from the dump
> - The dump’s `Person` snippet mutates `id` after insert; it claims printing the map then shows a broken order.
> - Insertion/get/remove APIs still “work”; the failure is a corrupted sort, not a compile error.
