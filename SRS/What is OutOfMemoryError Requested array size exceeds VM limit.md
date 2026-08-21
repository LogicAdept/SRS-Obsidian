<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/JVM/Memory #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list `java.lang.OutOfMemoryError: Requested array size exceeds VM limit` as its own OOM flavor: the program tried to allocate an array larger than the VM will allow (dump wording: larger than the heap / VM limit). Example they show: `new Integer[1000 * 1000 * 1000]` under a tiny `-Xmx`.

This is distinct in dump catalogs from `Java heap space` and from `GC overhead limit exceeded`.
> [!warning] Unverified traps from the dump
> - Dump text equates this with an array larger than the heap; official troubleshooting also describes a hard VM max array length, so a huge length can fail even when free heap looks large.
> - Raising -Xmx may not help if the requested length exceeds the VM's maximum array size.
