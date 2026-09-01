<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #SRS

# Which data structure underlies Java LinkedList?

> [!abstract] Short answer
> **A doubly-linked list of private `Node` objects: `prev`, `item`, `next`.** The list holds `first` and `last` pointers and a `size`. Empty means both ends `null`. It is **not** circular (`first.prev` and `last.next` stay `null`), **not** an array, and **not** a singly-linked list.

## Nodes, not a backing array

The class is specified as a doubly-linked implementation of `List` and `Deque` [[Is Java LinkedList a singly or doubly linked list]] [[What design idea does LinkedList implement]] [[Does LinkedList implement Queue and Deque in Java]]. Each element lives in a `Node`. `linkLast` / `linkFirst` / `linkBefore` allocate one node and rewire neighbors; there is no `elementData` array as in `ArrayList` [[How much extra memory does LinkedList add allocate per insertion]] [[What is an ArrayList]].

`get(i)` / `node(index)` walk `next` from `first` or `prev` from `last`, whichever is nearer — the structure is a chain, so random access is `O(n)` [[What is the time complexity of random access by index in a LinkedList]]. The commented invariant in OpenJDK is: size 0 ⇔ `first == last == null`; otherwise `first.prev == null && last.next == null`. No dummy header, no wrap-around to make a ring.

`LinkedList` is still a `List` (indexes, `ListIterator`) on top of that chain; “list” in the interview sense is the interface, “linked list” is this layout [[How would you explain LinkedList — or list]] [[What is the List interface in Java]].

```d2
direction: right
first: "first" {
  width: 70
  height: 40
  style.fill: "#e8f5e9"
}
n0: "Node\nprev item next" {
  width: 150
  height: 70
  style.fill: "#e3f2fd"
}
n1: "Node" {
  width: 80
  height: 70
  style.fill: "#e3f2fd"
}
n2: "Node" {
  width: 80
  height: 70
  style.fill: "#e3f2fd"
}
last: "last" {
  width: 70
  height: 40
  style.fill: "#e8f5e9"
}

first -> n0
n0 -> n1 -> n2
n2 -> n1 -> n0
n2 -> last
```

**Fig. 1.** Doubly-linked chain. Ends are null-terminated, not linked to each other.

```java
// Conceptual layout (private in java.util.LinkedList)
// Node: prev, item, next
java.util.LinkedList<String> list = new java.util.LinkedList<>();
list.add("a"); // one Node; first == last
list.add("b"); // second Node; last.next == null, first.prev == null
```

**Listing 1.** Conceptual: each `add` is a node on a doubly-linked chain, not a slot in an array.

> [!warning] Doubly-linked ≠ circular and ≠ `O(1) get(i)`
> Two pointers per node only let walks start from either end. `first` and `last` are not a ring. Do not draw a dummy sentinel unless you are describing some *other* linked-list design.

> [!warning] Not the dump “four-way / singly” story
> Java’s `LinkedList` is one `Node` type with `prev`/`next`. It is not a skip list, not `ArrayDeque`’s ring buffer, and not `ArrayList`. `Deque` is extra *interface*, not a second structure.

> [!tip] Interview answer
> **Doubly-linked list: `Node{prev, item, next}` plus `first`/`last`.** Null-terminated, not circular. That is why end insert is `Θ(1)` and index `get` is `O(n)`. Contrast `ArrayList`’s array.
