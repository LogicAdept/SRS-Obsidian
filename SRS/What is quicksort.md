<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Sorting #SRS

# What is quicksort

> [!abstract] Short answer
> A divide-and-conquer sort that **partitions** the array around a pivot — smaller keys to the left, larger to the right — then recurses into the two sides. It is **in-place** (only an `O(log n)` recursion stack), cache-friendly, and typically the fastest comparison sort in practice: **O(n log n)** on average. Its worst case is **O(n²)** with bad pivots, and it is **not stable**.

## Partition: the step that does the work

Partitioning rearranges one subarray so the pivot lands at its final index: scan once, swapping every element that belongs to the "smaller" region to its front. Quicksort then sorts the two sides independently — unlike merge sort, all the work happens *before* the recursion (merge sort merges *after*), and there is nothing to combine, which is where its low constant factor and memory frugality come from.

```java
// Lomuto partition: pivot = a[hi]; returns the pivot's final index
static int partition(int[] a, int lo, int hi) {
    int pivot = a[hi];
    int i = lo - 1;                        // end of the "smaller" region
    for (int j = lo; j < hi; j++) {
        if (a[j] <= pivot) {
            i++;
            int t = a[i]; a[i] = a[j]; a[j] = t;
        }
    }
    int t = a[i + 1]; a[i + 1] = a[hi]; a[hi] = t;
    return i + 1;
}
```

**Listing 1.** After partition, the pivot sits at its sorted position — sorting the two flanks recursively finishes the job.

## Pivot choice and the quadratic trap

A first-element pivot on an already-sorted array partitions 0 : n−1 every time — `n²` comparisons for the input most likely in production. The standard defenses: pick the pivot **randomly**, use **median-of-three** (first, middle, last), or both. Production implementations add a depth guard: OpenJDK's Dual-Pivot Quicksort (Yaroslavskiy, Bentley, Bloch — the engine behind `Arrays.sort` for primitives since Java 7, promising `O(n log n)` on all data sets) switches small ranges to insertion sort and pathological recursion to heap sort. The full picture of what the JDK picks per input lives in [[Which algorithms sorting arrays used in Java]].

> [!warning] Two claims that do not survive a follow-up
> "Quicksort is always faster than merge sort" — false: its worst case is quadratic and it is **not stable**; merge sort's guarantee and stability are exactly why Java sorts objects with Timsort, a merge hybrid, and primitives with quicksort. And "quicksort needs no extra memory" is half-true at best — the recursion stack is `O(log n)` when the recursion is balanced, and `O(n)` on the degenerate inputs the pivot strategy exists to prevent; the space nuance is spelled out in [[What is an in-place sorting algorithm]].

> [!tip] Interview answer
> Quicksort partitions around a pivot — smaller left, larger right, pivot fixed — and recurses on both sides: in-place, cache-friendly, O(n log n) on average, O(n²) worst case, not stable. Pivot choice is everything: random or median-of-three kills the sorted-input trap, and the JDK's dual-pivot variant for primitives adds insertion and heap-sort fallbacks. I choose it for primitive arrays and raw speed, merge-based sorts when I need stability or a guaranteed bound.
