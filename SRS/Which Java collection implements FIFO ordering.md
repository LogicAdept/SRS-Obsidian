<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #SRS

# Which Java collection implements FIFO ordering?

> [!abstract] Short answer
> **Typical `Queue`s — use `ArrayDeque`.** FIFO means first-in, first-out: insert at the tail, take from the head. `Queue` is **typically** FIFO, not always: `PriorityQueue` is a `Queue` whose head is **least**, not oldest. A `Deque` used as a `Queue` **is** FIFO. Concurrent FIFO: `ConcurrentLinkedQueue`; bounded FIFO: `ArrayBlockingQueue`.

## FIFO is a policy, not “the `Queue` class”

`Queue` holds elements prior to processing. Ordering is **typically, but not necessarily, FIFO**. The **head** is whatever `remove()` / `poll()` would take. In a FIFO queue, new elements go at the **tail**; retrieval takes the longest-waiting element [[What is the Queue interface in Java]] [[What is the difference between a Queue and a Stack]].

`Deque` extends `Queue`. Used as a queue, **FIFO results**: add last, remove first (`offer`→`offerLast`, `poll`→`pollFirst`) [[What is the Deque interface in Java]] [[How does the Queue interface differ from the Deque interface]].

Concrete FIFO types:

- `ArrayDeque` — usual resizable `Deque`/`Queue` (faster than `LinkedList` as a queue)
- `LinkedList` as a `Queue` — FIFO via the same map; also a `List` [[Does LinkedList implement Queue and Deque in Java]]
- `ConcurrentLinkedQueue` — unbounded concurrent FIFO [[What is ConcurrentLinkedQueue]]
- `ArrayBlockingQueue` / `LinkedBlockingQueue` — document FIFO; head = longest present [[What is the difference between ArrayBlockingQueue and LinkedBlockingQueue]]

**Not FIFO:** `PriorityQueue` / `PriorityBlockingQueue` (least under the ordering); `DelayQueue` (expired delay, not arrival) [[What is java.util.PriorityQueue]] [[What is a PriorityBlockingQueue]] [[What is a DelayQueue]].

```d2
direction: down
fifo: "FIFO Queue\ninsert last, poll first" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
ad: "ArrayDeque, LinkedList\nCLQ, ArrayBlockingQueue" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
not: "PriorityQueue\nhead = least, not oldest" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}

fifo -> ad
fifo -> not: "Queue, not FIFO"
```

**Fig. 1.** Name a FIFO implementation (`ArrayDeque`). Do not say “`Queue` always means FIFO.”

```java
import java.util.ArrayDeque;
import java.util.PriorityQueue;
import java.util.Queue;

class FifoVsPriority {
    static void demo() {
        Queue<Integer> fifo = new ArrayDeque<>();
        fifo.offer(3);
        fifo.offer(1);
        System.out.println(fifo.poll()); // 3 — first in

        Queue<Integer> pq = new PriorityQueue<>();
        pq.offer(3);
        pq.offer(1);
        System.out.println(pq.poll()); // 1 — least, not FIFO
    }
}
```

**Listing 1.** Java 5+. Same `Queue` type, two policies. `ArrayDeque` is FIFO; `PriorityQueue` is not.

> [!warning] `Queue` is not automatically FIFO
> The interface allows other orders. `PriorityQueue` implements `Queue` and is not first-in, first-out.

> [!warning] `Deque` as a stack is LIFO
> Typed as `Deque`, `push`/`pop` are first-end operations. FIFO is the **`Queue` method map**, not every use of `ArrayDeque`.

> [!tip] Interview answer
> **FIFO queues insert last and take the oldest: `ArrayDeque` is the usual choice** (`LinkedList` as `Queue`, `ConcurrentLinkedQueue`, `ArrayBlockingQueue` too). **`Queue` is typically FIFO, not always — `PriorityQueue` is the counterexample.** A `Deque` used as a `Queue` is FIFO.
