<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/List/LinkedList #SRS

# Which is slower: `ArrayList` or `LinkedList` for `add(size()/2, e)`?

> [!abstract] Short answer
> **Both are linear** in the list length. `ArrayList` copies about half the backing array (`System.arraycopy`); `LinkedList` walks about `size()/2` nodes, then relinks. Indexed `add` is in `ArrayList`’s “other operations … linear time” bucket, with a **lower constant factor** than `LinkedList`. The dump that “middle insert is faster on `LinkedList`” is the usual myth for this exact call.

## Midpoint `add` is an index operation

```d2
direction: down
call: "list.add(list.size()/2, e)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
al: "ArrayList\nmaybe grow; arraycopy of n/2 slots" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
ll: "LinkedList\nwalk n/2 nodes from an end, then splice" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

call -> al
call -> ll
```

**Fig. 1.** Same `List.add(int, E)` shape; different work. Midpoint is the **farthest** index for `LinkedList` (equally far from both ends).

`ArrayList.add(int, E)` “shifts the element currently at that position (if any) and any subsequent elements to the right.” OpenJDK grows if `size == capacity`, then `arraycopy` from `index` through the old tail. End `add` is amortized O(1); **this is not end `add`** ([[Does ArrayList always add elements in O(1) time]], [[How does resize ArrayList]]).

`LinkedList` is a doubly-linked `List`/`Deque`. “Operations that index into the list will traverse the list from the beginning or the end, whichever is closer to the specified index.” For `size()/2` that walk is Θ(n). The link update itself is O(1) **after** you have the node. `add(int, E)` still has to find that node.

`ArrayList` documents that its linear operations have a **low constant factor compared to `LinkedList`**. Contiguous `arraycopy` is the reason dumps mention; it is not a license to assign a better **big-O** to `LinkedList` for this call.

```java
list.add(list.size() / 2, newElement);
```

**Listing 1.** The measured call. Same line on both types. A broader comparison: [[What is the difference between ArrayList and LinkedList]]; when the `Deque` ends matter: [[When should you prefer LinkedList over ArrayList]].

> [!warning] O(1) splice does not make indexed `add` O(1)
> People quote “`LinkedList` insert is O(1).” That is true for `addFirst` / `addLast` / `ListIterator.add` **at an already held cursor**. `add(size()/2, e)` must **get to** the middle first. `ArrayList` does not need a pointer walk; it pays a bulk copy of the right half.

> [!warning] Grow is not the usual cost of middle insert
> A full `ArrayList` may copy **all** elements once to a larger array, then copy the tail right — still O(n), rare if capacity was reserved. Every `LinkedList` midpoint `add` still walks Θ(n) nodes.

> [!tip] Interview answer
> **Both `add(size()/2, e)` calls are O(n).** `ArrayList` copies the right half; `LinkedList` walks n/2 links. The spec already says `ArrayList`’s linear work is cheaper per step than `LinkedList`. Don’t pick `LinkedList` just to insert in the middle by index.
