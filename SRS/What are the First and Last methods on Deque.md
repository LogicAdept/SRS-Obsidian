<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/Deque #SRS

# What are the First and Last methods on `Deque`?

> [!abstract] Short answer
> **Twelve methods: insert, remove, and examine at each end, in a throwing form and a special-value form.** First is the head; last is the tail. `add*` / `remove*` / `get*` throw on failure; `offer*` / `poll*` / `peek*` return `false` or `null`. Inherited `Queue` methods are FIFO: **insert last, remove and examine first.** Stack `push`/`pop`/`peek` are **first**-end operations.

## Two ends, two failure styles

`Deque` (“deck”) is a linear collection with insertion and removal at **both** ends. Each of insert, remove, and examine exists in two forms: one throws if it cannot complete; the other returns a special value (`null` or `false`). The special-value insert is for capacity-restricted deques; on most implementations insert cannot fail [[What is the Deque interface in Java]] [[What are the two method families on Queue]].

| | First (head) throws | First special value | Last (tail) throws | Last special value |
|---|---|---|---|---|
| Insert | `addFirst(e)` | `offerFirst(e)` | `addLast(e)` | `offerLast(e)` |
| Remove | `removeFirst()` | `pollFirst()` | `removeLast()` | `pollLast()` |
| Examine | `getFirst()` | `peekFirst()` | `getLast()` | `peekLast()` |

Empty deque: `removeFirst` / `removeLast` / `getFirst` / `getLast` throw `NoSuchElementException`. `poll*` / `peek*` return `null`. Full capacity-restricted deque: `addFirst` / `addLast` throw `IllegalStateException`; `offerFirst` / `offerLast` return `false`. Prefer `offer*` when capacity can bind. `null` is the empty sentinel — implementations are strongly encouraged not to store `null`.

As a **queue**, FIFO means add at the **end**, remove from the **beginning**. `Queue` methods are exactly:

| `Queue` | `Deque` |
|---|---|
| `add(e)` / `offer(e)` | `addLast(e)` / `offerLast(e)` |
| `remove()` / `poll()` | `removeFirst()` / `pollFirst()` |
| `element()` / `peek()` | `getFirst()` / `peekFirst()` |

As a **stack**, push and pop at the **beginning**: `push` → `addFirst`, `pop` → `removeFirst`, `peek` → `peekFirst`. Queue `peek` and stack `peek` both mean the first element [[How do you use a Deque as a stack]] [[How does the Queue interface differ from the Deque interface]].

```d2
direction: right
first: "first / head\naddFirst · removeFirst · getFirst\nofferFirst · pollFirst · peekFirst" {
  width: 320
  height: 90
  style.fill: "#e3f2fd"
}
mid: "…" {
  width: 60
  height: 50
}
last: "last / tail\naddLast · removeLast · getLast\nofferLast · pollLast · peekLast" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}

first -> mid -> last: "FIFO: offer last, poll first"
```

**Fig. 1.** Queue traffic is tail in, head out. Stack traffic stays on the head. Same twelve methods either way.

```java
import java.util.ArrayDeque;
import java.util.Deque;

class DequeFirstLast {
    static void demo() {
        Deque<String> d = new ArrayDeque<>();
        d.offerFirst("x");          // true; does not throw
        d.offerLast("y");           // deque: x … y
        System.out.println(d.peekLast()); // y — null if empty
        System.out.println(d.getFirst()); // x — NoSuchElementException if empty
        d.removeFirst();            // Queue.remove / stack.pop
        d.addLast("z");             // Queue.add
    }
}
```

**Listing 1.** Java 6+ `Deque`. After `offerFirst("x")` then `offerLast("y")`, first is `x` and last is `y`. `ArrayDeque` is unbounded, so `addFirst`/`addLast` do not hit `IllegalStateException` here. Interior deletes are `removeFirstOccurrence` / `removeLastOccurrence`, not this grid.

Since Java 21, `Deque` also extends `SequencedCollection`; `addFirst` / `getFirst` and the other end methods are the same operations. No `get(i)` — that is `List`, not `Deque` [[How can you iterate a Deque in both directions]].

> [!warning] `getFirst` is not `peekFirst`
> Empty deque: `getFirst()` / `removeFirst()` throw `NoSuchElementException`. `peekFirst()` / `pollFirst()` return `null`. Interview mix-ups copy the `Queue` `element` vs `peek` split onto the wrong end.

> [!warning] `Queue.add` is `addLast`, not `addFirst`
> FIFO insert is the **tail**. Using `addFirst` (or `push`) as if it were `Queue.add` reverses the queue into a stack.

> [!tip] Interview answer
> **`Deque` has twelve end methods: first and last, each with a throwing form and a `null`/`false` form.** As a queue, insert last and take first. As a stack, `push`/`pop` are first-end. **`get`/`remove` throw on empty; `peek`/`poll` return `null`.**
