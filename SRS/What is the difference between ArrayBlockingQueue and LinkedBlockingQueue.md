<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues/BlockingQueue #SRS

# What is the difference between `ArrayBlockingQueue` and `LinkedBlockingQueue`?

> [!abstract] Short answer
> **Both are FIFO `BlockingQueue`s. `ArrayBlockingQueue` is always bounded: a fixed array whose capacity never changes.** `LinkedBlockingQueue` is **optionally** bounded: linked nodes, default cap `Integer.MAX_VALUE`. Linked queues typically have **higher throughput** than array ones, with **less predictable** performance. Only the array type has a **fair** constructor. Since 1.5. No `null`s.

## Fixed array versus optional linked cap

`ArrayBlockingQueue` is the classic bounded buffer: producers `put` into a fixed-size array, consumers `take` from it. Full → `put` blocks; empty → `take` blocks. Capacity is required and cannot grow. Optional fairness: `new ArrayBlockingQueue<>(100, true)` serves waiting threads in FIFO order. Fairness generally **lowers** throughput, cuts variability, and avoids starvation. Default is nonfair. Memory is the array of that length — a stable footprint. [[How do you implement producer-consumer with a BlockingQueue]]

`LinkedBlockingQueue` uses linked nodes created on each insert (until the cap). `new LinkedBlockingQueue(n)` is a bounded linked buffer. `new LinkedBlockingQueue()` (and the collection copy constructor) uses capacity `Integer.MAX_VALUE` — producers will not wait on a “full” queue; they can exhaust the heap. There is **no** `fair` constructor. [[What is the difference between a bounded and an unbounded queue]]

The linked class page: linked queues typically have higher throughput than array-based queues but less predictable performance in most concurrent applications. That is the documented rule of thumb — not a guarantee that linked always wins.

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

class Demo {
    static void ctors() {
        ArrayBlockingQueue<Integer> array = new ArrayBlockingQueue<>(100);
        ArrayBlockingQueue<Integer> fair = new ArrayBlockingQueue<>(100, true);

        LinkedBlockingQueue<Integer> linkedCap = new LinkedBlockingQueue<>(100);
        LinkedBlockingQueue<Integer> linkedOpen = new LinkedBlockingQueue<>(); // Integer.MAX_VALUE
    }
}
```

**Listing 1.** Same FIFO `put`/`take` API. The no-arg linked queue is not a bounded buffer.

```text
ArrayBlockingQueue
  always bounded array; capacity frozen
  one ReentrantLock on all access (fair optional)
  notEmpty / notFull conditions on that lock

LinkedBlockingQueue
  optional bound; default Integer.MAX_VALUE
  putLock (offer/put) and takeLock (poll/take) — two-lock queue
  nodes allocated per insert
```

**Listing 2.** OpenJDK internals behind the throughput sentence: array operations share one monitor; linked put and take can proceed on different locks.

```d2
direction: down
same: "FIFO BlockingQueue\nput waits if full*\ntake waits if empty" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
abq: "ArrayBlockingQueue\nfixed array, optional fair" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
lbq: "LinkedBlockingQueue\nnodes, optional cap" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

same -> abq
same -> lbq
```

**Fig. 1.** \*On the no-arg linked queue, “full” is `Integer.MAX_VALUE` — back-pressure is gone.

Both iterators are weakly consistent. `offer` / `add` / `put` follow the usual bounded-queue forms when a real cap is in play.

> [!warning] `new LinkedBlockingQueue()` is not `ArrayBlockingQueue` with a bigger array
> It is an **unbounded** (for practical purposes) linked buffer: no fair mode, growing nodes, possible `OutOfMemoryError` if producers outrun consumers. `new LinkedBlockingQueue(Integer.MAX_VALUE)` is the same cap as the no-arg constructor. Fairness exists only on `ArrayBlockingQueue`. “Higher throughput” is typical, not a promise — fairness on the array type **reduces** throughput on purpose.

> [!tip] Interview answer
> **`ArrayBlockingQueue` is a fixed-capacity array buffer with an optional fair lock. `LinkedBlockingQueue` is linked nodes, optionally bounded, default unbounded.** Linked is documented as typically higher throughput and less predictable. Use the array type for a simple bounded buffer with a known footprint; pass a capacity to the linked type if you still want back-pressure. Neither allows `null`.
