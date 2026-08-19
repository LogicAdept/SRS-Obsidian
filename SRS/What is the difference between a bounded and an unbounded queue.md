<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: an **unbounded** queue grows as needed (limited only by memory) — `LinkedList`, `ArrayDeque`, `PriorityQueue`, `ConcurrentLinkedQueue`, `LinkedBlockingQueue` (default). A **bounded** queue has a fixed maximum capacity set at construction — `ArrayBlockingQueue`, or `LinkedBlockingQueue` given a capacity.

```java
Queue<Integer> unbounded = new ArrayDeque<>();
BlockingQueue<Integer> bounded = new ArrayBlockingQueue<>(2);
bounded.offer(1);
bounded.offer(2);
bounded.offer(3); // false — full, rejected (offer form)
```

Dump: bounds matter for **back-pressure**. On a full bounded queue, `add` throws, `offer` returns `false`, and `put` (blocking) waits.

> [!warning] Unverified traps from the dump
> - Default `LinkedBlockingQueue` is unbounded; capacity is optional.
> - `ArrayDeque` is unbounded even though it is array-backed.
