<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #SRS

# What is the worst case time complexity of add on a LinkedList?

> [!abstract] Short answer
> **`add(E)` is `Θ(1)` even in the worst case** — always `linkLast`, one new `Node`, no array copy. **`add(int index, E)` is `Θ(n)` worst case** because `node(index)` walks from the nearer end; the expensive index is the **middle**. Name the overload. Do not import `ArrayList`’s grow-and-copy worst case.

## `add(E)` has no expensive worst case

`LinkedList.add(E)` is `linkLast`: allocate a `Node`, hang it off `last` (or become both `first` and `last` if empty), bump `size`. Every call does that same constant work — empty list, huge list, or after many inserts. There is no capacity, so there is no “sometimes `O(n)` copy” the way `ArrayList.add` has [[What is the worst case time complexity of add on an ArrayList]] [[How much extra memory does LinkedList add allocate per insertion]]. `addLast` is the same path; `addFirst` is `linkFirst`, also `Θ(1)` [[Does LinkedList implement Queue and Deque in Java]] [[What is the time complexity of inserting into a LinkedList]].

`add(int index, E)` is the other method. If `index == size` it `linkLast` (`Θ(1)`). Otherwise it `linkBefore(element, node(index))`. `node` walks `min(index, n − index)` pointers, so **worst `index` is near `n/2`**: `Θ(n)` locate, then `Θ(1)` splice [[What is the cost of accessing the middle element of a LinkedList]] [[What is the time complexity of random access by index in a LinkedList]]. `ListIterator.add` at a cursor you already hold is `Θ(1)` again.

```d2
direction: down
addE: "add(E) / addLast\nlinkLast" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
addI: "add(int, E)\nnode(index) then splice" {
  width: 240
  height: 70
  style.fill: "#ffe0b2"
}
wc1: "worst case Θ(1)" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
wcn: "worst case Θ(n)\n(middle index)" {
  width: 200
  height: 70
  style.fill: "#ffcdd2"
}

addE -> wc1
addI -> wcn
```

**Fig. 1.** Worst case depends on which `add`. Collection `add(E)` never walks.

```java
java.util.LinkedList<String> list = new java.util.LinkedList<>();
list.add("a");        // add(E) → linkLast; worst case still Θ(1)
list.add(0, "b");     // add(int, E); here index 0 is cheap
list.add(1, "c");     // middle of a longer list is the Θ(n) case
```

**Listing 1.** Conceptual: `add("a")` is not `add(0, "a")`. Worst-case `add(E)` does not grow with `n`.

> [!warning] Do not quote `ArrayList` worst-case `add` here
> `ArrayList.add(E)` is amortized `O(1)` and **worst-case `O(n)`** on resize. `LinkedList.add(E)` does not copy an array; worst case stays `Θ(1)`. Allocation of one `Node` is still `Θ(1)` time (GC pauses are not the Collections answer).

> [!warning] Unqualified “`add` is `O(n)`” is the indexed overload
> If the interviewer said `add` without an index, they usually mean `Collection.add` / `add(E)` → `Θ(1)` worst case. If they mean `add(i, e)`, say **`Θ(n)` worst at the middle**, not “always `O(1)` because linked.”

> [!tip] Interview answer
> **`add(E)`: worst case `Θ(1)` (`linkLast`). `add(i, e)`: worst case `Θ(n)` (`node(i)` from the nearer end).** Contrast `ArrayList.add`’s resize. Ask which overload if they say only “add”.
