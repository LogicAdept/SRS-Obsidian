<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #Java/Collections/Iteration #SRS

# Does iterating a `PriorityQueue` return elements in sorted order?

> [!abstract] Short answer
> **No.** `iterator()`, enhanced `for`, `forEach`, `toArray`, `toString`, and `spliterator()` are **not** in priority order. Only the **head** is the least element (`peek` / `element`). Repeated `poll` / `remove()` drain in priority order; for a sorted snapshot that keeps the queue, `Arrays.sort(pq.toArray())`.

## Heap walk, not a sorted scan

`PriorityQueue` is an unbounded priority queue **based on a priority heap**. The head is the least element under natural order or the constructor `Comparator`. `poll`, `remove()`, `peek`, and `element` access that head. That is the only ordering the type promises on retrieval.

The class contract: `iterator()` and `spliterator()` are **not guaranteed to traverse in any particular order**. `iterator()` “does not return the elements in any particular order.” `toArray()` is the same: elements in **no particular order**. `spliterator()` does not report `ORDERED`. If you need ordered traversal, the API’s own recipe is `Arrays.sort(pq.toArray())` [[What is java.util.PriorityQueue]] [[How do you iterate the elements of a Java collection]].

OpenJDK stores the heap in a balanced binary array: children of `queue[n]` are `queue[2*n+1]` and `queue[2*(n+1)]`; for every node `n` and descendant `d`, `n <= d`; the least element sits at `queue[0]`. That is a **partial** order (parent before children), not a fully sorted array. `Itr.next()` returns `queue[cursor++]` — a linear scan of that array, not a sequence of `poll`s. `toArray()` is `Arrays.copyOf(queue, size)`, so it is the same heap layout. `toString()` is inherited from `AbstractCollection`: it prints elements **in iterator order**, so the debugger string is a heap dump, not a sorted list.

```d2
direction: down
heap: "backing heap array\nparent ≤ children; index 0 is head" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
walk: "iterator / toString / toArray\nindex 0 … size-1" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
drain: "poll / remove()\nleast remaining each time" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

heap -> walk: "not sorted"
heap -> drain: "priority order, mutates"
```

**Fig. 1.** Same structure, two encounters: array index order versus successive head removal.

```java
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;

class PriorityQueueIteration {
    static void demo() {
        PriorityQueue<Integer> pq = new PriorityQueue<>(List.of(5, 1, 3, 2, 4));
        System.out.println(pq); // OpenJDK heap walk, e.g. [1, 2, 3, 5, 4]

        Object[] snapshot = pq.toArray();
        Arrays.sort(snapshot);  // [1, 2, 3, 4, 5] — queue unchanged

        while (!pq.isEmpty()) {
            System.out.print(pq.poll()); // 12345 — empties the queue
        }
    }
}
```

**Listing 1.** Java 9+ `List.of` into `PriorityQueue(Collection)` heapifies; OpenJDK’s array for this input is `[1, 2, 3, 5, 4]`. That print is **not** an API guarantee — another heap shape is legal. `poll` until empty is sorted and destructive. `Arrays.sort` on a `toArray()` copy is the documented non-destructive walk.

A tiny heap can *look* sorted (`[1, 2]`); that is still not a traversal contract. Contrast `Deque.iterator()`, which **is** head-to-tail [[How can you iterate a Deque in both directions]]. `PriorityQueue` has no `descendingIterator`. A max-heap (`Comparator.reverseOrder()`) still iterates the heap array, not descending keys [[How do you build a max-heap with PriorityQueue]].

OpenJDK’s iterator is fail-fast (`modCount`); the documented `spliterator()` is late-binding and fail-fast. Do not treat fail-fast as a reason the walk would be sorted.

> [!warning] `toString` and for-each are the interview trap
> Printing a `PriorityQueue` or writing `for (E e : pq)` does **not** yield priority order. The string is iterator order over the heap. Do not “prove” sort by glancing at `pq.toString()`.

> [!warning] `poll` until empty is sorted and destructive
> Draining is the retrieval contract, not a view. After the loop the queue is empty. Keep a copy, or sort `toArray()`, when you still need the queue.

> [!tip] Interview answer
> **No. Iteration, `toString`, and `toArray` walk the heap, which is only partially ordered.** The head is the least element; **`poll` / `remove()` repeatedly give priority order and empty the queue.** For a sorted snapshot, **`Arrays.sort(pq.toArray())`.**
