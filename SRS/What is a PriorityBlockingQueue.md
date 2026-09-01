<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues/BlockingQueue #Java/Collections/Queues/PriorityQueue #SRS

# What is a `PriorityBlockingQueue`?

> [!abstract] Short answer
> **An unbounded `BlockingQueue` with `PriorityQueue` ordering: the head is the least element under natural order or a `Comparator`.** `take` waits when empty. `put` never waits for space (`remainingCapacity` is always `Integer.MAX_VALUE`). No `null`s. Since 1.5. Iteration is **not** in take order.

## Same order as `PriorityQueue`, blocking `take`

`PriorityBlockingQueue` uses the same ordering rules as `PriorityQueue` and adds blocking retrievals. The head is the **least** element for that ordering — not “highest priority” unless your comparator says so. Natural-order `Integer` yields `1` before `3`. Non-comparable inserts under natural ordering throw `ClassCastException`. Equal priorities have **no** FIFO (or other) guarantee; add a secondary key if you need a total order. [[Is PriorityQueue thread-safe]] [[What is java.util.PriorityQueue]]

It is **logically unbounded**. Additions can still fail with `OutOfMemoryError`. `put` never blocks. `offer` never returns `false`. Timed `offer` ignores the timeout. `take` waits until an element exists (`InterruptedException` if interrupted). `poll()` returns `null` immediately when empty. [[How do you implement producer-consumer with a BlockingQueue]]

```java
import java.util.concurrent.PriorityBlockingQueue;

class Demo {
    static void leastFirst() throws InterruptedException {
        PriorityBlockingQueue<Integer> q = new PriorityBlockingQueue<>();
        q.put(3);
        q.put(1);
        Integer head = q.take(); // 1 — least, not “highest”
        // q.iterator() is not guaranteed to be 1 then 3
    }
}
```

**Listing 1.** Natural order is a min-heap. For largest-first, pass `Comparator.reverseOrder()` to the three-arg constructor. Default initial capacity is 11.

```text
PriorityBlockingQueue
  unbounded BlockingQueue  (put never waits)
  order: like PriorityQueue  (least head)
  take / poll(timeout): wait for an element
  iterator / spliterator: not priority order; weakly consistent
  drainTo: can drain in priority order
  null forbidden
```

**Listing 2.** Iterator vs `take` is a different contract. For a sorted snapshot, `Arrays.sort(pq.toArray())`.

```d2
direction: down
put: "put / offer\nnever blocks on capacity" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
heap: "head = least under Comparator\nor natural order" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
take: "take\nwaits if empty" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
iter: "iterator()\nany order" {
  width: 220
  height: 60
  style.fill: "#ffebee"
}

put -> heap
heap -> take
heap -> iter
```

**Fig. 1.** Back-pressure is not this type. `ArrayBlockingQueue` is the bounded FIFO buffer.

`PriorityQueue` is the non-thread-safe heap: `poll` does not wait. This class is the concurrent, blocking-retrieve counterpart — still unbounded, still no `null`.

> [!warning] “Highest priority first” and “put waits when full”
> Natural order takes the **least** element. Reverse the comparator if larger means more urgent. `put` never provides back-pressure; a fast producer can exhaust memory. Walking `iterator()` is not the same sequence as repeated `take`. Ties are arbitrary unless you encode them. `null` is `NullPointerException`, not a valid job.

> [!tip] Interview answer
> **`PriorityBlockingQueue` is an unbounded blocking priority queue with the same ordering as `PriorityQueue`.** The head is the least element; `take` waits when empty; `put` never waits. Iterators are not in priority order. It is not a bounded FIFO queue and not “highest first” unless you write the comparator that way.
