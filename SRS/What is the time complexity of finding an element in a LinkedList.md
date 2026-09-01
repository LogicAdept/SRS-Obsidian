<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #SRS

# What is the time complexity of finding an element in a LinkedList?

> [!abstract] Short answer
> **Linear: `O(n)`.** `contains` is `indexOf(o) >= 0`. `indexOf` walks from `first` with `== null` or `o.equals` until a hit or the tail. Presence does not make it faster than a scan: if the match is last (or missing), you still visit every node. `lastIndexOf` is the same bound from `last`. There is no hash table.

## Value search walks the chain

`LinkedList` is a doubly-linked sequence, not a map [[Is Java LinkedList a singly or doubly linked list]]. Finding an element by value (`contains`, `indexOf`, `lastIndexOf`, `remove(Object)`) follows next/prev pointers. `indexOf` always starts at `first`; it does **not** use the nearer-end trick that `get(int)` uses [[What is the cost of accessing the middle element of a LinkedList]] [[What is the worst case time complexity of contains on a LinkedList when the element exists]].

If the target is at index `k` from the head, `indexOf` / `contains` do `Θ(k)` node visits. Best case is the first node (`Θ(1)`). Worst case — last node, or not present — is `Θ(n)`. Interview shorthand is **`O(n)`**. `lastIndexOf` is `Θ(n − k)` from the tail, still `O(n)` worst. `equals` on a large element can add work per visit; the node walk is still linear in size.

`List` already warns that search methods are often costly linear scans [[What is the List interface in Java]] [[How do you search and remove elements in a List]]. `ArrayList.contains` is also `O(n)` (array scan); the LinkedList extra is pointer chasing and no random access to skip ahead.

```d2
direction: right
n0: "first\n?equals" {
  width: 110
  height: 70
  style.fill: "#e3f2fd"
}
n1: "…" {
  width: 50
  height: 50
}
n2: "match or last" {
  width: 130
  height: 70
  style.fill: "#ffe0b2"
}

n0 -> n1 -> n2
```

**Fig. 1.** `contains` / `indexOf` walk from `first`. No jump to the middle.

```java
java.util.LinkedList<String> list = new java.util.LinkedList<>();
list.add("a");
list.add("b");
list.add("c");
boolean hit = list.contains("c"); // walks a → b → c; still O(n) in size
int i = list.indexOf("c");        // 2; same walk
int last = list.lastIndexOf("a"); // from last toward first
```

**Listing 1.** Conceptual: value search is a chain walk. `contains("c")` is true and still linear in `n`.

> [!warning] Present ≠ `O(1)`
> `contains` does not stop in constant time just because the element is in the list. A match on the last node (or a miss) visits every `Node`. Do not quote `get(i)`’s nearer-end walk as the cost of **finding by value**.

> [!warning] `LinkedList` is the wrong tool for membership
> Repeated `contains` on a large list is `O(n)` per call. Use a `HashSet` (or keep both a list and a set) when you need expected-constant lookups. `List.of` / `ArrayList` search is also linear; switching away from `LinkedList` does not by itself give `O(1)` `contains`.

> [!tip] Interview answer
> **`O(n)`.** `LinkedList.contains` delegates to `indexOf`, which scans from the head. Best case first node, worst case last or absent. Same bound for `lastIndexOf` from the tail. Contrast `get(i)` (walk from the nearer end) and `HashSet.contains` (hash bucket), not “doubly-linked so find is `O(1)`”.
