<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `ConcurrentLinkedQueue` (and `ConcurrentLinkedDeque`) is **unbounded, non-blocking, lock-free** FIFO on **CAS**. `offer` / `poll` **never block** — `poll` returns **`null`** if empty.

Use it when consumers can **do other work** if the queue is empty (poll-and-continue). Use a **`BlockingQueue`** when consumers should **block on `take`**.

Rule of thumb in the dump: lock-free `ConcurrentLinkedQueue` for non-blocking pipelines; `BlockingQueue` when you want waiting.

> [!warning] Unverified traps from the dump
> - Unbounded `offer` never “full”; dumps warn of memory growth / OOME if producers outrun consumers.
