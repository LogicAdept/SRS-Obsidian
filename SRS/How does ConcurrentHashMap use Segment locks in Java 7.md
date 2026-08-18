<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: Java **7** `ConcurrentHashMap` is a **segmented array + linked list**. It uses **segment locks**: the bucket array is split into `Segment`s. Each lock covers only part of the table, so threads on **different segments** do not contend. The same dump: `Segment` extends **`ReentrantLock`**. Theoretically it supports **`concurrencyLevel`** concurrent writers (size of the `Segment` array). Occupying one segment does not lock the others.

`get` in that dump needs **no lock**: hash to a segment, hash again to the entry; `HashEntry.value` is **`volatile`**.

`put` still locks: `volatile` value is not enough for atomic writes. Resize check happens **before** insert (unlike a dump’s `HashMap` “insert then maybe resize”).

> [!warning] Unverified traps from the dump
> - Default `concurrencyLevel` / segment count is often named **16** in these notes, same as initial capacity in the heading.
> - Java 8 dumps say `Segment` may still exist in the class for **old-version compatibility**, not as the live lock table.
