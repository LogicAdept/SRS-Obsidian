<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #Java/Collections/List/LinkedList #SRS

# Does LinkedList implement Queue and Deque in Java?

> [!abstract] Short answer
> **Yes.** `LinkedList` is a doubly-linked implementation of **`List` and `Deque`**. `Deque` extends `Queue`, so a `LinkedList` *is* a `Queue` (`Queue` shows up on “all implemented interfaces”). Assign `Queue<E> q = new LinkedList<>()` or `Deque<E> d = new LinkedList<>()` — both compile.

## `Deque` is a `Queue`; `LinkedList` is both plus `List`

`LinkedList` (since 1.2) implements all optional list operations and permits every element, including `null`. As a `Deque` it supports insert / remove / examine at **both** ends. Queue methods on the class are since 1.5; the rest of the `Deque` surface (and the `Deque` type itself) is since 1.6.

`Deque` extends `Queue`. Used as a queue, a deque is FIFO: insert at the tail, take from the head. The inherited `Queue` methods are the tail/head `Deque` methods:

| `Queue` | `Deque` equivalent |
| --- | --- |
| `add` / `offer` | `addLast` / `offerLast` |
| `remove` / `poll` | `removeFirst` / `pollFirst` |
| `element` / `peek` | `getFirst` / `peekFirst` |

The same object is also a LIFO stack (`push` → `addFirst`, `pop` → `removeFirst`). `Deque` has no indexed access; `List` on the same instance still has `get(i)` (walk from the nearer end).

```d2
direction: right
ll: "LinkedList" {
  width: 160
  height: 80
  style.fill: "#e3f2fd"
}
list: "List" {
  width: 120
  height: 70
  style.fill: "#fff3e0"
}
deque: "Deque" {
  width: 120
  height: 70
  style.fill: "#e8f5e9"
}
queue: "Queue" {
  width: 120
  height: 70
  style.fill: "#e8f5e9"
}

ll -> list: implements
ll -> deque: implements
deque -> queue: extends
```

**Fig. 1.** `LinkedList` implements `List` and `Deque`. `Queue` is not a second sibling on the class header; it comes with `Deque`.

```java
class LinkedListIsQueueAndDeque {
    static void assign() {
        java.util.LinkedList<String> ll = new java.util.LinkedList<>();
        java.util.Queue<String> q = ll;   // Queue via Deque
        java.util.Deque<String> d = ll;   // Deque
        java.util.List<String> list = ll; // still a List

        q.offer("a");
        q.offer("b");
        String head = q.poll(); // "a" — FIFO
        d.addFirst("z");        // same list, now z, b
        String idx = list.get(0); // "z" — List index, not a Deque API
    }
}
```

**Listing 1.** One instance typed as `Queue`, `Deque`, and `List`. FIFO uses `offer` / `poll`; `get(0)` needs the `List` view.

Prefer `ArrayDeque` as a pure deque/queue: it forbids `null` and is documented as likely faster than `LinkedList` as a queue [[What is the difference between ArrayDeque and LinkedList as a Deque]]. Prefer `Deque` over legacy `Stack` [[Why is java.util.Stack discouraged and what should you use instead]]. Reverse walk is `descendingIterator()` or `reversed()` [[How can you iterate a Deque in both directions]].

> [!warning] `null` is legal on `LinkedList` and a hazard as a `Queue`
> `Queue` / `Deque` use `null` from `poll` / `peek` to mean empty. Implementations are strongly encouraged not to store `null`. `LinkedList` still allows it. `poll()` after `offer(null)` cannot tell “empty” from “null head.” `ArrayDeque` rejects `null`.

> [!warning] Implementing `Deque` does not hide `List`
> `equals` / `hashCode` follow **`List`** (same sequence), not identity-based `Deque` defaults. A `Deque` reference has no `get(int)`. Indexing a `LinkedList` is still O(n) from the nearer end. Not synchronized.

> [!tip] Interview answer
> **Yes — `LinkedList` implements `List` and `Deque`, and `Deque` extends `Queue`, so it is a queue.** FIFO is add-last / remove-first; the same instance is also a stack and a list with indexes. That is why you *can* write `Queue q = new LinkedList<>()`. For a queue or deque in new code, prefer `ArrayDeque`: no `null`, and it is the documented faster queue.
