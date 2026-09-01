<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #SRS

# What design idea does LinkedList implement?

> [!abstract] Short answer
> **A doubly-linked list: elements live in heap nodes chained by `prev` / `next`, not in a contiguous array.** That is sequential access (`AbstractSequentialList`) rather than random access (`AbstractList` / `ArrayList`). The same chain is also a `Deque` (and so a `Queue`): cheap work at both ends.

## Linked nodes, not a growing array

`LinkedList` is documented as a doubly-linked implementation of `List` and `Deque`. OpenJDK’s `Node` holds `item`, `prev`, and `next`. Insert/delete at a **known node** (the ends, or a `ListIterator` cursor) is pointer rewiring and one allocation; there is no `System.arraycopy` of a tail. Index `get` / `set` / `add(int)` must **walk** from the nearer end — time proportional to the index, which is why `List` tells you to iterate instead of indexing when you do not know the implementation [[Is Java LinkedList a singly or doubly linked list]] [[What is the difference between ArrayList and LinkedList]].

`AbstractSequentialList` exists for a “sequential access” store such as a linked list: `get(int)` is defined on top of `listIterator(index)`, the opposite of `AbstractList` (iterator on top of `get`). `LinkedList` extends that sequential skeleton. `ArrayList` is the resizable-array design [[What design idea does ArrayList implement]].

Because both ends are O(1), the class implements `Deque` (`addFirst` / `addLast` / `pollFirst` / …) and therefore `Queue` [[Does LinkedList implement Queue and Deque in Java]]. That is the same node chain, not a second structure.

The design does **not** give O(1) `contains` or mid-index `get`. Membership is a linear `equals` scan. Each `add` allocates a node (header + three oops). Prefer `ArrayDeque` as a pure deque when you do not need `List` indexes.

```d2
direction: right
idea: "doubly-linked list" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
seq: "AbstractSequentialList\nget via listIterator" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
apis: "List + Deque (+ Queue)" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}

idea -> seq
idea -> apis
```

**Fig. 1.** The idea is the node chain. Sequential `List` access and two-ended `Deque` APIs are that chain, not an array.

```java
java.util.LinkedList<String> list = new java.util.LinkedList<>();
list.addLast("tail");   // linkLast — new Node, no array copy
list.addFirst("head");  // other end, same idea
java.util.ListIterator<String> it = list.listIterator();
it.next();
it.add("mid");          // splice at the cursor — still nodes, not a shift of a backing array
```

**Listing 1.** End inserts and iterator `add` are the linked-list design: local pointer updates. `list.get(i)` would hide a walk.

```java
// OpenJDK shape — Conceptual
final class NodeShape<E> {
    E item;
    NodeShape<E> next;
    NodeShape<E> prev;
}
```

**Listing 2.** Conceptual: the design in one type — payload plus two neighbor links.

> [!warning] “Linked list” is not the `List` interface
> `List` is the sequence contract (`ArrayList` implements it too). Saying `LinkedList` “implements List” is the API, not the design idea. The idea is **doubly-linked nodes**. Calling `get(i)` in a loop throws that idea away and goes quadratic.

> [!warning] Mid-list “O(1) insert” needs a cursor already there
> Textbook linked-list insert is O(1) **at a node you hold**. `add(index, e)` first finds that node in O(min(index, n−index)). `ListIterator.add` after you have walked there is the O(1) splice. Do not quote O(1) mid-insert for `add(n/2, e)` from the outside.

> [!tip] Interview answer
> **`LinkedList` implements a doubly-linked list: nodes with `prev` and `next`, sequential access, cheap ends.** That is why it is a `Deque` as well as a `List`, and why `get(i)` and `contains` are linear. `ArrayList` is the other design — a resizable array. Do not treat `List` and “linked list” as the same words.
