<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #Java/Collections/Queues/PriorityQueue #SRS

# What is the difference between PriorityQueue and TreeSet?

> [!abstract] Short answer
> **`PriorityQueue` is a heap `Queue`: duplicates allowed, only the head is ordered, `poll`/`peek` are the access path.** **`TreeSet` is a `NavigableSet`: unique by comparator, the whole set is sorted, and you get range views and `ceiling` / `floor`.** Both can take a `Comparator`. Neither permits `null` under natural ordering. They are not interchangeable “sorted collections.”

## Heap queue vs sorted set

`PriorityQueue` (1.5) is an unbounded **priority heap**. The head is the **least** element under natural order or a constructor `Comparator`. Ties for least are broken **arbitrarily**. `poll`, `remove()`, `peek`, and `element` talk only to that head. `add` / `offer` always insert (`add` returns `true`); two `equals` elements are both kept. `contains(Object)` / `remove(Object)` use `equals` and are **linear**. Enqueue/dequeue (`offer`, `poll`, `add`, `remove()`) are **O(log n)**; `peek` / `size` are constant. No `null`.

`TreeSet` (1.2) is a `NavigableSet` on a `TreeMap`. `add` / `remove` / `contains` are **guaranteed log(n)**. A second element that compares equal is **dropped** (`add` returns `false`). Iteration is **ascending**. You get `headSet` / `tailSet` / `subSet`, `lower` / `floor` / `ceiling` / `higher`, `pollFirst` / `pollLast` ([[What do TreeSet headSet tailSet and subSet return]]). Comparator must be consistent with `equals` to honor the `Set` contract.

```d2
direction: right
pq: "PriorityQueue\nheap Queue\nduplicates OK\nonly head is ordered" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
ts: "TreeSet\nNavigableSet / TreeMap\nunique\nfull sorted order + ranges" {
  width: 300
  height: 110
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Same comparator idea, different ADT. Repeated `poll` drains a PQ in priority order; a single `iterator()` on the PQ does **not**.

```java
PriorityQueue<Integer> pq = new PriorityQueue<>(Comparator.reverseOrder());
pq.addAll(List.of(5, 1, 5));
pq.poll();           // 5 — reverseOrder head is the largest
pq.size();           // 2 — the other 5 is still there

TreeSet<Integer> ts = new TreeSet<>(Comparator.reverseOrder());
ts.addAll(List.of(5, 1, 5));
ts.size();           // 2 — {5, 1}; second 5 was rejected
ts.first();          // 5
```

**Listing 1.** Two `5`s survive in the queue. The set keeps one. `pq.iterator()` is not required to yield 5, 5, 1.

## Iteration, views, threads

The PQ `iterator()` / `spliterator()` are **not guaranteed** to traverse in any particular order. For ordered traversal, `Arrays.sort(pq.toArray())` ([[Does iterating a PriorityQueue return elements in sorted order]]). `toArray()` is “no particular order.”

A `TreeSet` iterator is sorted. Range views are live. There is no PQ equivalent of `subSet`.

Neither class is synchronized. Concurrent PQ use is `PriorityBlockingQueue`; concurrent sorted set is `ConcurrentSkipListSet` ([[What is ConcurrentSkipListSet]]).

> [!warning] Equal priority is not uniqueness
> Two PQ elements that compare equal are **both stored**; which one is head is arbitrary ([[What happens when two PriorityQueue elements have equal priority]]). In a `TreeSet` that comparison **is** equality: the second `add` is a no-op. `pq.contains` is `equals` and O(n), not the heap order.

> [!warning] Do not iterate a `PriorityQueue` expecting `TreeSet` order
> Walking `for (E e : pq)` is heap layout, not sorted order. Repeated `poll()` is the ordered consumption path, and it **empties** the queue.

> [!tip] Interview answer
> **`PriorityQueue` is a heap queue: duplicates allowed, O(log n) `offer`/`poll`, only the head is ordered, iteration is unordered.** **`TreeSet` is a unique sorted set: log(n) `contains`, full `NavigableSet` ranges, iterator is sorted.** Use the queue to consume by priority; use the set when you need uniqueness and ordered views.
