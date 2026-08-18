<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: a **non-blocking, lock-free FIFO** queue based on **CAS** — for high-throughput, low-latency pipelines.

```java
Queue<Integer> clq = new ConcurrentLinkedQueue<>();
clq.offer(1);
clq.offer(2);
System.out.println(clq.poll()); // 1
```

Another dump: Michael-Scott algorithm; enqueue and dequeue use CAS; many threads add/remove **without blocking each other**.

> [!warning] Unverified traps from the dump
> - `poll()` returns **null** when empty; it does not wait.
> - Dump also names `ConcurrentLinkedDeque` as the deque sibling.
