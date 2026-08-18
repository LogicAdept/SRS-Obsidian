<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `concurrencyLevel` is the **`Segment` array length**. The map theoretically supports that many concurrent writers: a thread locking one segment does not lock the others. Notes also title the class with **initial capacity 16**.

Compilation dumps (Java 8+): `concurrencyLevel` is only a **sizing hint**, not the number of live locks or allowed threads.

> [!warning] Unverified traps from the dump
> - Java 7 “N segments = N concurrent writers” does not match Java 8 bin-level `synchronized`.
> - Initial capacity 16 and concurrencyLevel 16 are easy to mix up in those notes.
