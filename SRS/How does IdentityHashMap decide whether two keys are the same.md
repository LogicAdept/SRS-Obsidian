<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/HashCodeEquals #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: two keys `k1` and `k2` are the same **iff `k1 == k2`** (same object). `HashMap` uses `(k1==null ? k2==null : k1.equals(k2))`.

Compilation example: `new String("key")` twice is **one** `HashMap` key (second `put` replaces) and **two** `IdentityHashMap` keys (size 2, both strings print).

> [!warning] Unverified traps from the dump
> - String **literals** `"key"` may be interned, so two literals can be `==` and collapse even in `IdentityHashMap`.
> - Dumps also apply `==` to **values** (`containsValue` / entry equality), not only keys.
