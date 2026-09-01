<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #Java/Collections/Set/TreeSet #SRS

# What happens when two `PriorityQueue` elements have equal priority?

> [!abstract] Short answer
> **Both stay in the queue.** If several elements are tied for least, the head is **one of them — ties are broken arbitrarily.** `poll` / `remove()` / `peek` / `element` see that head. That is **not** a random shuffle, **not** FIFO, and **not** `TreeSet` uniqueness (`compare == 0` does not drop the second insert).

## Arbitrary among current minima — not a lottery

The head is the least element under the constructor ordering (natural order or a `Comparator`). If multiple elements are tied for least, the head is one of those elements; **ties are broken arbitrarily**. Retrieval (`poll`, `remove()`, `peek`, `element`) always accesses that head [[What does PriorityQueue require of its elements]].

“Arbitrarily” is the spec word: no promised insertion order, no documented `Random`. Heap repair after `offer`/`poll` can leave any current minimum at index 0. Do not write tests that assume the first-inserted equal key comes out first.

The type is a `Queue`, not a `Set`. `remove(Object)` removes **a single instance** matching `equals`. Two values that compare equal can both sit in the heap. `TreeSet` is the opposite: it compares with `compareTo`/`compare`, and two elements that method treats as equal are **equal from the set’s standpoint** — the second `add` does not introduce another occupant [[What is the difference between PriorityQueue and TreeSet]] [[Why must TreeMap ordering be consistent with equals]].

```d2
direction: down
both: "two elements, compare == 0\nboth remain in the heap" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
head: "head = one of the current minima\narbitrary which" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
poll: "poll / peek / element / remove()\nsee that head" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}

both -> head
head -> poll
```

**Fig. 1.** Equal priority keeps both items. Only the choice of **which** tied minimum sits at the head is unspecified.

To make ties deterministic, put a **secondary key** in `Comparable` / `Comparator` (sequence number, id). `Comparator.thenComparingInt` (Java 8) is enough. `PriorityBlockingQueue` uses the same ordering rules as `PriorityQueue` and documents that equal-priority order is unguaranteed unless you add such a key [[What is a PriorityBlockingQueue]] [[How do you build a max-heap with PriorityQueue]].

Iteration is still a heap walk, not “all equals together in FIFO” [[Does iterating a PriorityQueue return elements in sorted order]].

```java
import java.util.Comparator;
import java.util.PriorityQueue;

class EqualPriority {
    static void demo() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.offer(1);
        pq.offer(1);
        pq.poll(); // 1 — which of the two 1s is unspecified
        pq.poll(); // the other 1

        PriorityQueue<Job> fifoAmongTies = new PriorityQueue<>(
            Comparator.comparingInt((Job j) -> j.priority)
                .thenComparingInt(j -> j.seq));
        fifoAmongTies.offer(new Job(1, 0));
        fifoAmongTies.offer(new Job(1, 1));
        fifoAmongTies.poll(); // seq 0 — secondary key, not default PQ behavior
    }

    static final class Job {
        final int priority;
        final int seq;
        Job(int priority, int seq) {
            this.priority = priority;
            this.seq = seq;
        }
    }
}
```

**Listing 1.** Default `PriorityQueue` keeps both `1`s; which is polled first is not a FIFO contract. The `Job` comparator is an explicit tie-break you add. `TreeSet` with natural order would not hold two equal `Integer`s.

> [!warning] Not “randomly”
> Interview dumps say `poll` picks at random. The spec says **arbitrarily**: unspecified, not `java.util.Random`. Insertion order is not a tie-break unless you encode it.

> [!warning] Equal priority is not `TreeSet` collapse
> `PriorityQueue` allows duplicates. `TreeSet` treats `compare == 0` as the same set element. Do not expect the second equal-priority `offer` to be ignored.

> [!tip] Interview answer
> **Both elements stay in the `PriorityQueue`.** If they are tied for least, **`poll` returns one of them — unspecified which, not FIFO.** If you need a stable tie-break, add a secondary key to the comparator. **That is not `TreeSet`, which keeps only one element per comparison-equal key.**
