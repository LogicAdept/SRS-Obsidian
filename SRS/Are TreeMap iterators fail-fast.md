<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **yes.** Iterators from `keySet()`, `values()`, and `entrySet()` are **fail-fast**. A **structural** modification of the `TreeMap` during iteration (except `Iterator.remove`) throws **`ConcurrentModificationException`**.

The same dumps call `ConcurrentSkipListMap` view iterators **fail-safe** (no CME). General fail-fast vs fail-safe dumps: fail-fast throws CME; fail-safe iterates a copy.

> [!warning] Unverified traps from the dump
> - Fail-fast is **best-effort**; dumps still say do not depend on CME for correctness.
> - Changing only a value is not always treated as a structural modification in the sibling HashMap/LinkedHashMap dumps.
