<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Sorting #SRS

# What is bubble sort

> [!abstract] Short answer
> A sort that walks the array comparing **adjacent pairs** and swapping the out-of-order ones, so the largest remaining key "bubbles" to the end each pass. **O(n²)** with `n(n−1)/2` worst-case comparisons; **stable** and **in-place**; with a no-swap early exit it becomes `O(n)` on sorted input — and still loses to insertion sort on every real measure, which is why it ships in no production library.

## Mechanism

Each pass sweeps left to right, swapping any adjacent pair that is in the wrong order; after pass `k`, the `k` largest keys occupy their final positions at the right, so the next pass can stop one position earlier. Adding a `swapped` flag gives the adaptive best case: a pass with zero swaps proves the array sorted and the loop exits — on an already-sorted array that is one pass of `n−1` comparisons.

```java
static void bubbleSort(int[] a) {
    for (int pass = 1; pass < a.length; pass++) {
        boolean swapped = false;
        for (int j = 0; j < a.length - pass; j++) {
            if (a[j] > a[j + 1]) {
                int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;  // 3 writes
                swapped = true;
            }
        }
        if (!swapped) return;            // already sorted: O(n) best case
    }
}
```

**Listing 1.** The shrinking boundary (`a.length - pass`) and the early-exit flag are the two textbook refinements; both are already present in this minimal form.

## Why it lost to insertion sort — same big-O, worse constants

Bubble sort and insertion sort have identical asymptotics, stability, and in-place memory use — the difference is entirely in constant factors, and it is damning. Every out-of-order adjacent pair costs bubble sort a full **swap** (three assignments, one temporary) where insertion sort performs a single **shift** (one assignment per moved element); on nearly-sorted data with a few displaced elements far from home, insertion sort moves each misplaced element directly to its slot, while bubble sort walks it one adjacent step at a time. OpenDSA's verdict is blunt: it has "no redeeming features" next to the equally simple insertion and selection sorts — bubble sort survives only as an interview punchline and a teaching device for [[What is an in-place sorting algorithm]] semantics and the growth classes in [[What is Big-O]].

> [!warning] The early exit does not rehabilitate it
> "Bubble sort with the swapped flag is fine on nearly-sorted data" is the popular half-truth: the best case improves to `O(n)`, but for the same nearly-sorted input insertion sort does fewer comparisons **and** roughly a third of the writes. Quoting bubble sort as a legitimate choice in an interview signals that the constant-factor layer — the layer where real sorting lives — has not been thought through; see the contrast with [[What is insertion sort]].

> [!tip] Interview answer
> Bubble sort swaps adjacent out-of-order pairs; each pass floats the largest remaining element to the end, shrinking the scan window. O(n²) average and worst, n(n−1)/2 comparisons, stable, in-place, and O(n) with an early-exit flag on sorted input. Same big-O as insertion sort, but every move costs a three-write swap instead of one shift — so it's a teaching tool, not a production sort; I'd always substitute insertion sort.
