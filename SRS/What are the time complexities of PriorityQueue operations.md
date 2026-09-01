<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #SRS

# What are the time complexities of `PriorityQueue` operations?

> [!abstract] Short answer
> **Enqueue/dequeue are O(log n); looking at the head is O(1); finding or removing an arbitrary element is linear.** The implementation note: `offer` / `add` / `poll` / `remove()` are O(log n); `peek` / `element` / `size` are constant; `remove(Object)` / `contains(Object)` are linear. OpenJDK builds from a plain collection with Floyd **heapify in O(n)**, cheaper than *n* offers.

## Heap costs, two different `remove`s

`PriorityQueue` is a binary heap in an array. The head is the least element under the constructor ordering. Sift-up / sift-down along the tree height is logarithmic; a scan of the array is linear [[What is java.util.PriorityQueue]].

| Operation | Documented cost | Why |
|---|---|---|
| `offer` / `add` | O(log n) | sift up |
| `poll` / `remove()` | O(log n) | take `queue[0]`, sift down |
| `peek` / `element` / `size` | O(1) | head slot or a counter |
| `contains(Object)` / `remove(Object)` | linear | scan, then (for remove) repair the heap |

`remove()` with no argument is `Queue.remove`: dequeue the head (logarithmic). `remove(Object)` is `Collection.remove`: `indexOf` then `removeAt` — the scan dominates. Mixing those two names is the usual interview miss.

```d2
direction: down
head: "queue[0] head\npeek / element — O(1)" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
sift: "offer / poll / remove()\nO(log n) along the height" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
scan: "contains / remove(Object)\nO(n) walk of the array" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

head -> sift
sift -> scan: "no index by value"
```

**Fig. 1.** Fast “next min,” slow “is this object in the heap?”

OpenJDK `offer` is `siftUp` after an optional `grow` (array `copyOf`, same family of spike as `ArrayList` growth). `poll` sifts the last element down from index 0. `contains` / `remove(Object)` call `indexOf`, a loop over `queue[0 .. size)`.

```java
import java.util.List;
import java.util.PriorityQueue;

class PriorityQueueCosts {
    static void demo() {
        PriorityQueue<Integer> oneByOne = new PriorityQueue<>();
        oneByOne.offer(7);     // O(log n) each; n offers → O(n log n)
        oneByOne.offer(1);
        oneByOne.peek();       // O(1) — head is 1
        oneByOne.remove(7);    // O(n) — search, not dequeue
        oneByOne.remove();     // O(log n) — dequeue remaining head

        PriorityQueue<Integer> bulk = new PriorityQueue<>(List.of(5, 1, 3, 2, 4));
        // OpenJDK heapify: O(n), not n × offer
    }
}
```

**Listing 1.** `remove(7)` is the linear `Collection` method. `remove()` is logarithmic dequeue. `PriorityQueue(Collection)` on a non-`PriorityQueue` / non-`SortedSet` copies then `heapify()` — OpenJDK comments Floyd (1964) as **O(size)**. Copying an existing `PriorityQueue` or `SortedSet` is an array copy of an already valid heap, still O(n) elements, no per-element sift-up.

n successive `offer`s remain O(n log n). Use the collection constructor when the data is already in hand. Iteration / `toArray` still walk the heap, not sorted order [[Does iterating a PriorityQueue return elements in sorted order]]. A reverse comparator does not change these bounds [[How do you build a max-heap with PriorityQueue]].

> [!warning] `remove()` vs `remove(Object)`
> Head `remove()` is O(log n). Arbitrary `remove(o)` is O(n). Saying “remove is log n” without the signature is false for the `Object` overload.

> [!warning] n inserts are not heapify
> A loop of `offer` is O(n log n). The collection constructor’s Floyd heapify is O(n). Heaps answer “give me the min”; they do not answer “find this element” in log time.

> [!tip] Interview answer
> **`offer`/`add`/`poll`/`remove()` are O(log n); `peek`/`element`/`size` are O(1); `contains` and `remove(Object)` are O(n).** Building from a collection is O(n) heapify, not n log n. **The two `remove` methods are different costs.**
