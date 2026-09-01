<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #SRS

# How would you explain LinkedList — or list?

> [!abstract] Short answer
> **`List` is the interface (sequence, indexes, typically duplicates).** **`LinkedList` is one implementation: a doubly-linked list of `List` and `Deque`.** Each OpenJDK `Node` has `item`, `prev`, and `next` — two neighbor links, not one and not four. `first` / `last` live on the list, not on every node. It is not an `ArrayList` and not the `List` type itself.

## Interface versus this class

`List` is the ordered `Collection`: positional `get` / `set` / `add(int, …)`, `ListIterator`, typically `equals`-duplicates. Many classes implement it (`ArrayList`, `LinkedList`, `Vector`, `CopyOnWriteArrayList`, `List.of`, …). You program to `List` when any sequence will do.

`LinkedList` is the doubly-linked concrete class: implementation of `List` and `Deque` (so also `Queue`). All optional list operations; `null` allowed. Index operations walk from the nearer end. Sequential iteration (`iterator` / `listIterator`) follows `next` / `prev` in linear time; repeating `get(i)` does not [[Does LinkedList implement Queue and Deque in Java]] [[What is the difference between ArrayList and LinkedList]].

**Doubly, not singly, not “four-way.”** A singly-linked list would store only a successor. OpenJDK stores **both** directions on every node. A third/fourth pointer on the node does not exist: `item` is the payload, not a link. The list object’s `first` and `last` are two references for the whole collection, not extra links per element. Ends are `null` (`first.prev`, `last.next`) — it is not a circular ring.

Each `add` allocates one `Node` (header + three oops) [[How much extra memory does LinkedList add allocate per insertion]]. Prefer `ArrayDeque` as a pure deque/queue.

```d2
direction: right
iface: "List\n(interface)" {
  width: 160
  height: 80
  style.fill: "#fff3e0"
}
al: "ArrayList\narray + size" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
ll: "LinkedList\ndoubly-linked nodes" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}

iface -> al: implements
iface -> ll: implements
```

**Fig. 1.** `List` is the contract. `LinkedList` is the node-chain implementation of that contract (and of `Deque`).

```java
java.util.List<String> asList = new java.util.LinkedList<>();
java.util.Deque<String> asDeque = (java.util.LinkedList<String>) asList;
asList.add("a");           // List
asDeque.addLast("b");      // Deque / Queue
String x = asList.get(0);  // still List — O(n) walk from an end
```

**Listing 1.** One object, two APIs. `get(0)` is legal because it is a `List`; it is still a link walk.

```java
// OpenJDK node — Conceptual
final class NodeShape<E> {
    E item;
    NodeShape<E> next;
    NodeShape<E> prev;
}
```

**Listing 2.** Conceptual: two structural links (`prev`, `next`) plus the element. That is doubly-linked, not singly-linked and not four-linked.

> [!warning] `LinkedList` is a `List`, but `List` is not a `LinkedList`
> A method that takes `List` may receive an `ArrayList`. Do not call `descendingIterator()` or assume O(1) `addFirst` without a `Deque` / `LinkedList` type. Conversely, `List.get(i)` on a `LinkedList` is not array access.

> [!warning] “Four links” usually miscounts `item` or `first`/`last`
> `item` is data. `first`/`last` are list fields. Counting those as per-node links invents a 3- or 4-linked list that the class does not implement. Walk with an iterator, not `get(i)` [[How do you iterate elements LinkedList in order not using get(index]].

> [!tip] Interview answer
> **`List` is the interface; `LinkedList` is a doubly-linked implementation of `List` and `Deque`.** Each node points to previous and next — not singly-linked, not four-way. Use it when you need deque operations at the ends; for a random-access list use `ArrayList`. Never treat `List` and `LinkedList` as the same type.
