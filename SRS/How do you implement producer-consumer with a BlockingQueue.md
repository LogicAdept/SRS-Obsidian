<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues/BlockingQueue #SRS

# How do you implement producer-consumer with a `BlockingQueue`?

> [!abstract] Short answer
> **Share one `BlockingQueue`. Producers `put`; consumers `take`.** `put` waits for space; `take` waits for an element. That is the bounded-buffer protocol without `wait` / `notify`. `ArrayBlockingQueue` is the classic fixed-capacity buffer. Several producers and several consumers may share the same queue.

## `put` and `take` are the protocol

A `BlockingQueue` is a `Queue` that waits for the queue to become non-empty on retrieve, and waits for space on store. Implementations are thread-safe and are **designed primarily as producer-consumer queues**. Since 1.5.

Four forms exist for insert and remove. Producer-consumer uses the **blocking** pair:

| | Throws | Special value | Blocks | Times out |
| --- | --- | --- | --- | --- |
| Insert | `add(e)` | `offer(e)` | **`put(e)`** | `offer(e, t, u)` |
| Remove | `remove()` | `poll()` | **`take()`** | `poll(t, u)` |

`put` waits for space; `take` waits until a head element exists. Both throw `InterruptedException` if interrupted while waiting. `add` on a full bounded queue throws `IllegalStateException` instead of waiting. `offer` returns `false`. `poll` returns `null` (null is also forbidden as an element — it is the `poll` failure sentinel). [[What makes a BlockingQueue blocking]]

The queue **may** be capacity-bounded. `remainingCapacity` is extra slots you can `put` without blocking, or `Integer.MAX_VALUE` when there is no intrinsic limit. `ArrayBlockingQueue` is a **classic bounded buffer**: fixed array, capacity set at construction and never changed; `put` on full blocks; `take` on empty blocks. Optional fairness (`true`) serves waiting threads in FIFO order.

`LinkedBlockingQueue` is **optionally** bounded. `new LinkedBlockingQueue(5)` caps at five. `new LinkedBlockingQueue()` uses `Integer.MAX_VALUE` — the producer will not block on capacity. Linked nodes are created per insert until that cap. [[What is the difference between ArrayBlockingQueue and LinkedBlockingQueue]]

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

class ProducerConsumer {
    static final String POISON = "EOF";

    static void run() throws InterruptedException {
        BlockingQueue<String> q = new ArrayBlockingQueue<>(5);

        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < 8; i++) {
                    q.put("item-" + i); // waits if q is full
                }
                q.put(POISON);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        Thread consumer = new Thread(() -> {
            try {
                for (;;) {
                    String x = q.take(); // waits if q is empty
                    if (POISON.equals(x)) {
                        break;
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        producer.start();
        consumer.start();
        producer.join();
        consumer.join();
    }
}
```

**Listing 1.** Bounded `ArrayBlockingQueue`. `put` / `take` implement backpressure. A poison object stops the consumer — the interface has no `close`.

```d2
direction: right
p: "Producer\nput(e)" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
q: "BlockingQueue\ncapacity N" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
c: "Consumer\ntake()" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}

p -> q: "full → wait"
q -> c: "empty → wait"
```

**Fig. 1.** The queue is the monitor. Several producers and several consumers may attach to `q`.

A `put` happens-before the matching `take` in another thread (same as other concurrent collections). Bulk `addAll` / `removeAll` are not necessarily atomic.

Hand-rolled `wait` / `notify` on a mutex around an array is the same idea; `BlockingQueue` is that recipe as a library type. [[How do you implement a bounded buffer with synchronized in Java]] [[How do methods wait and notify notifyAll]]

> [!warning] `put`/`take`, not `add`/`poll`, and not an unbounded linked queue
> `add` on a full `ArrayBlockingQueue` throws `IllegalStateException`; it does not wait. `offer` / `poll` return immediately. `new LinkedBlockingQueue()` is not a bounded buffer — capacity is `Integer.MAX_VALUE`, so the producer never waits for the consumer. `put` and `take` throw `InterruptedException`; restore the interrupt (or exit) — do not empty-catch it. There is no shutdown on the interface; a poison object (or `offer` with a timeout plus a stop flag) is the usual end-of-stream. `null` is never an element.

> [!tip] Interview answer
> **Share a `BlockingQueue`: producers `put`, consumers `take`.** That waits on full and empty without you writing `wait` / `notify`. Use `ArrayBlockingQueue` for a fixed bounded buffer; `LinkedBlockingQueue(n)` if you want a linked cap. Several producers and consumers are supported. Handle `InterruptedException`, and do not use the no-arg linked constructor if you needed backpressure.
