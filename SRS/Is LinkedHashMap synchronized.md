<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **no.** `LinkedHashMap` is **non synchronized**.

> [!warning] Unverified traps from the dump
> - “Non synchronized” is not the same claim as “safe to share if you only call `get`.”
> - The dump does not give a wrapper recipe; it only states the class is not synchronized.
