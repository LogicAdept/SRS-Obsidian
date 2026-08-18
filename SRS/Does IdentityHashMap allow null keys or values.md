<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **yes.** Both `HashMap` and `IdentityHashMap` permit a **null key and null values**.

FAQ dump: both `IdentityHashMap` and `WeakHashMap` support **null keys**.

> [!warning] Unverified traps from the dump
> - Nulls here are not the `Hashtable` / `ConcurrentHashMap` story.
> - A null key is still one slot; identity of “the null key” is not a second object.
