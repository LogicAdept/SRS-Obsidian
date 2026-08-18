<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `IdentityHashMap` is a **linear-probe** hash table. `HashMap` uses **chaining**. Both are still “hashtable-based” `Map`s. The dump claims linear probing can be **faster** than chaining `HashMap` for many JREs and mixes.

Another dump: an internal array with **open addressing**; it does not rely on `hashCode()` / `equals()`.

> [!warning] Unverified traps from the dump
> - “Open addressing like HashMap” in one FAQ is sloppy: the HashMap dump in the same comparison is **chaining**.
> - Faster linear probe is an implementation note in dumps, not a reason to drop `equals` for ordinary keys.
