<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #Java/Collections/List/Vector #SRS

# What is the difference between a `Queue` and a `Stack`?

> [!abstract] Short answer
> **A `Queue` holds elements prior to processing; insert, extract, and inspect the head. It is typically FIFO, but not always** (`PriorityQueue` is a `Queue`). **A stack is LIFO: push/pop/peek the top.** In `java.util`, prefer `Deque` (`ArrayDeque`) for LIFO. Legacy `Stack` extends synchronized `Vector` and does **not** implement `Queue`. On a `Queue`, `remove()`/`poll()` take the **head** — for FIFO that is the oldest element; for a deque used as a stack, `pop` is `removeFirst` (the newest).

## FIFO processing vs LIFO top

`Queue` (Java 5): a collection designed for holding elements prior to processing, plus insert / extract / inspect. Those methods come in throw vs special-value pairs (`add`/`offer`, `remove`/`poll`, `element`/`peek`). Queues **typically, but do not necessarily**, order FIFO. Exceptions named in the interface: **priority queues** (comparator / natural order) and **LIFO queues (stacks)** [[What is the Queue interface in Java]] [[What is java.util.PriorityQueue]] [[What are the two method families on Queue]].

Whatever the policy, the **head** is the element `remove()` or `poll()` would take.

`Stack` (Java 1.0): a LIFO vector of objects — `push`, `pop`, `peek`, `empty`, `search`. It **extends `Vector`**. `Vector` is synchronized (unlike the newer collections). `Deque` provides a more complete LIFO API and **should be used in preference** to `Stack`; the documented example is `Deque<Integer> stack = new ArrayDeque<>()` [[Why is java.util.Stack discouraged and what should you use instead]] [[How do you use a Deque as a stack]].

`Deque` is the type that is **both**: as a queue, add at the **tail**, take from the **head** (FIFO). As a stack, `push` → `addFirst`, `pop` → `removeFirst`, `peek` → `peekFirst`. Queue `peek` and stack `peek` both mean the first/head element of the deque [[What is the Deque interface in Java]] [[What are the First and Last methods on Deque]].

`java.util.Stack` is **not** a `Queue`. Empty `Stack.peek`/`pop` throw `EmptyStackException`; empty `Queue.peek`/`poll` return `null`.

```d2
direction: down
q: "Queue (typical FIFO)\noffer tail → poll head" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
s: "Stack / Deque LIFO\npush/pop the same end" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

q -> s: "Deque can be either"
```

**Fig. 1.** Same `ArrayDeque`, two disciplines. `PriorityQueue` is a `Queue` that skips FIFO.

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Queue;

class QueueVsStack {
    static void demo() {
        Queue<Integer> fifo = new ArrayDeque<>();
        fifo.offer(1);
        fifo.offer(2);
        System.out.println(fifo.poll()); // 1 — oldest

        Deque<Integer> lifo = new ArrayDeque<>();
        lifo.push(1);
        lifo.push(2);
        System.out.println(lifo.pop());  // 2 — newest
        // Deque<Integer> stack = new ArrayDeque<>();  // preferred over java.util.Stack
    }
}
```

**Listing 1.** Work lists / request handling: FIFO `Queue`. Nested undo / “only the top”: LIFO `Deque`. Do not reach for `java.util.Stack` (a `Vector`) unless you need that legacy type [[Which Java collection implements FIFO ordering]] [[Which Java collection implements FILO ordering]].

> [!warning] `Queue` ≠ FIFO
> `PriorityQueue` implements `Queue` and delivers the **least** element, not arrival order. “Queue means FIFO” fails that interview follow-up.

> [!warning] `Stack.peek` is not `Queue.peek`
> Empty stack: `EmptyStackException`. Empty queue: `peek`/`poll` → `null`. Mixing the APIs on one mental model causes the wrong empty handling.

> [!warning] Prefer `ArrayDeque` over `java.util.Stack`
> `Stack` is a synchronized `Vector` with five extra methods. The platform’s own `Stack` javadoc points at `Deque` / `ArrayDeque`.

> [!tip] Interview answer
> **A `Queue` is hold-then-process, usually FIFO, head via `poll`/`remove` — but `PriorityQueue` is still a `Queue`.** A stack is LIFO (`push`/`pop` the top). **Use `Deque` (`ArrayDeque`) for a stack; `java.util.Stack` is a legacy synchronized `Vector`.**
