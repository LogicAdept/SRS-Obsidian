<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Caching #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

FAQ dump: **not recommended.** It does **not** release unused keys the way `WeakHashMap` does.

> [!warning] Unverified traps from the dump
> - “Not a cache” is about GC eviction, not about “never store computed values.”
> - IdentityHashMap still **pins** keys with strong refs.
