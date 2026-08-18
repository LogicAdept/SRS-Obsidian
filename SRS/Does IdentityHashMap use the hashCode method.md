<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/HashCodeEquals #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **no.** `IdentityHashMap` does **not** use `hashCode()`. It uses **`System.identityHashCode()`** to find the bucket. It does **not** use `equals()` either; it uses **`==`**. The same dump: the class is **not a general-purpose `Map`**; it **intentionally violates** the `Map` contract that comparison uses `equals`.

> [!warning] Unverified traps from the dump
> - “Does not use hashCode” means it skips the key’s overridden `hashCode()`, not that hashing is absent.
> - `identityHashCode` is still a hash used to pick a slot.
