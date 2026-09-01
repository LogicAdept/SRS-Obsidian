<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #Java/Collections/Queues/BlockingQueue #Java/Collections/Concurrency #SRS

# Is `PriorityQueue` thread-safe?

> [!abstract] Short answer
> **No.** The class is not synchronized. Do not share a `PriorityQueue` across threads if any of them modifies it. The named replacement is `PriorityBlockingQueue`: same heap ordering, blocking `take` when empty. That queue is unbounded, so `put` never waits — it is not “`PriorityQueue` plus a lock.”

## The class page names the replacement

`PriorityQueue` (1.5) is an unbounded binary heap. `offer` / `add` / `poll` / `remove()` are O(log n). It forbids `null`. It is **not synchronized**. Several threads must not use the same instance if any of them mutates it. Use `PriorityBlockingQueue` instead. [[What is java.util.PriorityQueue]]

`PriorityBlockingQueue` uses the same ordering rules and also forbids `null`. It is a `BlockingQueue`: `take` waits until a head element exists (`InterruptedException` if interrupted). Because it is **logically unbounded**, `put` never blocks and `offer` never returns `false` (additions can still fail with `OutOfMemoryError`). `remainingCapacity` is always `Integer.MAX_VALUE`. Iterators are weakly consistent and not in priority order. [[What is a PriorityBlockingQueue]] [[How do you implement producer-consumer with a BlockingQueue]]

```java
import java.util.PriorityQueue;
import java.util.concurrent.PriorityBlockingQueue;

class Demo {
    static void contrast() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.offer(2);
        pq.offer(1);
        Integer head = pq.poll(); // 1; null if empty — does not wait

        PriorityBlockingQueue<Integer> pbq = new PriorityBlockingQueue<>();
        pbq.put(2); // never blocks on capacity
        try {
            Integer taken = pbq.take(); // waits if empty
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

**Listing 1.** `poll` on `PriorityQueue` is not `take`. `put` on `PriorityBlockingQueue` is not a bounded-buffer wait.

```d2
direction: down
pq: "PriorityQueue\nnot synchronized, unbounded" {
  width: 300
  height: 70
  style.fill: "#ffcdd2"
}
pbq: "PriorityBlockingQueue\nsame order; take waits; put never waits" {
  width: 360
  height: 80
  style.fill: "#e8f5e9"
}
wrap: "Collections.synchronizedCollection\none lock; iterate under synchronized(c)" {
  width: 380
  height: 80
  style.fill: "#fff3e0"
}

pq -> pbq: concurrent + blocking take
pq -> wrap: coarse lock, still no take
```

**Fig. 1.** Three answers to “threads and a heap.” The javadoc names the middle box.

There is no `Collections.synchronizedQueue`. `Collections.synchronizedCollection(new PriorityQueue<>())` is a one-mutex wrapper: all access through the returned collection, and you must `synchronized (c)` around `Iterator` / `Spliterator` / `Stream`. That does **not** add `take`, and it is not what `PriorityQueue` tells you to use.

A bounded producer-consumer heap is not this type. `ArrayBlockingQueue` is FIFO. A bounded priority buffer is not in `java.util.concurrent` as a standard class — you would compose a lock with a `PriorityQueue`, or accept an unbounded `PriorityBlockingQueue`.

> [!warning] `PriorityBlockingQueue` is not a locked `PriorityQueue`
> Both heaps grow without a capacity cap. Switching types does not create backpressure: the producer’s `put` never waits for the consumer. `PriorityQueue.poll()` returns `null` on empty; it does not block. Empty-catching `InterruptedException` from `take` is wrong — restore the interrupt. A wrapper around `PriorityQueue` still has no `take`, and skipping `synchronized (c)` on iteration is unspecified concurrent access.

> [!tip] Interview answer
> **No — `PriorityQueue` is not thread-safe; the javadoc replacement is `PriorityBlockingQueue`.** Same ordering, no nulls, but `take` waits when empty and `put` never waits because the queue is unbounded. A `Collections.synchronizedCollection` wrap is one lock and still not a blocking queue. Do not treat `poll` as `take`.
