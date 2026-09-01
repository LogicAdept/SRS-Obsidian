<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #SRS

# What is the worst case time complexity of contains on a LinkedList when the element exists?

> [!abstract] Short answer
> **`Θ(n)` even when the element is present.** `contains` is `indexOf(o) >= 0`. `indexOf` walks from `first` with `== null` or `o.equals` and stops at the **first** match. If that match is the last node, you still visit every `Node`. Presence is not a hash lookup.

## Existing does not mean early exit from the tail

“The element exists” only means `indexOf` will return some index `≥ 0` instead of `-1`. It does not start at `last`, and it does not use the nearer-end walk of `get(i)` [[What is the time complexity of random access by index in a LinkedList]] [[How do you iterate elements LinkedList in order not using get(index]]. Worst case among hits: the first `equals` (or `null`) success is the tail — **`Θ(n)` node visits**, same order as a miss. Best hit is `first` (`Θ(1)`). Interview bound stays **`O(n)`** [[What is the time complexity of finding an element in a LinkedList]]. `equals` that is O(k) in the payload makes wall-clock O(n·k).

Duplicates do not help the worst case: `contains` only needs one hit, but the adversary puts that first hit at the end. `lastIndexOf` would be cheap for a last-node hit and expensive for a first-node hit; `contains` does not call it. `ArrayList.contains` is also a linear scan; existence there is likewise `Θ(n)` worst (last slot) [[What is the worst case time complexity of contains on an ArrayList when the element exists]] [[How do you search and remove elements in a List]]. `equals` on a heavy payload can add per-node work; the walk is still linear in size.

```d2
direction: right
h: "first\nno match" {
  width: 110
  height: 70
  style.fill: "#e3f2fd"
}
m: "…" {
  width: 50
  height: 50
}
t: "last\nexists → true" {
  width: 140
  height: 70
  style.fill: "#ffcdd2"
}

h -> m -> t
```

**Fig. 1.** Present-but-last is the worst hit: `contains` still walked the whole chain.

```java
java.util.LinkedList<String> list = new java.util.LinkedList<>();
list.add("a");
list.add("b");
list.add("c");
boolean hit = list.contains("c"); // true, and still Θ(n) — first match is last
```

**Listing 1.** Conceptual: a true result can still mean n `equals` tests. `get(n-1)` would be `Θ(1)`; `contains` is not `get`.

> [!warning] `true` ≠ `O(1)`
> Interviewers add “when it exists” to trap “then it’s constant.” `contains` cannot know it exists without scanning. Last-node present is as bad as absent for `indexOf` from `first`. Do not quote `getLast` or `node(i)` from the tail.

> [!warning] Not `HashSet`, `getLast`, or `add`
> Doubly-linked `prev`/`next` do not make membership `O(1)`. `HashSet.contains` is the expected-constant lookup. `getLast` / `peekLast` are `Θ(1)` and still not a search. Tail `add` / `addFirst` are `Θ(1)` pointer updates; `add(index, e)` is an O(n) walk. Neither is `contains`.

> [!tip] Interview answer
> **Worst case `Θ(n)` even if present** — first match can be the last node. `contains` → `indexOf` from `first`. Contrast `get(n-1)` (`Θ(1)`) and `HashSet`. Same linear story as `ArrayList.contains`, plus pointer chasing.
