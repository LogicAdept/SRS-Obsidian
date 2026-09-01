<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #SRS

# How would you explain what `PriorityQueue` allows you to do?

> [!abstract] Short answer
> **Always take the current least element.** Order is natural ordering or a `Comparator` given **at construction** — that is how you rank objects by a property. `offer`/`poll` are O(log n); `peek` is O(1). It does **not** give a sorted list, FIFO, or `null` elements.

## Rank the head, not sort the collection

`PriorityQueue` is an unbounded heap-backed `Queue`. What it adds over a FIFO queue is **priority**: `poll` / `remove()` / `peek` / `element` always access the **least** element under the queue’s ordering [[What is java.util.PriorityQueue]].

You choose that ordering once:

- default constructors → **natural ordering** (`Comparable`)
- `new PriorityQueue<>(comparator)` (or capacity + comparator) → custom order, including a field (`comparingInt(...)`) or a max-heap (`reverseOrder()`) [[What does PriorityQueue require of its elements]] [[How do you build a max-heap with PriorityQueue]]

That is “store objects by a property”: the comparator is the property. Ties for least are broken **arbitrarily** [[What happens when two PriorityQueue elements have equal priority]].

It does **not** walk in sorted order. `iterator()` has no particular order; drain with `poll` or sort a `toArray()` copy [[Does iterating a PriorityQueue return elements in sorted order]] [[What is the difference between PriorityQueue and TreeSet]].

`null` is not an element (`offer`/`add` → `NullPointerException`). Costs: O(log n) `offer`/`poll`/`add`/`remove()`, O(1) `peek`/`element`/`size` [[Does PriorityQueue allow null]] [[What are the time complexities of PriorityQueue operations]].

```d2
direction: down
order: "natural order or Comparator\nat construction" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
head: "head = least under that order\npeek O(1)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
poll: "poll\nO(log n) — next least" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}

order -> head
head -> poll
```

**Fig. 1.** The capability is repeated least-first retrieve, not a sorted view of all elements.

```java
import java.util.Comparator;
import java.util.PriorityQueue;

class Job {
    final String name;
    final int urgency;
    Job(String name, int urgency) {
        this.name = name;
        this.urgency = urgency;
    }
}

class WhatPriorityQueueAllows {
    static void demo() {
        PriorityQueue<Job> q = new PriorityQueue<>(Comparator.comparingInt(j -> j.urgency));
        q.offer(new Job("later", 10));
        q.offer(new Job("now", 1));
        System.out.println(q.poll().name); // now — least urgency
        System.out.println(q.peek().name); // later
        // q.offer(null);                  // NullPointerException
    }
}
```

**Listing 1.** Java 8+. `comparingInt` ranks by a field. `poll` returns that least job. Default `PriorityQueue<Integer>` would use natural order instead.

> [!warning] This is not “the collection is sorted”
> Heap order is only guaranteed at the head. A for-each loop is not priority order. `TreeSet` is the sorted-set type.

> [!warning] Dijkstra is not a `PriorityQueue` feature
> A shortest-path algorithm can *use* a min-priority queue. The class contract is heap-backed least-first `Queue` operations, not graph APIs.

> [!tip] Interview answer
> **`PriorityQueue` lets you always retrieve the current least element**, under natural order or a constructor `Comparator` (a field, or reversed for a max-heap). **That is priority, not FIFO and not a sorted list.** No `null`; `offer`/`poll` are O(log n).
