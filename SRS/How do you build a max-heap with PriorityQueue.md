<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #DSA/DataStructures/Heap #SRS

# How do you build a max-heap with `PriorityQueue`?

> [!abstract] Short answer
> **Pass a reverse comparator at construction.** The head is always the **least** element under the queue’s ordering, so the default (natural order) is a **min-heap**. `new PriorityQueue<>(Comparator.reverseOrder())` — or, before the Java 8 comparator-only constructor, `new PriorityQueue<>(capacity, Collections.reverseOrder())` — makes that “least” the **greatest** natural value. For a field, reverse the key comparator (`comparingInt(...).reversed()`), not the key extractor alone.

## Head is least — flip the order

`PriorityQueue` orders by natural ordering **or** a `Comparator` supplied **at construction**. `poll` / `remove()` / `peek` / `element` always access the head: the least element under that ordering. Ties at the head are broken arbitrarily [[What is java.util.PriorityQueue]] [[What is the difference between java.lang.Comparable and java.util.Comparator]].

There is no `setComparator`. OpenJDK stores `private final Comparator`; `comparator()` returns it or `null` for natural order. To get a max-heap you choose the ordering up front.

`Comparator.reverseOrder()` (Java 8) returns a comparator that imposes the **reverse of natural ordering**. `Collections.reverseOrder()` is the same idea and works with `PriorityQueue(int, Comparator)` (the capacity+comparator constructor, Java 5). Under reverse natural order, the least element is the largest `compareTo` value, so `poll()` yields a max-heap sequence.

```d2
direction: down
ctor: "constructor ordering" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
nat: "natural / comparingInt(key)\nhead = least key" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
rev: "reverseOrder() / .reversed()\nhead = greatest key" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

ctor -> nat: "default"
ctor -> rev: "max-heap"
```

**Fig. 1.** Same heap API. “Max” means the comparator’s least element is the value you want to `poll` first.

```java
import java.util.Collections;
import java.util.Comparator;
import java.util.PriorityQueue;

class MaxHeapWithPriorityQueue {
    static void demo() {
        PriorityQueue<Integer> max = new PriorityQueue<>(Comparator.reverseOrder());
        max.offer(1);
        max.offer(9);
        max.offer(5);
        System.out.println(max.poll()); // 9

        PriorityQueue<Integer> alsoMax =
            new PriorityQueue<>(11, Collections.reverseOrder()); // Java 5 shape

        PriorityQueue<Task> urgentFirst = new PriorityQueue<>(
            Comparator.comparingInt(Task::priority).reversed());
        urgentFirst.offer(new Task("low", 1));
        urgentFirst.offer(new Task("high", 10));
        System.out.println(urgentFirst.poll().name); // high
    }

    static final class Task {
        final String name;
        final int priority;
        Task(String name, int priority) {
            this.name = name;
            this.priority = priority;
        }
        int priority() { return priority; }
    }
}
```

**Listing 1.** `Comparator.reverseOrder()` and `PriorityQueue(Comparator)` are Java 8. `new PriorityQueue<>(11, Collections.reverseOrder())` is the Java 5 constructor. `comparingInt(Task::priority)` alone is still a **min**-heap on that `int`; `.reversed()` flips it.

Natural order still requires mutually comparable elements or `offer`/`add` may throw `ClassCastException`. `reverseOrder()` also throws `NullPointerException` on `null` arguments; `PriorityQueue` already forbids `null` elements [[What does PriorityQueue require of its elements]] [[Does PriorityQueue allow null]].

Iteration, `toString`, and `toArray` still walk the heap array, not descending keys. Drain with `poll` (or sort a copy) if you need max-to-min order [[Does iterating a PriorityQueue return elements in sorted order]].

> [!warning] Default is smallest-first
> `new PriorityQueue<Integer>()` polls `1` before `9`. Interview default is a min-heap. Forgetting `reverseOrder()` is the usual max-heap miss.

> [!warning] `comparingInt(key)` is not a max-heap
> It compares the extracted `int` in natural order, so the **smallest** key is the head. For largest-key-first, chain `.reversed()` (or `Collections.reverseOrder(thatComparator)`). You cannot swap the comparator on an existing queue.

> [!tip] Interview answer
> **Default `PriorityQueue` is a min-heap: the head is the least element under natural order.** For a max-heap, construct it with `Comparator.reverseOrder()` (or `Collections.reverseOrder()`). **The comparator is fixed at construction.** A key extractor still needs `.reversed()` if the high value should come out first.
