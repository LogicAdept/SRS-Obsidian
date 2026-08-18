<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **unbounded** blocking queue, ordered by **comparator** (not FIFO). Highest-priority first.

Another dump: unbounded **priority** queue by natural order or `Comparator`; **never blocks on put**; ordering guaranteed for **take/poll**, **not** for iteration; **binary heap** internally.

```java
BlockingQueue<Job> p = new PriorityBlockingQueue<>(); // highest-priority first
```

> [!warning] Unverified traps from the dump
> - Unbounded `put` does not give back-pressure; dumps contrast that with `ArrayBlockingQueue`.
> - Iteration order is not the take order in the dump.
