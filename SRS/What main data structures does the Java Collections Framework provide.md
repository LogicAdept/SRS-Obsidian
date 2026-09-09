<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS

# What main data structures does the Java Collections Framework provide?

> [!abstract] Short answer
> Behind the interfaces the JDK implements six classic machines: a **dynamic array** (`ArrayList`, `ArrayDeque`'s circular variant), a **doubly-linked list** (`LinkedList`), a **hash table** (`HashMap`/`HashSet`, extended with a linked list for `LinkedHashMap`/`LinkedHashSet`), a **red-black tree** (`TreeMap`/`TreeSet`), a **binary heap** (`PriorityQueue`), and the plain fixed-size **array** bridged through `Arrays` utilities.

## Which machine runs which type

The implementation docs are explicit. `ArrayList` — "resizable-array implementation of the `List` interface"; `LinkedList` — a doubly-linked list whose indexed operations "traverse the list from the beginning or the end, whichever is closer"; `HashSet` — a hash table, "actually a `HashMap` instance"; `LinkedHashSet`/`LinkedHashMap` add a "doubly-linked list running through all of its entries" so iteration order follows insertion; `TreeMap` is "a Red-Black tree based `NavigableMap` implementation" with "guaranteed log(n) time cost"; `PriorityQueue` — "an unbounded priority queue based on a priority heap" ([[What are the time complexities of PriorityQueue operations]]); `ArrayDeque` — a resizable-array `Deque` with no capacity limits ([[How do you use a Deque as a stack]]).

```d2
direction: right
ds: "Data structure" {
  width: 190
  height: 64
  style.fill: "#e3f2fd"
}
arr: "Dynamic array\nArrayList · ArrayDeque" {
  width: 280
  height: 72
  style.fill: "#e8f5e9"
}
list: "Doubly-linked list\nLinkedList" {
  width: 260
  height: 72
  style.fill: "#e8f5e9"
}
hash: "Hash table\nHashMap · HashSet ·\nLinked* (+ linked list)" {
  width: 300
  height: 88
  style.fill: "#fff3e0"
}
tree: "Red-black tree\nTreeMap · TreeSet" {
  width: 260
  height: 72
  style.fill: "#fff3e0"
}
heap: "Binary heap\nPriorityQueue" {
  width: 240
  height: 72
  style.fill: "#ffebee"
}
ds -> arr
ds -> list
ds -> hash
ds -> tree
ds -> heap
```

**Fig. 1.** One structure can serve several types: the hash table powers both `Set` and `Map` sides, and the linked list appears both standalone (`LinkedList`) and inside `Linked*` classes.

## Choosing by operation, not by interface

The structure decides the costs. A dynamic array gives O(1) indexed reads and amortized O(1) appends but O(n) middle inserts ([[What backing data structure does ArrayList use internally]]); a linked list splices its ends in O(1) but walks for indexed access ([[When should you prefer LinkedList over ArrayList]]); a hash table trades ordering for expected constant-time lookup ([[What is a HashMap]]); the tree keeps keys sorted with O(log n) operations and supports range views ([[How do you customize TreeMap key order]]); the heap gives the cheapest "smallest element first" — O(log n) `offer`/`poll`, with iteration that is *not* sorted ([[Does iterating a PriorityQueue return elements in sorted order]]).

```java
PriorityQueue<Integer> top = new PriorityQueue<>();
top.addAll(List.of(7, 1, 5));
System.out.println(top.poll());                       // smallest, not first inserted

TreeMap<String, Integer> byName = new TreeMap<>();
byName.put("b", 2); byName.put("a", 1); byName.put("c", 3);
System.out.println(byName);                           // sorted by key
```

**Listing 1.** Heap vs tree behavior. Verified on JDK 21 — output: `1` / `{a=1, b=2, c=3}`.

> [!warning] The interface name does not tell you the structure
> A `Set` can be a hash table, a linked hash table, or a red-black tree — the interface is the contract, the implementation is the machine. Interviewers exploit this: "iterate a `PriorityQueue`" yields heap-array order, not sorted order, and `TreeSet.contains` is O(log n) while `HashSet.contains` is expected O(1) — same interface method, different machines ([[What is a HashSet]], [[Is TreeSet implemented using TreeMap]]).

> [!tip] Interview answer
> **The framework's main structures are the dynamic array, doubly-linked list, hash table, red-black tree, and binary heap — implemented as `ArrayList`/`ArrayDeque`, `LinkedList`, `HashMap` family, `TreeMap`/`TreeSet`, and `PriorityQueue`.** Array gives fast random access, hash gives expected O(1) lookup without order, tree keeps sorted order at O(log n), heap answers "peek smallest" cheaply, and the linked list shines only at the ends.
