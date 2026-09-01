<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #SRS

# Is Java LinkedList a singly or doubly linked list?

> [!abstract] Short answer
> **Doubly linked.** `java.util.LinkedList` is a doubly-linked implementation of `List` and `Deque`. Each OpenJDK `Node` stores `item`, `prev`, and `next`. A singly-linked list would have only a successor. Ends are `null` (`first.prev`, `last.next`), not a circular ring.

## Two neighbor pointers per node

The class documentation names it a **doubly-linked** list. OpenJDK’s private static `Node` has three fields: the payload and **both** directions. `linkLast` sets the new node’s `prev` to the old `last` and the old last’s `next` to the new node. `linkBefore` / unlinks patch both sides. `get(i)` walks from `first` via `next` or from `last` via `prev`, whichever end is closer — that nearer-end walk needs `prev`.

Reverse traversal without `get(i)` follows `prev`: `listIterator(size()).previous()`, `descendingIterator()`, or `reversed()` [[How do you traverse a LinkedList in reverse without using get index]]. A singly-linked structure could not offer O(1) `addFirst` / `removeLast` without scanning. `LinkedList` is also a `Deque` because both ends are cheap [[Does LinkedList implement Queue and Deque in Java]].

`first` and `last` on the list object are not extra per-node links. `item` is data, not a third structural pointer [[How would you explain LinkedList — or list]] [[How much extra memory does LinkedList add allocate per insertion]].

```d2
direction: right
a: "a\nprev / next" {
  width: 140
  height: 80
  style.fill: "#e3f2fd"
}
b: "b\nprev / next" {
  width: 140
  height: 80
  style.fill: "#e3f2fd"
}
c: "c\nprev / next" {
  width: 140
  height: 80
  style.fill: "#e3f2fd"
}

a -> b: next
b -> c: next
c -> b: prev
b -> a: prev
```

**Fig. 1.** Each node points both ways. Singly-linked would be `next` only.

```java
java.util.LinkedList<String> list = new java.util.LinkedList<>();
list.addFirst("a");
list.addLast("c");
list.add(1, "b"); // linkBefore — patches prev and next
String last = list.getLast(); // Deque / List end, not a scan from the head
```

**Listing 1.** End operations and mid insert all maintain two links. `getLast` is the tail pointer, not a singly-linked crawl.

```java
// OpenJDK shape — Conceptual
final class NodeShape<E> {
    E item;
    NodeShape<E> next;
    NodeShape<E> prev;
}
```

**Listing 2.** Conceptual: `prev` is what makes it doubly linked. There is no fourth neighbor field.

> [!warning] Doubly linked is not circular
> `first.prev` and `last.next` are `null`. Do not write a loop that assumes `tail.next == head`. `descendingIterator` uses `prev`, not a wrap-around `next`.

> [!warning] `List` does not imply linked nodes
> `ArrayList` implements `List` with an array. Asking “is a Java `List` singly or doubly linked?” is a type error: `List` is the interface; **this class** is the doubly-linked one.

> [!tip] Interview answer
> **`LinkedList` is doubly linked: each node has `prev` and `next`.** That is why both ends are O(1) and reverse iteration does not scan from the head. It is not singly linked, not circular, and not “four-way” — `item` is the element, not another link.
