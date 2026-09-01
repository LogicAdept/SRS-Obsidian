<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues/BlockingQueue #SRS

# What is the difference between `ConcurrentLinkedQueue` and a `BlockingQueue`?

> [!abstract] Short answer
> **`ConcurrentLinkedQueue` is an unbounded non-blocking FIFO `Queue`; a `BlockingQueue` can wait.** `offer` / `poll` on the linked concurrent queue never park: empty means `null`. `put` / `take` on a blocking queue park until there is space or an element. The linked concurrent type does not implement `BlockingQueue`, so it cannot be an executor work queue.

## Never wait versus wait for empty or full

Both live in `java.util.concurrent` and both are thread-safe FIFOs that reject `null`. The interface split is the interview point. `ConcurrentLinkedQueue` is a `Queue` of linked nodes: many threads may share it; inserts go to the tail; retrievals take the head. It is unbounded. `offer` / `add` never wait and never fail for capacity. `poll` / `peek` return `null` when empty. There is no `take`, no `put`, no timed wait, no `remainingCapacity`. The algorithm is non-blocking (Michael and Scott). [[What is ConcurrentLinkedQueue]]

A `BlockingQueue` is a `Queue` that **adds** waiting forms. Four shapes for insert and for remove: throw, special value (`false` / `null`), block forever (`put` / `take`), or wait up to a timeout. A given implementation may be capacity-bounded (`remainingCapacity` then drops toward zero) or report `Integer.MAX_VALUE` when it has no intrinsic cap. Package overview contrast: the linked concurrent queue is a scalable **non-blocking** FIFO; a blocking queue waits on full or empty. [[What makes a BlockingQueue blocking]] [[How do you implement producer-consumer with a BlockingQueue]]

Use the linked concurrent queue when a consumer can **do other work** if `poll` is `null` (poll-and-continue). Use a `BlockingQueue` when the consumer should **park until work arrives**, and when a producer should **park when the buffer is full** — classic producer-consumer backpressure. A zero-capacity rendezvous is still a `BlockingQueue`, not a linked concurrent queue. [[What is a SynchronousQueue]] [[What is the difference between a bounded and an unbounded queue]]

`ThreadPoolExecutor` takes a `BlockingQueue<Runnable>` as its work queue. A `ConcurrentLinkedQueue` does not implement that type, so it cannot be plugged in there.

```java
ConcurrentLinkedQueue<Runnable> pipeline = new ConcurrentLinkedQueue<>();
pipeline.offer(task);                 // never waits, never false
Runnable a = pipeline.poll();         // null if empty — the caller keeps going

BlockingQueue<Runnable> buffer = new ArrayBlockingQueue<>(64);
buffer.put(task);                     // waits if the array is full
Runnable b = buffer.take();           // waits if empty
```

**Listing 1.** Same FIFO idea; only the `BlockingQueue` can park.

```java
while (running) {
    Runnable task = pipeline.poll();
    if (task == null) {
        doOtherWork();                // empty is a signal, not a wait
        continue;
    }
    task.run();
}
```

**Listing 2.** Empty `poll` means continue. To wait for the next task, you wanted `take`.

```d2
direction: right
Empty queue: {
  CLQ: ConcurrentLinkedQueue.poll
  BQ: BlockingQueue.take
}
CLQ -> Null: return null, proceed
BQ -> Park: wait for a producer
```

**Fig. 1.** Empty queue: non-blocking `poll` versus blocking `take`.

> [!warning] `poll` is not `take`, and unbounded is not backpressure
> A loop that spins on `ConcurrentLinkedQueue.poll()` until an element appears burns a core; `BlockingQueue.take()` is the wait. `offer` on the linked concurrent queue never returns `false` for capacity, so a fast producer can exhaust the heap. A bounded `BlockingQueue` is how you apply backpressure. Do not pass a `ConcurrentLinkedQueue` as a `ThreadPoolExecutor` work queue — that parameter is a `BlockingQueue`.

> [!tip] Interview answer
> **`ConcurrentLinkedQueue` is an unbounded concurrent FIFO: `offer` never waits and `poll` returns `null` when empty.** A `BlockingQueue` adds `put` and `take` that park until there is space or an element. Use the linked concurrent queue when a consumer can do other work on an empty poll. Use a blocking queue for producer-consumer waiting and backpressure, including an executor work queue.
