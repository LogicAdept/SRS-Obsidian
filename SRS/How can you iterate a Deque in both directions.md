<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #Java/Collections/Iteration #SRS

# How can you iterate a `Deque` in both directions?

> [!abstract] Short answer
> **Head → tail with `iterator()` (enhanced `for`). Tail → head with `descendingIterator()`, or — since Java 21 — `for (E e : deque.reversed())`.** `descendingIterator()` returns an `Iterator`, not an `Iterable`, so you cannot drop it into a for-each. `reversed()` is a reverse-ordered `Deque` **view**. Neither walk is an indexed scan: `Deque` has `getFirst` / `getLast`, not `get(i)`.

## Two iterators, one reverse view

`Deque.iterator()` returns elements in **proper sequence**: first (head) to last (tail). That is also dequeue / `pop` order: successive `remove()` or `pop()` would yield the same sequence. Enhanced `for` uses this iterator [[How are Iterable Iterator and for-each related in Java]].

`Deque.descendingIterator()` returns the opposite: last (tail) to first (head). Use a `while` (`hasNext` / `next`). `Iterator.remove()` is optional and supported on `ArrayDeque` (both directions).

Java 21: `Deque` extends `SequencedCollection`. `reversed()` returns a reverse-ordered `Deque` view whose encounter order is the inverse of this deque. Order-sensitive operations on the view write through (for example `getFirst` on the view behaves like `getLast` on the original). `reversed().reversed()` is this deque. Because the view is a `Deque`, it is `Iterable`, so enhanced `for` works.

Unlike `List`, `Deque` does not offer indexed access. `LinkedList` still has `get(i)` and `listIterator` because it is also a `List`; that is not the `Deque` API [[How do you iterate a List in reverse using ListIterator]].

When the deque is a **stack** (`push` / `pop` at the head), for-each is already **top to bottom**. `descendingIterator` / `reversed()` is bottom to top. Prefer `ArrayDeque` over legacy `Stack` [[Why is java.util.Stack discouraged and what should you use instead]].

```d2
direction: right
head: "head (first)" {
  width: 160
  height: 55
  style.fill: "#e3f2fd"
}
mid: "…elements…" {
  width: 140
  height: 55
}
tail: "tail (last)" {
  width: 160
  height: 55
  style.fill: "#fff3e0"
}

head -> mid -> tail: "iterator() / for-each"
tail -> mid -> head: "descendingIterator()\nreversed() (Java 21)"
```

**Fig. 1.** Same deque, two encounter orders. Queue FIFO and stack pop order follow **head → tail**.

```java
class DequeBothWays {
    static void demo() {
        java.util.Deque<Integer> d = new java.util.ArrayDeque<>(java.util.List.of(1, 2, 3));
        for (int x : d) {
            System.out.print(x);           // 123  head → tail
        }
        java.util.Iterator<Integer> it = d.descendingIterator();
        while (it.hasNext()) {
            System.out.print(it.next());   // 321  tail → head
        }
        for (int x : d.reversed()) {       // Java 21: Iterable reverse view
            System.out.print(x);           // 321
        }
    }
}
```

**Listing 1.** `ArrayDeque(Collection)` places the collection’s first element at the front, so `1` is head and `3` is tail. `for (int x : d.descendingIterator())` does not compile: `Iterator` is not `Iterable`.

`ArrayDeque` documents that `iterator()` is **fail-fast**: structural change except through that iterator’s `remove` generally throws `ConcurrentModificationException` (best-effort). `descendingIterator` is the same live deque, not a snapshot; OpenJDK throws CME if a walked slot is unexpectedly `null`. `ConcurrentLinkedDeque` iterators (both directions) are **weakly consistent** and do not throw CME. Do not treat CME as a `Deque` interface guarantee [[What is ConcurrentModificationException]].

`PriorityQueue` is a `Queue`, not a `Deque`. It has no `descendingIterator`. Its `iterator()` is not in any particular order [[Does iterating a PriorityQueue return elements in sorted order]].

> [!warning] `descendingIterator()` is not for-each-ready
> It is an `Iterator`. Loop with `hasNext` / `next`, or for-each `reversed()` (Java 21). Do not confuse that with copying into a `List` just to walk backwards.

> [!warning] Reverse walk is not a snapshot
> `descendingIterator` and `reversed()` see the live deque (implementation policy varies: fail-fast vs weakly consistent). `PriorityQueue` is the wrong type for this API.

> [!tip] Interview answer
> **For-each / `iterator()` is head to tail; `descendingIterator()` is tail to head.** The descending iterator is not `Iterable`, so use a `while` loop, or Java 21 `for (E e : deque.reversed())`. That reverse view is not a copy. `Deque` has no `get(i)`.
