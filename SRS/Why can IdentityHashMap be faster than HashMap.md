<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/HashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: because it skips `hashCode()` / `equals()` and uses `==` plus `identityHashCode`, it can be **faster than `HashMap`**, especially when those methods are **expensive**. FAQ: **sometimes**.

> [!warning] Unverified traps from the dump
> - “Faster” is not “use it instead of HashMap for ordinary value keys.”
> - The same dumps still say it **violates** the `Map` `equals` contract and is not general-purpose.
