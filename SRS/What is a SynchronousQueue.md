<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues/BlockingQueue #Java/Concurrency/Executors #SRS

# What is a `SynchronousQueue`?

> [!abstract] Short answer
> **A `BlockingQueue` with no internal capacity — not even one slot.** Each `put` waits for a `take` in another thread, and each `take` waits for a `put`. It is a rendezvous / hand-off, not a buffer. `peek` is always `null`. `size` is always 0. No `null` elements. Since 1.5.

## Insert waits for remove, and the reverse

You cannot insert unless another thread is trying to remove; you cannot `peek` because an element is only present while a removal is in progress; you cannot iterate — there is nothing to iterate. For `contains` and friends it behaves as an **empty** collection. `isEmpty()` is always `true`. `remainingCapacity()` is always 0. `clear()` does nothing. `toString()` is `"[]"`.

`put` waits for a consumer (`InterruptedException` if interrupted). `take` waits for a producer. Timed `offer` / `poll` wait up to a timeout. Untimed `offer` succeeds only if a taker is already waiting — otherwise `false`. Untimed `poll` returns `null` unless a putter is already waiting. [[How do you implement producer-consumer with a BlockingQueue]]

That is **not** `ArrayBlockingQueue(1)`. A one-slot array queue can hold an element with no consumer present. A synchronous queue cannot.

```java
import java.util.concurrent.SynchronousQueue;

class Demo {
    static void handoff() throws InterruptedException {
        SynchronousQueue<String> q = new SynchronousQueue<>();
        Thread consumer = new Thread(() -> {
            try {
                q.take(); // waits for put
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        consumer.start();
        q.put("task"); // waits until take is in progress
        consumer.join();
        // q.peek() == null; q.size() == 0; q.offer("x") == false here
    }
}
```

**Listing 1.** Direct hand-off. `put` / `take` throw `InterruptedException`. After both return, the queue is still “empty.”

```text
SynchronousQueue
  capacity: none (not even 1)
  put  ↔ take   (rendezvous)
  offer(e): true only if a taker is already waiting
  peek / iterator / size: null / empty / 0
  fair=true: waiting threads in FIFO; default nonfair
```

**Listing 2.** Collection methods lie in the usual sense: they report an empty collection even while threads are blocked in `put`.

```d2
direction: right
p: "Producer\nput(e)" {
  width: 160
  height: 70
  style.fill: "#e3f2fd"
}
r: "no slot\nhandoff" {
  width: 160
  height: 70
  style.fill: "#fff3e0"
}
c: "Consumer\ntake()" {
  width: 160
  height: 70
  style.fill: "#e8f5e9"
}

p -> r: waits for take
c -> r: waits for put
```

**Fig. 1.** CSP-style rendezvous: the item never sits in the queue.

Optional fairness: `new SynchronousQueue(true)` serves waiting threads in FIFO order. The no-arg constructor is nonfair.

`ThreadPoolExecutor` documents this as the **direct handoff** work queue: if no worker is idle, queueing fails and a new thread is created (needs a large `maximumPoolSize`). `Executors.newCachedThreadPool()` is that setup: core 0, max `Integer.MAX_VALUE`, 60s keep-alive, `new SynchronousQueue<Runnable>()`. [[How would you explain Executors.newCachedThreadPool()]]

> [!warning] `peek`, `size`, and `offer` are not a buffer API
> `peek()` always returns `null`. `size()` is always 0. You cannot poll a staged item later. `offer(e)` without a waiting taker is `false` — it does not enqueue. `add(e)` then throws `IllegalStateException`. Use `put`/`take` (or timed `offer`/`poll`) for the rendezvous. `null` is forbidden.

> [!tip] Interview answer
> **`SynchronousQueue` is a blocking queue with zero capacity: `put` waits for `take` and `take` waits for `put`.** Nothing is stored. `peek` and `size` always look empty. Cached thread pools use it so a task is handed to an idle worker or a new thread is started — it is never buffered in the queue.
