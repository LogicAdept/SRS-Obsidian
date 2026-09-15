<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Sorting #SRS

# What is Timsort

> [!abstract] Short answer
> An **adaptive, stable merge-sort hybrid** by Tim Peters (2002, for Python; in OpenJDK since Java 7). It scans once, harvesting naturally ordered **runs**, extends short runs with **binary insertion sort**, then merges runs with a balanced stack of merges that can switch to **galloping** on highly structured data. Worst case `O(n log n)`, best case `O(n)` on already-sorted input. It is the standard sort for **object** arrays and collections in Java; primitives take Dual-Pivot Quicksort instead.

## How a pass works

The main loop marches left to right: identify the next run (a maximal ascending sequence, or descending — reversed in place), and if the run is shorter than `minRun` it is grown to `minRun` with binary insertion sort before being pushed on the merge stack. OpenJDK's `TimSort` computes this `minRunLength` from `MIN_MERGE = 32`, keeping run lengths in a band so the pending-run stack stays shallow and merges stay balanced. When the run on top of the stack becomes dominant, the merge fires; inside a merge, if one run keeps winning consecutively, the comparison switches to **gallop mode** — exponential search for the insertion point — which is where the adaptive speedup on partially ordered data comes from.

```java
// Run detection (conceptual, mirrors TimSort.countRunAndMakeAscending):
int i = 1;
if (a[1] < a[0]) {                              // start is descending:
    while (i + 1 < a.length && a[i] > a[i + 1]) i++;
    reverse(a, 0, i);                           // flip it to ascending
} else {                                        // start is ascending:
    while (i + 1 < a.length && a[i] <= a[i + 1]) i++;
}
int runLength = i + 1;
```

**Listing 1.** The direction is chosen once, from the first pair: ride the rise, or ride the fall and reverse it in place. Timsort then grows short runs to `minRun` by binary insertion before merging.

## Where it lives in Java

`Arrays.sort(Object[])`, `Collections.sort` and `List.sort` all land on Timsort for object references — and the `Arrays` specification only promises that object sorting is **stable**, leaving the algorithm swappable, while the OpenJDK implementation note names the sort-merge (Timsort) machinery and a working space no larger than the original array. Primitive arrays have no stability to preserve (equal `int`s are indistinguishable), so they go to Dual-Pivot Quicksort — the split is documented in [[Which algorithms sorting arrays used in Java]] and reachable from user code via [[How do you sort a list of strings with a lambda in Java]].

> [!warning] Stability is an objects-only guarantee, and memory is not free
> `Arrays.sort(int[])` is **not** stable and needs no such promise — equal primitives carry no identity. Expecting stable order from a primitive sort, or sorting objects through a comparator that treats distinct objects as equal while assuming the previous order survives — only the object path guarantees that. On random data Timsort may allocate a temp buffer of up to `n/2` references; on strongly structured input it needs none.

> [!tip] Interview answer
> Timsort is the adaptive, stable merge-sort hybrid behind object sorting in Java since 7: it harvests naturally occurring runs, pads short ones with binary insertion, and merges the run stack, galloping when one side keeps winning. Worst case O(n log n), O(n) on sorted input, and stability is guaranteed for objects — primitives take Dual-Pivot Quicksort instead. Its superpower is real-world data, where pre-existing order is common.
