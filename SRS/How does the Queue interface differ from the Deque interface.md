<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #SRS

# How does the `Queue` interface differ from the `Deque` interface?

> [!abstract] Short answer
> **`Deque` extends `Queue` and adds the other end.** A `Queue` inserts into the collection and removes/examines only the **head**. A `Deque` (“deck”) inserts, removes, and examines at **both** ends (twelve methods). Used as a `Queue`, a deque is FIFO. Used as a stack, it is LIFO. Every `Deque` is a `Queue`; **not** every `Queue` is a `Deque` (`PriorityQueue`).

## Head-only vs both ends

`Deque` is a linear collection with insertion and removal at **both** ends. It **extends `Queue`**. The name is short for double-ended queue, pronounced “deck.” Since **1.6** (`Queue` is 1.5). It also extends `SequencedCollection` [[What is the Queue interface in Java]] [[What is the Deque interface in Java]].

A `Queue` still has two method families (throw vs special value) for insert, remove-head, and examine-head: `add`/`offer`, `remove`/`poll`, `element`/`peek` [[What are the two method families on Queue]]. Ordering is **typically FIFO**, but need not be: the head is whatever `remove`/`poll` would take (`PriorityQueue`: least element).

`Deque` repeats those two families at **first** and **last**:

| | First (head) | Last (tail) |
|---|---|---|
| Insert | `addFirst` / `offerFirst` | `addLast` / `offerLast` |
| Remove | `removeFirst` / `pollFirst` | `removeLast` / `pollLast` |
| Examine | `getFirst` / `peekFirst` | `getLast` / `peekLast` |

Inherited `Queue` methods are **exactly** the FIFO map: `add`→`addLast`, `poll`→`pollFirst`, `peek`→`peekFirst`, and so on. Stack `push`/`pop`/`peek` are **first**-end operations. `peek` always looks at the beginning, whether the deque is used as a queue or a stack [[What are the First and Last methods on Deque]] [[What is the difference between a Queue and a Stack]].

`Deque` also has `removeFirstOccurrence` / `removeLastOccurrence` and `descendingIterator`. It does **not** offer `List` indexes.

Implementations that are `Queue` only include `PriorityQueue` and `ConcurrentLinkedQueue`. `ArrayDeque` and `LinkedList` are `Deque`s (hence `Queue`s) [[Does LinkedList implement Queue and Deque in Java]] [[How can you iterate a Deque in both directions]].

```d2
direction: down
q: "Queue (1.5)\ninsert; remove/examine head" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
d: "Deque (1.6) extends Queue\nfirst and last — twelve methods" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
fifo: "as Queue: add last, poll first" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
lifo: "as stack: push/pop first" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}

q -> d
d -> fifo
d -> lifo
```

**Fig. 1.** `Deque` is a `Queue` plus the other end. FIFO and LIFO are how you *use* those ends.

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.PriorityQueue;
import java.util.Queue;

class QueueVsDeque {
    static void demo() {
        Queue<Integer> q = new ArrayDeque<>();
        q.offer(1);
        q.offer(2);
        System.out.println(q.poll()); // 1 — FIFO via Queue methods

        Deque<Integer> d = new ArrayDeque<>();
        d.offerLast(1);
        d.offerLast(2);
        d.offerFirst(0);
        System.out.println(d.pollFirst()); // 0
        System.out.println(d.pollLast());  // 2

        Queue<Integer> pq = new PriorityQueue<>();
        pq.offer(3);
        pq.offer(1);
        System.out.println(pq.poll()); // 1 — least; not a Deque
        // Deque<Integer> no = pq;     // does not compile
    }
}
```

**Listing 1.** Java 6+. `ArrayDeque` as `Queue` is FIFO. The same type as `Deque` exposes both ends. `PriorityQueue` is a `Queue` that is **not** a `Deque`.

> [!warning] A `Queue` variable is not both ends
> `offer`/`poll` on a `Deque` typed as `Queue` are last-in / first-out only. Use `offerFirst` / `pollLast` (or a `Deque` reference) for the other end.

> [!warning] Not every `Queue` is a `Deque`
> `PriorityQueue` and `ConcurrentLinkedQueue` implement `Queue` only. You cannot assign them to `Deque`.

> [!tip] Interview answer
> **`Deque` extends `Queue` and operates at both ends; `Queue` only defines the head (plus insert).** A deque used as a queue is FIFO; used as a stack, LIFO — prefer it to legacy `Stack`. **Every `Deque` is a `Queue`; `PriorityQueue` is a `Queue` that is not a `Deque`.**
