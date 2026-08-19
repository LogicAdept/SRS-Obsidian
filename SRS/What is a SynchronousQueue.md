<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues/BlockingQueue #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **zero internal capacity** — holds **no** elements. A `put` **blocks until** another thread `take`s (and vice versa): **direct hand-off**, not a buffer.

```java
SynchronousQueue<Task> q = new SynchronousQueue<>();
// producer: q.put(task) parks until a consumer is ready
// consumer: q.take() picks it up directly
```

Dump: work queue of **`Executors.newCachedThreadPool()`** — task goes to an idle thread, or a new thread is spawned. Use when you want pickup **immediately or not queued at all**.

> [!warning] Unverified traps from the dump
> - “Zero capacity” means you cannot peek a buffered item; it is a rendezvous, not a list.
