<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #Java/Collections/List/LinkedList #SRS

# Why does LinkedList implement both List and Deque?

> [!abstract] Short answer
> **The same doubly-linked chain is a sequence with indexes (`List`) and a structure with `O(1)` access at both ends (`Deque`).** `Deque` extends `Queue`, so a queue API comes along. `LinkedList` has been a `List` since 1.2; `Deque` (1.6) named the double-ended operations it already did. Dual interfaces are a fit, not two backing stores.

## One chain, two contracts

`Node{prev, item, next}` plus `first`/`last` already support `addFirst` / `addLast` / `removeFirst` / `removeLast` in `Θ(1)` and a total order for `get(i)`, `ListIterator`, and `List.equals` [[Which data structure underlies Java LinkedList]] [[What design idea does LinkedList implement]] [[Is Java LinkedList a singly or doubly linked list]]. `List` is the indexed/sequence contract; `Deque` is insert/remove/examine at **both** ends (and stack `push`/`pop` at the head) [[What is the List interface in Java]] [[Does LinkedList implement Queue and Deque in Java]].

Those contracts do not fight the way `List` and `Set` do. Duplicates and `null` are allowed on both. `Queue` methods are `Deque` aliases (`add` → `addLast`, `remove` → `removeFirst`, …). Implementing `Deque` is why you can pass a `LinkedList` where a queue or deque is required without a second collection.

History matches the structure: the class is a `List` since 1.2; queue-style `offer`/`poll`/`peek` appear in 1.5; `offerFirst` / `push` / `descendingIterator` are 1.6 with `Deque`. The javadoc still leads with “doubly-linked list implementation of the `List` and `Deque` interfaces.” `Deque` lists `LinkedList` among known implementations next to `ArrayDeque`.

`ArrayDeque` shows the other product choice: a ring buffer that is a **`Deque` only** (no `List`, no `null`). It is the better default queue/stack. Keep `LinkedList` when you need **one object** that is a `List` (indexes, `ListIterator` splice) *and* a deque [[What is the difference between ArrayDeque and LinkedList as a Deque]] [[What is the worst case time complexity of add on a LinkedList]] [[Which classes implement the Java List interface]].

```d2
direction: down
node: "doubly-linked Node chain" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
list: "List\nindex, ListIterator, equals" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
deq: "Deque\nends + Queue + stack ops" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

node -> list
node -> deq
```

**Fig. 1.** Two interfaces, one layout. Not two lists glued together.

```java
java.util.LinkedList<String> both = new java.util.LinkedList<>();
java.util.List<String> asList = both;   // sequence / get(i)
java.util.Deque<String> asDeque = both; // addFirst / removeLast
java.util.Queue<String> asQueue = both; // Deque extends Queue
asDeque.addFirst("x");
asList.get(0); // "x" — same nodes
both.add(1, "y"); // List: walk, then linkBefore — still one chain
```

**Listing 1.** Conceptual: one instance satisfies `List` and `Deque`. Indexed `add` is the `List` half. `Queue` is not a third structure.

> [!warning] Dual interface ≠ “use LinkedList for everything”
> End ops are cheap; `get(i)` / `contains` are still `O(n)`. Prefer `ArrayList` for a list and `ArrayDeque` for a queue. Implementing both is capability, not a hint that one class wins all use cases.

> [!warning] `Deque` is not a second copy of the data
> There is no hidden array beside the nodes. `List` views and deque ops share `first`/`last`. Do not expect `ArrayDeque` to implement `List` just because `LinkedList` does.

> [!tip] Interview answer
> **Because a doubly-linked list is already a sequence and a double-ended queue.** `List` for indexes/`ListIterator`; `Deque` (hence `Queue`) for `O(1)` ends. Added when `Deque` arrived in 1.6; the nodes were always there. For a queue only, say `ArrayDeque`.
