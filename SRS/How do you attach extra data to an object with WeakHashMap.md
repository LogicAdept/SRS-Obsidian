<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: use it when you must **add information to objects without changing their class**. Put each object as a **key** and the extra information as the **value**. While a strong (or soft) reference to the object exists, you can look up the table. When the object is collected, the weak key is enqueued and the mapping is removed.

> [!warning] Unverified traps from the dump
> - This is “sidecar metadata,” not “WeakHashMap is an LRU cache.”
> - The dump still needs some *other* strong or soft ref to the key, or there is nothing left to look up.
