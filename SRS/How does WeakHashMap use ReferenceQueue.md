<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #Java/JVM/Memory #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: when the key object is collected, the `WeakReference` for that key is **enqueued on a `ReferenceQueue`**, and **then** the corresponding mapping is removed from `WeakHashMap`.

The metadata-on-an-object story in the same dump: while a strong (or soft) ref to the key exists, you can `get` the extra value; after the key is gone, the queue path clears the row.

> [!warning] Unverified traps from the dump
> - The dump does not say *which* map method polls the queue, only that enqueue happens and then the entry is deleted.
> - Removal is not described as instantaneous at the moment the last strong ref is dropped.
