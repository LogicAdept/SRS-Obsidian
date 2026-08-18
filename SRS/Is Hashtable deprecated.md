<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **no.** `Hashtable` has been in Java since version 1.0. **It is not deprecated** but is **mostly considered obsolete.** It is a thread-safe hash map whose methods are simply synchronized.

Other dumps call `Hashtable` a **legacy** class whose use is **not recommended**.

> [!warning] Unverified traps from the dump
> - “Obsolete / not recommended” is not the same claim as `@Deprecated`.
> - The same dump still lists `Hashtable` among Map implementations; that is not an invitation to pick it for new maps.
