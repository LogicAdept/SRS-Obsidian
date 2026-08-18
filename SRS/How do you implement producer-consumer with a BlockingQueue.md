<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: producer and consumer are two threads sharing a **bounded** queue. Producer **halts** when the queue is full; consumer **halts** when it is empty.

Dump approaches: `wait()` / `notifyAll()`, **`BlockingQueue`**, semaphores.

`BlockingQueue` sample: `LinkedBlockingQueue` with max size; producer `put`, consumer `take` (both wait via the queue):

```java
static int MAX_SIZE = 5;
static BlockingQueue queue = new LinkedBlockingQueue(MAX_SIZE);

// producer
queue.put(element);

// consumer
System.out.println("Consumed " + queue.take());
```

> [!warning] Unverified traps from the dump
> - `put` / `take` throw `InterruptedException` in the dump sample (caught empty on the producer).
> - Other dumps also show `ArrayBlockingQueue` as the bounded buffer.
