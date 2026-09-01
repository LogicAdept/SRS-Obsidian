<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues/BlockingQueue #SRS

# What makes a `BlockingQueue` blocking?

> [!abstract] Short answer
> **Waiting: `take` parks while the queue is empty and `put` parks while it is full.** That is what “blocking” means on this type. `offer` / `poll` still return immediately (`false` / `null`). The wait is why producer-consumer loops and `ThreadPoolExecutor` workers do not spin on `poll`.

## `put` / `take` wait; `offer` / `poll` do not

A `BlockingQueue` is a `Queue` that **additionally** supports operations that wait for the queue to become non-empty when retrieving, and wait for space to become available when storing. Implementations are thread-safe. Insert and remove each have four shapes: throw, special value, block indefinitely, or wait up to a timeout. Only the last two park the caller. [[How would you explain BlockingQueue]] [[How do you implement producer-consumer with a BlockingQueue]]

“Full” is a capacity story. A bounded queue (`ArrayBlockingQueue`, a `LinkedBlockingQueue` constructed with a cap) can make `put` wait. A queue with no intrinsic cap reports `remainingCapacity` of `Integer.MAX_VALUE`; `put` then does not wait for space — `take` can still wait when empty. A zero-capacity queue waits on **both** sides until a peer arrives. [[What is the difference between a bounded and an unbounded queue]] [[What is a SynchronousQueue]] [[What is a PriorityBlockingQueue]]

The non-blocking sibling is a different type: `ConcurrentLinkedQueue` has no `take` / `put`. Empty `poll` is `null`; the caller keeps running. [[What is the difference between ConcurrentLinkedQueue and a BlockingQueue]]

`ThreadPoolExecutor` takes a `BlockingQueue<Runnable>` as its work queue so idle workers can `take` and park until a task is submitted.

```java
BlockingQueue<String> q = new ArrayBlockingQueue<>(1);

q.add("a");                         // throws if full
q.offer("a");                       // false if full
q.put("a");                         // waits if full
q.offer("a", 1, TimeUnit.SECONDS);  // false on timeout

q.remove();                         // throws if empty
q.poll();                           // null if empty
q.take();                           // waits if empty
q.poll(1, TimeUnit.SECONDS);        // null on timeout
```

**Listing 1.** Four families. Only `put` / `take` and the timed pair wait.

```java
BlockingQueue<Runnable> work = new LinkedBlockingQueue<>();
work.put(task);           // producer: wait only if this queue is actually full
Runnable job = work.take(); // worker: wait until a task exists
```

**Listing 2.** Producer-consumer without a busy-wait `poll` loop. Default `LinkedBlockingQueue` is unbounded, so `put` here waits for space only in the `Integer.MAX_VALUE` sense.

```d2
direction: down
Producer: {
  put: put(e)
}
Queue: BlockingQueue
Consumer: {
  take: take()
}
Producer.put -> Queue: waits if full
Consumer.take -> Queue: waits if empty
```

**Fig. 1.** Blocking is conditional: wait for space, or wait for an element — not a spin on `poll`.

> [!warning] `poll` is not what makes it blocking
> `BlockingQueue.poll()` still returns `null` when empty, same idea as `Queue`. The blocking methods are `take` and `put` (and the timed `poll` / `offer`). `ConcurrentLinkedQueue` is not a `BlockingQueue`: there is nothing to wait on. Unbounded blocking queues (`PriorityBlockingQueue`, default `LinkedBlockingQueue`) do not backpressure producers — only `take` still waits.

> [!tip] Interview answer
> **A `BlockingQueue` can wait: `take` parks until an element exists and `put` parks until there is space.** `offer` and `poll` still return immediately. That wait is why producer-consumer and `ThreadPoolExecutor` use it instead of spinning. `ConcurrentLinkedQueue` is not a `BlockingQueue` — empty `poll` is `null`.
