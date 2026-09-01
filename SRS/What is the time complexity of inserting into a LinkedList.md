<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #SRS

# What is the time complexity of inserting into a LinkedList?

> [!abstract] Short answer
> **At an end, or at a cursor you already hold: `Θ(1)` to splice one `Node`.** `add(E)` / `addLast` call `linkLast`; `addFirst` calls `linkFirst`. **`add(int index)` is `O(n)`:** `node(index)` walks from the nearer end, then `linkBefore` (or `linkLast` if `index == size`) is `Θ(1)`. “Insert is always `O(1)`” is the usual wrong slogan.

## Splice is cheap; finding the slot may not be

`LinkedList` is a doubly-linked sequential list [[What design idea does LinkedList implement]]. Allocating and wiring one `Node` (`prev` / `item` / `next`) does not shift the rest of the list. That is why an end insert or a `ListIterator.add` is constant time [[How much extra memory does LinkedList add allocate per insertion]] [[Does LinkedList implement Queue and Deque in Java]].

`add(int index)` is different: it `checkPositionIndex`, then if `index == size` it `linkLast`, else `linkBefore(element, node(index))`. `node(index)` walks `next` from `first` when `index < size >> 1`, else `prev` from `last` — same nearer-end walk as `get` [[What is the cost of accessing the middle element of a LinkedList]]. Locate is `Θ(min(index, n − index))`; worst index is the middle (`Θ(n)`). The splice after that is still `Θ(1)`.

`addAll(Collection)` is `addAll(size, c)`: find the tail in `Θ(1)`, then link `m` new nodes (`O(m)`). `addAll(int, c)` pays `node(index)` first unless the index is `size`. Value search (`contains`) is a separate `O(n)` walk from `first` and is not how insert locates a hole [[What is the time complexity of finding an element in a LinkedList]].

```d2
direction: down
ends: "add / addFirst / addLast\nListIterator.add" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
idx: "add(int index)\nnode(index) then splice" {
  width: 240
  height: 70
  style.fill: "#ffe0b2"
}
cheap: "Θ(1) linkFirst / linkLast / linkBefore" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
walk: "O(n) walk to the slot" {
  width: 220
  height: 70
  style.fill: "#ffcdd2"
}

ends -> cheap
idx -> walk -> cheap
```

**Fig. 1.** End and iterator inserts skip the walk. Indexed insert pays `node(index)` first.

```java
java.util.LinkedList<String> list = new java.util.LinkedList<>();
list.add("a");              // linkLast — Θ(1)
list.addFirst("b");         // linkFirst — Θ(1)
list.add(1, "c");           // node(1) then linkBefore — O(n) to locate
```

**Listing 1.** Conceptual: append/prepend are constant; `add(index, …)` walks, then splices.

> [!warning] `O(1)` insert is not `add(i)`
> Interview “LinkedList insert is `O(1)`” means **you already know the neighbor** (ends, or `ListIterator`). `add(i)` on a large list is `O(n)` because of `node(i)`, even though no array shift happens. Middle insert is the expensive index, same as `get`.

> [!warning] Do not confuse with `ArrayList` or with `contains`
> `ArrayList.add(i)` shifts tail elements (`O(n)` data moves). `LinkedList.add(i)` shifts nothing but still walks. `add(E)` does not search for a value; `contains` / `indexOf` are the `O(n)` find path.

> [!tip] Interview answer
> **Ends and iterator: `Θ(1)` one-node splice (`linkFirst` / `linkLast` / `linkBefore`). Indexed `add(i)`: `O(n)` to find the node, `Θ(1)` to link.** `add(E)` is `linkLast`, not `add(0)`. Quote the method, not “LinkedList insert”.
