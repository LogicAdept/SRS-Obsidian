<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #Java/Collections/Concurrency #SRS

# What is the difference between a bounded and an unbounded queue?

> [!abstract] Short answer
> **A bounded queue has a fixed maximum number of elements; an unbounded one grows until memory runs out.** On a full bounded queue, `offer` returns `false`, `add` throws `IllegalStateException`, and `BlockingQueue.put` waits. Unbounded types (`ArrayDeque`, `PriorityQueue`, `ConcurrentLinkedQueue`, default `LinkedBlockingQueue`) do not reject inserts for capacity. “Array-backed” is not “bounded.”

## Capacity restriction versus grow-as-needed

The `Queue` `offer` method exists for **capacity-restricted** implementations: insert if possible, otherwise `false`. `add` is the throwing form (`IllegalStateException` when there is no space). In most implementations insert cannot fail. `BlockingQueue` adds waiting: `put` waits for space; `remainingCapacity` is extra slots you can `put` without blocking, or `Integer.MAX_VALUE` when there is **no intrinsic limit**. [[How do you implement producer-consumer with a BlockingQueue]]

**Bounded (fixed cap).** `ArrayBlockingQueue` is a classic bounded buffer: capacity set at construction and never changed; `put` on full blocks; `take` on empty blocks. `LinkedBlockingQueue(int capacity)` is the same idea with linked nodes. `SynchronousQueue` reports `remainingCapacity` **0** — not even one slot; that is a rendezvous, not an N-element buffer. [[What is the difference between ArrayBlockingQueue and LinkedBlockingQueue]] [[What is a SynchronousQueue]]

**Unbounded (no cap, memory aside).** `ArrayDeque` is a resizable array with **no capacity restrictions**; it grows as needed (initial array size is not a max). `PriorityQueue` and `ConcurrentLinkedQueue` are unbounded: `offer` never returns `false`. `new LinkedBlockingQueue()` uses capacity `Integer.MAX_VALUE` — the producer will not wait on a full buffer. `PriorityBlockingQueue` / `DelayQueue`: `put` never blocks; additions can still fail with `OutOfMemoryError`. [[What is ConcurrentLinkedQueue]] [[What is a PriorityBlockingQueue]]

```java
import java.util.ArrayDeque;
import java.util.Queue;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

class Demo {
    static void contrast() {
        Queue<Integer> unbounded = new ArrayDeque<>();
        unbounded.offer(1); // grows; not a max of 16

        BlockingQueue<Integer> bounded = new ArrayBlockingQueue<>(2);
        bounded.offer(1);
        bounded.offer(2);
        boolean third = bounded.offer(3); // false — full
        // bounded.add(3); → IllegalStateException
        // bounded.put(3); waits for a take (InterruptedException)
    }
}
```

**Listing 1.** `offer` is the non-throwing probe. `put` is back-pressure. `ArrayDeque`’s constructor capacity is a starting array, not a ceiling.

```d2
direction: down
q: "Insert when the queue looks full?" {
  width: 300
  height: 60
  style.fill: "#e3f2fd"
}
unb: "unbounded\ngrow / OOM" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
bnd: "bounded BlockingQueue" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
off: "offer → false\nadd → ISE\nput → wait" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}

q -> unb
q -> bnd
bnd -> off
```

**Fig. 1.** Bounds are how you get back-pressure. An unbounded concurrent queue will not slow the producer.

A hand-rolled bounded buffer (`wait`/`notify` around an array) is the same protocol `ArrayBlockingQueue` already implements. [[How do you implement a bounded buffer with synchronized in Java]]

> [!warning] Default `LinkedBlockingQueue` and `ArrayDeque` are not capped
> `new LinkedBlockingQueue()` is not a bounded buffer — capacity is `Integer.MAX_VALUE`. `new ArrayDeque<>(n)` still grows past `n`. `remainingCapacity() == Integer.MAX_VALUE` means “no intrinsic limit,” not “a huge but real cap you should fill.” `SynchronousQueue` is capacity 0, not “unbounded.” Unbounded `put`/`offer` can still exhaust the heap.

> [!tip] Interview answer
> **Bounded queues have a max size: `offer` fails, `add` throws, `put` waits.** Unbounded queues grow until memory: `ArrayDeque`, `ConcurrentLinkedQueue`, default `LinkedBlockingQueue`. `ArrayBlockingQueue` is the classic bounded buffer. An array inside the class does not make it bounded — `ArrayDeque` grows.
