<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS

# Which tree data structure backs Java TreeSet?

> [!abstract] Short answer
> **A red-black tree.** `TreeSet` (Java 1.2) is a `NavigableSet` **based on a `TreeMap`**, and `TreeMap` is documented as a **red-black tree** `NavigableMap`. Basic `add` / `contains` / `remove` are **guaranteed log(n)**. You do not pick AVL, B-tree, or a plain unbalanced BST.

## `TreeSet` → `TreeMap` → red-black

`TreeSet` JavaDoc: a `NavigableSet` implementation based on a `TreeMap`. Order is natural `Comparable` order or a constructor `Comparator` ([[What restriction applies when adding elements to a TreeSet]]).

`TreeMap` JavaDoc: a **red-black tree** `NavigableMap`. `containsKey` / `get` / `put` / `remove` are guaranteed log(n). The algorithms are adaptations of Cormen, Leiserson, and Rivest (*Introduction to Algorithms*). That is why inserting already-sorted keys does not degenerate into a linked list ([[What happens when you insert elements into a TreeSet in ascending order]]).

`TreeSet` is the class; `SortedSet` / `NavigableSet` are the interfaces ([[What is the difference between TreeSet and SortedSet]]). Neighbour queries (`floor`, `ceiling`, `lower`, `higher`) and range views sit on that same tree ([[What NavigableSet operations does TreeSet provide]]).

```d2
direction: down
set: "TreeSet\nNavigableSet" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
map: "TreeMap\nNavigableMap" {
  width: 200
  height: 55
  style.fill: "#fff3e0"
}
rb: "Red-black tree" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}

set -> map: "based on"
map -> rb: "implementation"
```

**Fig. 1.** The JDK does not expose a `RedBlackTree` type. The set is a `TreeMap` whose keys are the elements.

```java
NavigableSet<Integer> s = new TreeSet<>();
s.add(3);
s.add(1);
s.add(2);
s.first();                 // 1 — tree order, not insert order
```

**Listing 1.** Construction hides the tree. Membership and order both go through `compareTo` / `compare`, which must stay consistent with `equals` for the `Set` contract ([[Why must TreeMap ordering be consistent with equals]]).

> [!warning] Not AVL, not a heap, not a skip list
> Interview guesses of AVL or B-tree are wrong for `java.util.TreeSet`. `PriorityQueue` is a heap, not a search tree ([[What is the difference between PriorityQueue and TreeSet]]). `ConcurrentSkipListSet` is a concurrent skip list, not a red-black `TreeMap` ([[What is ConcurrentSkipListSet]]).

> [!warning] Self-balancing does not mean “always balanced height 1”
> Red-black trees keep height O(log n), not perfectly filled. Cost is still guaranteed log(n) for the documented operations. The implementation is not synchronized.

> [!tip] Interview answer
> **`TreeSet` is backed by a `TreeMap`, and `TreeMap` is a red-black tree.** That gives guaranteed log(n) `add`, `contains`, and `remove`. It is not AVL and not a heap.
