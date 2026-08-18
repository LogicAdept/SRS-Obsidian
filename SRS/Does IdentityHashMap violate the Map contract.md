<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **yes, on purpose.** It implements `Map` but **intentionally violates** the general contract that keys are compared with **`equals`**. It is **not a general-purpose** `Map`. Use it only when **reference-equality** is required (serialization / deep-copy node tables, proxies).

> [!warning] Unverified traps from the dump
> - “Violates Map” is the `equals`-based key sameness rule, not “it fails to implement `get`/`put`.”
> - One dump muddles this sentence with `WeakHashMap` in the same paragraph.
