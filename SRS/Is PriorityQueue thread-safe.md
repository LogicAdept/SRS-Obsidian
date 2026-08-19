<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **PriorityQueue is not thread safe.** Use **`PriorityBlockingQueue`** in a concurrent environment.

> [!warning] Unverified traps from the dump
> - `PriorityBlockingQueue` is unbounded and `take` blocks when empty — not a drop-in lock around `PriorityQueue`.
> - Wrapping with `Collections.synchronizedCollection` is not what this dump names.
