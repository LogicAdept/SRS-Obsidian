<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #SRS

# How would you explain `Queue extends Deque` or `Deque extends Queue`?

> [!abstract] Short answer
> **`Deque` extends `Queue` — never the other way around.** The signature is `interface Deque extends Queue`. Every deque is a queue (FIFO if you use the inherited methods). A queue is **not** a deque: `PriorityQueue` implements `Queue` only. `Deque` adds the other end (and can be a LIFO stack). Both generally keep **identity** `equals` / `hashCode`.

## The subtype has both ends

`Deque` (“deck”, double-ended queue) is declared `extends Queue, SequencedCollection`. Since **1.6**; `Queue` is **1.5**. You may pass a `Deque` anywhere a `Queue` is required. You may **not** assign a `Queue` to a `Deque` [[How does the Queue interface differ from the Deque interface]] [[What is the Queue interface in Java]] [[What is the Deque interface in Java]].

`Queue` holds elements prior to processing. Remove/examine hit the **head** (`remove` / `poll` / `element` / `peek`). Ordering is **typically FIFO** (insert last, take first) but **need not be** — `PriorityQueue` orders by natural order or a `Comparator`; its head is the **least** element, not the oldest [[What is the difference between a Queue and a Stack]].

`Deque` is a linear collection with insert/remove/examine at **both** ends. Inherited `Queue` methods are the FIFO map: `add`→`addLast`, `poll`→`pollFirst`, and so on. The same object can be a LIFO stack: `push`/`pop` at **first**. Implementations include `ArrayDeque` and `LinkedList`. `PriorityQueue` and `ConcurrentLinkedQueue` are `Queue` only [[What are the First and Last methods on Deque]] [[Does LinkedList implement Queue and Deque in Java]].

`Queue` and `Deque` implementations **generally** do not define element-based `equals` / `hashCode`; they inherit identity from `Object`. Two equal-content deques are not `equals` unless they are the same instance [[Do Queue and Deque implementations override equals]].

```d2
direction: down
q: "Queue (1.5)\nhead insert/remove/examine" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
d: "Deque extends Queue (1.6)\nboth ends; FIFO or LIFO" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
pq: "PriorityQueue\nQueue, not Deque" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}

q -> d
q -> pq
```

**Fig. 1.** Inheritance runs `Deque` → `Queue`. `PriorityQueue` sits on `Queue` only.

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.PriorityQueue;
import java.util.Queue;

class DequeExtendsQueue {
    static void demo() {
        Deque<String> d = new ArrayDeque<>();
        Queue<String> q = d; // OK — Deque is-a Queue
        q.offer("a");
        q.offer("b");
        System.out.println(q.poll()); // a — FIFO via Queue methods
        // Deque<String> no = q;      // does not compile

        Queue<Integer> pq = new PriorityQueue<>();
        pq.offer(3);
        pq.offer(1);
        System.out.println(pq.poll()); // 1 — least, still not a Deque
    }
}
```

**Listing 1.** Java 6+. A `Deque` assigns to `Queue`. The reverse assignment does not compile. `PriorityQueue` is a `Queue` that is not a `Deque`.

> [!warning] `Queue` does not extend `Deque`
> The dump’s other wording is the trap. `interface Deque extends Queue`. A `Queue` parameter accepts `ArrayDeque`; it does not give you `addFirst`.

> [!warning] FIFO is how you *use* a `Deque` as a `Queue`
> It is not the only `Queue` ordering. `PriorityQueue` is a `Queue` whose head is least, not first-in.

> [!tip] Interview answer
> **`Deque` extends `Queue`.** A deque is a queue plus the other end (FIFO as a queue, LIFO as a stack). **A `Queue` is not a `Deque`** — `PriorityQueue` proves it. Both types usually keep `Object` identity `equals` / `hashCode`.
