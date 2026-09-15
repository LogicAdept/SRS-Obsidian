<!--
reps: 0
priority: 0
-->
#DSA/DataStructures/Heap #SRS

# What is a heap as a data structure

> [!abstract] Short answer
> A **complete binary tree** with one order invariant — in a max-heap every parent is **≥ its children** (min-heap: ≤) — stored compactly **in an array** without pointers. It answers "give me the best element" in **O(1)** and insert/extract in **O(log n)**. It is built for repeated best-element access (priority queues, heapsort), **not** for search or sorted iteration. `java.util.PriorityQueue` is a min-heap of exactly this shape.

## Array layout and the order invariant

Completeness (every level full except possibly the last, filled left to right) is what makes the array packing work: with 0-based indexing the parent of `i` sits at `(i-1)/2` and its children at `2i+1` and `2i+2` — no pointers, no per-node objects, and better cache behavior than a tree of references. The heap-order invariant is deliberately weaker than BST order: nothing orders the left and right siblings, so an in-order walk is **not** sorted and you cannot binary-search a heap — the only cheap question is "who is the root?".

```java
// Sift-down: restore heap order after replacing the root (conceptual)
static void siftDown(int[] a, int i, int size) {
    while (true) {
        int best = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < size && a[l] > a[best]) best = l;
        if (r < size && a[r] > a[best]) best = r;
        if (best == i) return;               // parent dominates: done
        int t = a[i]; a[i] = a[best]; a[best] = t;
        i = best;                            // continue downward
    }
}
```

**Listing 1.** Each level fixes one comparison pair and drops one level — that is the `O(log n)` behind `extract-max` and behind the sift-down half of building a heap bottom-up.

## Operations and where Java ships one

`insert` appends at the first free slot and **sifts up**; `extract` removes the root, moves the last element into its place and sifts down; building all at once from an unsorted array (bottom-up heapify, the engine of in-place heapsort — [[What is an in-place sorting algorithm]]) is linear time. The JDK exposes this structure as `PriorityQueue`, a min-heap on natural order or a comparator — the per-operation costs are tabulated in [[What are the time complexities of PriorityQueue operations]], max-heap emulation is shown in [[How do you build a max-heap with PriorityQueue]], and [[Does iterating a PriorityQueue return elements in sorted order]] documents the iteration trap.

> [!warning] Two name collisions, two classic lies
> A data-structure **heap has nothing to do with the JVM heap** — the memory area where objects live (the one in heap dumps) merely shares the word. And "it's a tree, so I can search it" is wrong twice: heap order does not bound siblings, so finding an arbitrary element is `O(n)`, and `PriorityQueue.iterator()` returns array order, not sorted order — you must drain it with `poll()` to get sorted output.

> [!tip] Interview answer
> A heap is a complete binary tree in an array — parent at (i−1)/2, children at 2i+1 and 2i+2 — with a one-way order invariant: parents dominate children. Peek is O(1), insert and extract are O(log n) via sift-up and sift-down, and bottom-up construction is linear. It answers "best element next", not search or sorted iteration. PriorityQueue is the JDK's min-heap; the JVM heap is unrelated memory with the same name.
