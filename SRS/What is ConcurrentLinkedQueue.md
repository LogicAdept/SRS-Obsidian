<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues #SRS

# What is `ConcurrentLinkedQueue`?

> [!abstract] Short answer
> **An unbounded, thread-safe FIFO `Queue` of linked nodes.** Many threads may share it. `offer` / `add` at the tail never wait and never return `false`. `poll` / `peek` at the head return `null` when empty — they do **not** block. No `null` elements. Since 1.5. It is not a `BlockingQueue`.

## Non-blocking FIFO, not `take`

The head is the oldest element; the tail is the newest. It is an appropriate choice when many threads share one collection. The implementation uses a non-blocking algorithm based on Michael and Scott’s concurrent queue paper. Package overview: a scalable **non-blocking** FIFO queue (contrast `BlockingQueue`, which waits on full/empty). [[What is the difference between ConcurrentLinkedQueue and a BlockingQueue]] [[How do you implement producer-consumer with a BlockingQueue]]

`ConcurrentLinkedDeque` is the deque sibling: same concurrent-linked idea, plus `Deque` operations. A rendezvous with **zero** capacity is a different type. [[What is a SynchronousQueue]]

```java
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

class Demo {
    static void fifo() {
        Queue<Integer> q = new ConcurrentLinkedQueue<>();
        q.offer(1);
        q.offer(2);
        Integer head = q.poll(); // 1; null if empty — does not wait
        q.peek();                // next head, or null
    }
}
```

**Listing 1.** `Queue` methods only. There is no `take` / `put`. Empty `poll` is `null`, not a park.

```text
ConcurrentLinkedQueue
  unbounded linked FIFO
  thread-safe, non-blocking
  no nulls
  offer/add: never false / never ISE
  poll/peek: null if empty
  iterator: weakly consistent, head→tail, no CME
  size(): O(n), may be stale under concurrent updates
```

**Listing 2.** `size()` is not a snapshot you can use for control flow.

```d2
direction: down
offer: "offer / add\ntail, never waits" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
q: "linked FIFO\nmany threads" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
poll: "poll / peek\nnull if empty" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

offer -> q
q -> poll
```

**Fig. 1.** Producer-consumer **waiting** needs a `BlockingQueue`. This type is share-and-poll.

Iterators are weakly consistent: they reflect the queue at some point at or since creation, do not throw `ConcurrentModificationException`, and may run beside other operations. Elements present since iterator creation are returned exactly once. Bulk `addAll` / `removeIf` / `forEach` are not necessarily atomic. A `put` into the queue happens-before a later `poll` of that element in another thread.

> [!warning] `poll` is not `take`, and `size` is not a lock
> Empty → `null`, immediately. A consumer that must wait needs `LinkedBlockingQueue.take` (or another `BlockingQueue`), not a spin on `poll`. `size()` walks the chain (O(n)) and can be wrong if others mutate during the walk — do not use it to decide “the queue is idle.” `null` is `NullPointerException`. `forEach` concurrent with `addAll` may see only some new elements.

> [!tip] Interview answer
> **`ConcurrentLinkedQueue` is an unbounded concurrent FIFO queue: linked nodes, no locks on `offer`/`poll`, no nulls.** `poll` returns `null` when empty; it never waits. Iterators are weakly consistent. `size()` is a traversal, not O(1). For a blocking producer-consumer, use a `BlockingQueue`, not this type.
