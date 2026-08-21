<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/JVM/Memory #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `java.lang.OutOfMemoryError: PermGen space` is pre-Java 8 Permanent Generation metadata (tuned with `-XX:PermSize` / `-XX:MaxPermSize`). Raising `-Xmx` does not fix it.

From Java 8, class metadata lives in Metaspace. Dumps: `OutOfMemoryError: Metaspace` when there is no room to allocate class metadata; limit with `-XX:MaxMetaspaceSize`. Demo dumps generate it by dynamically defining many classes under a tiny MaxMetaspaceSize.
> [!warning] Unverified traps from the dump
> - Heap OOM (Java heap space) and Metaspace/PermGen OOM are different memory pools.
> - PermGen space is obsolete on modern JDKs; Metaspace is the current class-metadata OOM message.
