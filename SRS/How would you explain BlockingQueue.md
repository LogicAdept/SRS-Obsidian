<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues/BlockingQueue #SRS

# How would you explain `BlockingQueue`?

> [!abstract] Short answer
> **A thread-safe `Queue` that can wait.** Beyond `Queue`, it **waits for an element** on retrieve (`take`) and **waits for space** on insert (`put`). That is the producer-consumer API (including a `ThreadPoolExecutor` work queue). Immediate `offer`/`poll` still return `false`/`null`. No `null`s. Capacity **may** be bounded. There is no close.

## Wait for an item, wait for a slot

`BlockingQueue` extends `Queue` with operations that wait until the queue is non-empty (retrieve) or has space (store). Implementations are **thread-safe** and designed **primarily for producer-consumer queues**. Multiple producers and consumers are allowed. `null` is forbidden: it is the sentinel for a failed `poll` [[What makes a BlockingQueue blocking]] [[How do you implement producer-consumer with a BlockingQueue]] [[Why do most Queue implementations forbid null]].

Four forms exist for insert and remove:

| | Throws | Special value | Blocks | Times out |
|---|---|---|---|---|
| Insert | `add(e)` | `offer(e)` | **`put(e)`** | `offer(e, time, unit)` |
| Remove | `remove()` | `poll()` | **`take()`** | `poll(time, unit)` |

`put` / `take` throw `InterruptedException` if interrupted while waiting. `poll()` **does not wait**. A bounded queue (`ArrayBlockingQueue`, or `LinkedBlockingQueue(capacity)`) makes full `put` wait; an unbounded one (`PriorityBlockingQueue`, default `LinkedBlockingQueue`) does not wait for a cap. `SynchronousQueue` has no internal slots: `put` waits for a `take` [[What is the difference between a bounded and an unbounded queue]] [[What is the difference between ArrayBlockingQueue and LinkedBlockingQueue]] [[What is a SynchronousQueue]].

`ArrayBlockingQueue` is the documented **classic bounded buffer**: fixed array, FIFO, `put` blocks when full, `take` when empty, optional fairness. OpenJDK `put`/`take` loop on `Condition.await` (`while` full / `while` empty) under one `ReentrantLock` — not `synchronized` + `Object.wait` on the queue [[What are the two method families on Queue]].

`ConcurrentLinkedQueue` is **not** a `BlockingQueue`: empty `poll` returns `null` immediately [[What is the difference between ConcurrentLinkedQueue and a BlockingQueue]].

```d2
direction: down
prod: "producer put" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
q: "BlockingQueue\nwait for space / wait for item" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
cons: "consumer take" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
nowait: "offer / poll\nfalse / null — no wait" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}

prod -> q
q -> cons
q -> nowait
```

**Fig. 1.** Blocking pair is `put`/`take`. `offer`/`poll` are the `Queue` special-value family.

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

class ExplainBlockingQueue {
    static void demo() throws InterruptedException {
        BlockingQueue<Integer> q = new ArrayBlockingQueue<>(1);
        q.put(1);                      // waits if full
        System.out.println(q.take());  // 1; waits if empty
        System.out.println(q.offer(2)); // true
        System.out.println(q.poll());   // 2 — does not wait
        // q.put(null);                // NullPointerException
    }
}
```

**Listing 1.** Java 5+ `BlockingQueue`. Capacity 1 shows a bounded buffer. `offer`/`poll` do not wait; `put`/`take` do. `null` is illegal.

> [!warning] `poll` / `offer` are not the blocking API
> Empty `poll` returns `null`. Full `offer` returns `false`. Waiting is `take` / `put` (or the timed overloads).

> [!warning] A whiteboard `wait`/`notify` buffer is not `ArrayBlockingQueue`
> `put` waits when full and `take` when empty — that part matches. OpenJDK uses a lock and **two** conditions (`notFull` / `notEmpty`) with `while (… ) await()`, not `synchronized` + `notifyAll` after every call.

> [!tip] Interview answer
> **`BlockingQueue` is a thread-safe `Queue` that can wait: `take` for an element, `put` for space.** Use it for producer-consumer (and as a thread-pool work queue). **`offer`/`poll` still do not wait.** The classic bounded implementation is `ArrayBlockingQueue`; do not confuse it with `ConcurrentLinkedQueue`.
