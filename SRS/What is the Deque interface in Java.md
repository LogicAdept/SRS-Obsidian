<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/Deque #SRS

# What is the `Deque` interface in Java?

> [!abstract] Short answer
> **A linear collection with insert, remove, and examine at both ends** (“deck”, double-ended queue). It **extends `Queue`** (Java 6; also `SequencedCollection`). Twelve methods: throw vs special value at first and last. As a `Queue` it is FIFO; as a stack, LIFO (`push`/`pop` at first). Prefer it to legacy `Stack`. Usual impl: `ArrayDeque`.

## Both ends, two failure styles

`Deque` supports insertion and removal at **both** ends. Most implementations have no fixed size; the interface also allows capacity-restricted deques. Insert, remove, and examine each exist in two forms: one throws, the other returns `null` or `false`. Special-value insert is for capacity-restricted deques; on most impls insert cannot fail [[What are the First and Last methods on Deque]] [[What are the two method families on Queue]].

| | First (head) | Last (tail) |
|---|---|---|
| Insert | `addFirst` / `offerFirst` | `addLast` / `offerLast` |
| Remove | `removeFirst` / `pollFirst` | `removeLast` / `pollLast` |
| Examine | `getFirst` / `peekFirst` | `getLast` / `peekLast` |

It **extends `Queue`**. Used as a queue → FIFO: add last, remove first (`add`→`addLast`, `poll`→`pollFirst`, …). Used as a stack → LIFO: `push`→`addFirst`, `pop`→`removeFirst`. `peek` always looks at the **beginning**, queue or stack. Prefer `Deque` to `java.util.Stack` [[How does the Queue interface differ from the Deque interface]] [[How would you explain extends Queue extends Deque or Deque extends Queue]] [[What is the difference between a Queue and a Stack]].

Also: `removeFirstOccurrence` / `removeLastOccurrence`; `descendingIterator` (no `List` indexes) [[How can you iterate a Deque in both directions]]. Implementations are **strongly encouraged** not to store `null` (`null` means empty on `poll*`/`peek*`). `LinkedList` still permits `null` as a `List`. `equals` / `hashCode` are generally **identity** [[Why do most Queue implementations forbid null]] [[Does LinkedList implement Queue and Deque in Java]] [[Do Queue and Deque implementations override equals]].

`ArrayDeque` is the resizable-array `Deque` (no `null`, faster than `LinkedList` as a queue). `PriorityQueue` is a `Queue` that is **not** a `Deque`.

```d2
direction: down
d: "Deque extends Queue\nfirst and last" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
fifo: "as Queue: add last, poll first" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
lifo: "as stack: push/pop first" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

d -> fifo
d -> lifo
```

**Fig. 1.** One interface, two uses: FIFO queue or LIFO stack. Both ends are always there.

```java
import java.util.ArrayDeque;
import java.util.Deque;

class WhatIsDeque {
    static void demo() {
        Deque<Integer> d = new ArrayDeque<>();
        d.offerLast(1);
        d.offerLast(2);
        System.out.println(d.pollFirst()); // 1 — FIFO as a queue

        d.push(9);
        System.out.println(d.pop());       // 9 — LIFO at first
        System.out.println(d.peekLast());  // 2
    }
}
```

**Listing 1.** Java 6+. `ArrayDeque` as `Deque`: `offerLast`/`pollFirst` are the `Queue` map; `push`/`pop` are the stack map.

> [!warning] `Queue` methods are not both ends
> Typed as `Queue`, you only get last-in / first-out. Use `offerFirst` / `pollLast` (or a `Deque` reference) for the other end.

> [!warning] `null` is the empty signal
> Implementations should reject `null`. `LinkedList` still allows it; then `pollFirst() == null` is not “empty.”

> [!tip] Interview answer
> **`Deque` is a double-ended queue (pronounced “deck”) that extends `Queue`.** Twelve methods at first and last; FIFO as a queue, LIFO as a stack — use it instead of `Stack`. **Usual implementation is `ArrayDeque`; not every `Queue` is a `Deque`.**
