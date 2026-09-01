<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #DSA/DataStructures/Heap #SRS

# What is `java.util.PriorityQueue`?

> [!abstract] Short answer
> **An unbounded priority queue based on a priority heap** (`Queue`, Java 5). The head is the **least** element under natural order or a `Comparator` given at construction. No `null`. `offer`/`poll` are O(log n); `peek` is O(1). Iteration is **not** sorted. Not synchronized — use `PriorityBlockingQueue` if threads mutate it.

## Heap-backed `Queue`, least at the head

`PriorityQueue` extends `AbstractQueue` and implements `Queue` (not `Deque`). Elements follow **natural ordering** or a constructor `Comparator`. Retrieval (`poll`, `remove()`, `peek`, `element`) always hits the head: the least element under that ordering. Equal-least ties are broken **arbitrarily** [[What is a heap as a data structure]] [[What happens when two PriorityQueue elements have equal priority]] [[How would you explain extends Queue extends Deque or Deque extends Queue]].

Natural order requires mutually comparable elements (`ClassCastException` otherwise). `null` is forbidden (`offer` / `add` → `NullPointerException`). Default least-first is what interviews call a **min-heap**; `Comparator.reverseOrder()` — or `comparingInt(...).reversed()` on a field — flips it [[What does PriorityQueue require of its elements]] [[Does PriorityQueue allow null]] [[Why do most Queue implementations forbid null]] [[How do you build a max-heap with PriorityQueue]].

The queue is **unbounded**; an internal array capacity grows as needed (growth policy unspecified; default constructor capacity 11). Documented times: O(log n) `offer`, `poll`, `remove()`, `add`; linear `remove(Object)` / `contains`; constant `peek`, `element`, `size` [[What are the time complexities of PriorityQueue operations]].

`iterator()` / `spliterator()` have **no** particular order — `Arrays.sort(pq.toArray())` for a sorted snapshot. That is a heap, not a `TreeSet` [[Does iterating a PriorityQueue return elements in sorted order]] [[What is the difference between PriorityQueue and TreeSet]].

Not synchronized. Concurrent modification needs `PriorityBlockingQueue` (same ordering, blocking `take`, logically unbounded) [[Is PriorityQueue thread-safe]] [[What is a PriorityBlockingQueue]].

```d2
direction: down
pq: "PriorityQueue\nQueue, not Deque" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
heap: "priority heap\nhead = least" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
ops: "offer/poll O(log n)\npeek O(1)" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}

pq -> heap
heap -> ops
```

**Fig. 1.** Type shape: heap-backed `Queue`. Only the head is the least element.

```java
import java.util.Comparator;
import java.util.PriorityQueue;

class WhatIsPriorityQueue {
    static void demo() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.offer(3);
        pq.offer(1);
        pq.offer(2);
        System.out.println(pq.peek()); // 1 — least
        System.out.println(pq.poll()); // 1
        System.out.println(pq.poll()); // 2
        // pq.offer(null);             // NullPointerException

        PriorityQueue<Integer> max = new PriorityQueue<>(Comparator.reverseOrder());
        max.offer(1);
        max.offer(3);
        System.out.println(max.poll()); // 3 — greatest under reverseOrder
    }
}
```

**Listing 1.** Default natural order is Java 5+. The `Comparator`-only constructor is Java 8+. `poll` is least-first; `reverseOrder()` makes the head the greatest natural value. A for-each over `pq` is not guaranteed sorted.

> [!warning] Not a sorted collection
> `iterator()` is unordered. Drain with `poll`, or sort a copy. Default is **smallest-first**, not a max-heap.

> [!warning] Not thread-safe
> One mutating thread at a time unless you use `PriorityBlockingQueue`.

> [!tip] Interview answer
> **`PriorityQueue` is Java’s unbounded heap `Queue`: head is least under natural order or a constructor `Comparator`.** O(log n) insert/remove, O(1) peek, no `null`. **Iteration is not sorted; the class is not synchronized.**
