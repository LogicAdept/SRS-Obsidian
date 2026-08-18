<!--
reps: 0
priority: 0
-->
#Java/Collections/List #Java/Collections/Queues #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **`ArrayDeque` is typically faster and more cache-friendly.** `LinkedList` has **node overhead** but supports **constant-time removals given a node reference**.

A related dump on choosing a queue/stack: prefer `ArrayDeque` for locality and lower overhead; use `LinkedList` only if you need constant-time removal given a node reference.
