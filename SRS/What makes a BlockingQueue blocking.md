<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: a `BlockingQueue` is a thread-safe queue whose **`put` waits when full** and whose **`take` waits when empty** — so threads do not busy-wait. Backbone of **producer-consumer** and of `ThreadPoolExecutor`’s work queue.

Method families in the dump:

- throw: `add` / `remove`
- special value: `offer` / `poll`
- block: `put` / `take`
- time out: `offer(e, t, u)` / `poll(t, u)`

Another dump: dequeue from empty **blocks until an insert**; enqueue on full **blocks until space**.

> [!warning] Unverified traps from the dump
> - `ConcurrentLinkedQueue` is **not** a `BlockingQueue`; `poll` returns `null` instead of waiting.
