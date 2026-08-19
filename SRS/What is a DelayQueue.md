<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues/BlockingQueue #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: holds elements implementing **`Delayed`**. An element can be taken **only after its delay elapses**. `take` **blocks** until the head’s delay expires. For scheduled / expiring work (caches, retries, timeouts).

Dump: internally a **`PriorityQueue` ordered by remaining delay**, so the soonest-ready item is at the head. Prefer this over polling with `sleep`.

Another dump vs `PriorityQueue`: `DelayQueue` **releases elements only after their delay expires**.

> [!warning] Unverified traps from the dump
> - Elements must implement `Delayed` (`getDelay`, `compareTo`).
> - Unbounded in the BlockingQueue comparison dumps (unlike `ArrayBlockingQueue`).
