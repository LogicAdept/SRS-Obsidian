<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/ArrayDeque #SRS

> [!abstract] Short answer
> **FILO is LIFO — a stack.** `java.util.Stack` is the legacy class documented as last-in-first-out. The collections API’s LIFO type is `Deque` used with `push` / `pop` / `peek` on the head; the usual implementation is `ArrayDeque`. Java’s own pages say **LIFO**, not “FILO.”

## Same order, official name LIFO

First-in-last-out and last-in-first-out describe one discipline: the earliest insert is removed last; the latest insert is removed first. `Stack` “represents a last-in-first-out (LIFO) stack of objects.” `Deque` “can also be used as LIFO (Last-In-First-Out) stacks.” There is no `FILO` type or method name in `java.util`.

That stack protocol is **not** a separate `Collection` subinterface. `Queue` (and a `Deque` used as a queue) is FIFO: insert at the tail, take from the head ([[Which Java collection implements FIFO ordering]], [[What is the difference between a Queue and a Stack]]). The same `ArrayDeque` is FIFO if you `offer`/`poll` and LIFO if you `push`/`pop` ([[How do you use a Deque as a stack]]).

```d2
direction: right
fifo: "FIFO / queue\noffer last, poll first" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
lifo: "LIFO = FILO / stack\npush and pop the head" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
ad: "ArrayDeque\nimplements Deque" {
  width: 220
  height: 70
  style.fill: "#fff8e1"
}
ad -> fifo
ad -> lifo
```

**Fig. 1.** One concrete type, two disciplines. “Which collection is FILO?” → stack usage of `Deque`, not a unique class besides legacy `Stack`.

`Stack` extends `Vector` and adds `push`, `pop`, `peek`, `empty`, `search` on the **last** slot. Prefer `Deque` implementations instead: `ArrayDeque` is the example on `Stack`’s own page and is likely faster as a stack ([[How would you explain Stack how why]], [[Why is java.util.Stack discouraged and what should you use instead]]). `LinkedList` is also a `Deque`, so it can be LIFO too — that is a different trade-off ([[What is the difference between ArrayDeque and LinkedList as a Deque]]).

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Stack;

class FiloIsLifo {
    static void demo() {
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(1);              // first in
        stack.push(2);              // last in
        Integer lastIn = stack.pop(); // 2 — LIFO / FILO
        Integer firstIn = stack.pop(); // 1 — first in, last out

        Stack<Integer> legacy = new Stack<>();
        legacy.push(1);
        legacy.push(2);
        legacy.pop();               // 2 — same order, last Vector index
    }
}
```

**Listing 1.** `ArrayDeque.push` / `pop` at the head, or legacy `Stack` at the vector’s end: first inserted leaves last.

Other `Deque`s (`LinkedList`, `ConcurrentLinkedDeque`, blocking deques) can run the same head protocol. None of them is “the FILO collection” in the type hierarchy the way `Set` is a set. Name the **discipline** and the **type you would declare**: `Deque<E> stack = new ArrayDeque<>()`.

> [!warning] Do not stop at `java.util.Stack`
> A dump that answers only “`Stack`” is half a generation behind. The LIFO API to declare is `Deque`. `Stack` is still LIFO; it is also a synchronized `List`.

> [!warning] `offer` is not FILO
> `add` / `offer` append at the tail. Mixing them with `push` on one deque is neither a clean stack nor a clean queue. FILO on a `Deque` means the `push` / `pop` (or `*First`) family.

> [!tip] Interview answer
> **FILO is LIFO: a stack.** Legacy `java.util.Stack` does that on a `Vector`. In modern code you declare a `Deque`, almost always `ArrayDeque`, and call `push`/`pop` on the head. Java documents it as LIFO, not as a type named FILO.
