<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues/BlockingQueue #Java/Collections/Queues/PriorityQueue #SRS

# What is a `DelayQueue`?

> [!abstract] Short answer
> **An unbounded `BlockingQueue` of `Delayed` elements that you can remove only after their delay has expired.** `take` waits until the expired head exists. The head is the earliest expiration, even if that time is still in the future. `put` never waits for capacity. Since 1.5. No `null`s.

## Expired head versus head

An element is **expired** when `getDelay(TimeUnit.NANOSECONDS) <= 0`. The **head** is the element with the earliest expiration (past or future). The **expired head**, when present, is also the head.

`poll`, `poll(timeout)`, `take`, and `remove()` **intentionally violate** the usual `BlockingQueue` contract: they ignore unexpired elements and only ever take the expired head. `size()` counts everyone. `peek()` may return a non-null head while `take` would still block waiting for that element to expire. `iterator()` walks expired and unexpired, in no particular order, and is weakly consistent. [[How do you implement producer-consumer with a BlockingQueue]]

`Delayed` is a mix-in: `getDelay(TimeUnit)` plus a `compareTo` that is **consistent with** `getDelay`. Zero or negative remaining delay means “already due.”

```java
import java.util.concurrent.DelayQueue;
import java.util.concurrent.Delayed;
import java.util.concurrent.TimeUnit;

final class Task implements Delayed {
    final String name;
    final long readyAtNanos;

    Task(String name, long delay, TimeUnit unit) {
        this.name = name;
        this.readyAtNanos = System.nanoTime() + unit.toNanos(delay);
    }

    @Override
    public long getDelay(TimeUnit unit) {
        return unit.convert(readyAtNanos - System.nanoTime(), TimeUnit.NANOSECONDS);
    }

    @Override
    public int compareTo(Delayed o) {
        return Long.compare(
                getDelay(TimeUnit.NANOSECONDS), o.getDelay(TimeUnit.NANOSECONDS));
    }
}

class Demo {
    static void use() throws InterruptedException {
        DelayQueue<Task> q = new DelayQueue<>();
        q.put(new Task("later", 5, TimeUnit.SECONDS)); // never blocks
        Task next = q.peek();  // may be unexpired
        Task due = q.take();   // waits until expired; InterruptedException
    }
}
```

**Listing 1.** `put` inserts immediately. `peek` is not “ready to run.” `take` is.

OpenJDK’s `DelayQueue` stores elements in a `PriorityQueue` under a `ReentrantLock`. `compareTo` (not array order) puts the soonest expiration at the heap head. `take` then `await`s until that delay elapses — you do not `sleep` and poll yourself. That is a concurrent heap, not a plain `PriorityQueue`: `PriorityQueue.poll()` returns the least element whether or not a delay has elapsed. [[Is PriorityQueue thread-safe]] [[What is java.util.PriorityQueue]]

```d2
direction: down
put: "put / offer\nimmediately, unbounded" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
heap: "head = earliest expiration\n(may still be in the future)" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
take: "take / poll\nonly expired head" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

put -> heap
heap -> take: "getDelay > 0 → wait"
```

**Fig. 1.** Capacity is not the gate. Time is. `remainingCapacity()` is always `Integer.MAX_VALUE`.

`clear()` drops unexpired elements without waiting. `remove(Object)` can delete an element whether or not it has expired. `drainTo` transfers only what is already available (expired).

> [!warning] `peek` is not `poll`
> `peek` returns the next-to-expire element even when `getDelay` is still positive. `poll()` returns `null` in that case; `take` blocks; `remove()` throws `NoSuchElementException`. Treating `size() > 0` as “something is due” is wrong — unexpired items count. `compareTo` that disagrees with `getDelay` breaks the heap order. Do not use this as a bounded buffer: `put` never waits.

> [!tip] Interview answer
> **`DelayQueue` is an unbounded blocking queue of `Delayed` objects.** You insert immediately; you can `take` an element only after `getDelay` is zero or negative. `take` waits for that expiry. `peek` can show a not-yet-due head. It is not a `PriorityQueue` you poll yourself, and it is not a capacity-bounded `ArrayBlockingQueue`.
