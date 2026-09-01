<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #SRS

# What is the `Queue` interface in Java?

> [!abstract] Short answer
> **A collection for holding elements prior to processing** (Java 5). Besides `Collection`, it adds insert, remove-head, and examine-head, each in a **throwing** form and a **special-value** form (`offer` / `poll` / `peek`). Ordering is **typically FIFO**, but need not be (`PriorityQueue`). The **head** is whatever `remove`/`poll` would take. Generally no `null`.

## Head operations, two families

`Queue` extends `Collection`. Insert, extract, and inspect exist in two forms: one throws if it cannot complete; the other returns `false` or `null`. Special-value **insert** is for capacity-restricted queues; on most implementations insert cannot fail [[What are the two method families on Queue]].

| | Throws | Special value |
|---|---|---|
| Insert | `add(e)` → `IllegalStateException` if full | `offer(e)` → `false` |
| Remove head | `remove()` → `NoSuchElementException` if empty | `poll()` → `null` |
| Examine head | `element()` → `NoSuchElementException` if empty | `peek()` → `null` |

`offer` exists because a full bounded buffer is a **normal** outcome, not a bug (`Collection.add` may only fail by throwing). `poll`/`peek` returning `null` means empty **only if the queue does not store `null`** [[What is the peek method on stacks queues or streams in Java]] [[Why do most Queue implementations forbid null]].

Whatever the policy, the **head** is the element `remove()` / `poll()` would take. FIFO queues insert at the **tail**. Exceptions: priority queues (least under a comparator / natural order) and LIFO queues. Every implementation must document its ordering [[What is java.util.PriorityQueue]] [[What is the difference between a Queue and a Stack]].

`Deque` extends `Queue` and adds the other end (FIFO as a queue, LIFO as a stack). `BlockingQueue` adds waiting `put`/`take`. `LinkedList` is a `Queue` that still allows `null`. Implementations generally keep **identity** `equals` / `hashCode` [[What is the Deque interface in Java]] [[How would you explain extends Queue extends Deque or Deque extends Queue]] [[How does the Queue interface differ from the Deque interface]] [[What makes a BlockingQueue blocking]] [[Does LinkedList implement Queue and Deque in Java]] [[Do Queue and Deque implementations override equals]] [[What is ConcurrentLinkedQueue]].

Usual FIFO type: `ArrayDeque`.

```d2
direction: down
q: "Queue (1.5)\nhold before processing" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
head: "head = remove/poll target\nFIFO: oldest; PQ: least" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
two: "add/remove/element throw\noffer/poll/peek special value" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

q -> head
q -> two
```

**Fig. 1.** A `Queue` is not “always FIFO.” It is head insert/remove/examine plus an ordering policy.

```java
import java.util.ArrayDeque;
import java.util.Queue;

class WhatIsQueue {
    static void demo() {
        Queue<Integer> q = new ArrayDeque<>();
        System.out.println(q.offer(1)); // true
        System.out.println(q.offer(2)); // true
        System.out.println(q.peek());   // 1 — head, not removed
        System.out.println(q.poll());   // 1
        System.out.println(q.poll());   // 2
        System.out.println(q.poll());   // null — empty
        // q.remove();                  // NoSuchElementException
    }
}
```

**Listing 1.** Java 5+. `ArrayDeque` as `Queue` is FIFO. Empty `poll`/`peek` return `null`; `remove()`/`element()` throw.

> [!warning] `Queue` ≠ FIFO
> `PriorityQueue` is a `Queue` whose head is least, not first-in. `Deque` used as a `Queue` *is* FIFO.

> [!warning] `peek() == null` is not “empty” if the queue holds `null`
> Most implementations forbid `null` so the sentinel stays unambiguous. `LinkedList` is the named exception.

> [!tip] Interview answer
> **`Queue` holds elements before processing and adds head insert/remove/examine in two families (throw vs `false`/`null`).** Typically FIFO, but the head is defined by the implementation’s ordering. **Generally no `null`; `Deque` and `BlockingQueue` extend it.**
