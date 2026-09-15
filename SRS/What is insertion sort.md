<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Sorting #SRS

# What is insertion sort

> [!abstract] Short answer
> A sort that grows a sorted prefix one element at a time: take the next element and **shift** prefix elements that are larger one slot right, then drop it in. **O(n²)** worst and average, but **O(n)** on already-sorted data — it is **adaptive**, **stable**, **in-place**, and the speed champion on small and nearly-sorted arrays, which is exactly why the JDK still runs it inside its production sorts.

## Mechanism

After `k` iterations, the first `k` elements are sorted (not just smaller — genuinely ordered, unlike quicksort's partitions). Element `k+1` is lifted out, all larger prefix elements slide one right, and the element settles into the gap. Because a new element never jumps over an equal one, equal keys keep their relative order — stability for free. On an already-sorted array each element costs one comparison and no shifts: a single pass, `O(n)`.

```java
static void insertionSort(int[] a) {
    for (int i = 1; i < a.length; i++) {
        int key = a[i];              // lift the next element out
        int j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];         // shift right (one write per move)
            j--;
        }
        a[j + 1] = key;              // settle into the gap
    }
}
```

**Listing 1.** The shift loop writes once per moved element; a swap-based version would write three times per move for the same effect.

## Why the JDK still ships a "textbook" sort

Inside Timsort, runs shorter than the minimum run size are finished with **binary insertion sort** — the shifting stays, but the insertion point is found by binary search, cutting comparisons to `O(log n)` per element. OpenJDK's Dual-Pivot Quicksort hands ranges up to `MAX_INSERTION_SORT_SIZE = 44` (and the mixed variant up to 65) to insertion sort outright. The reason: at tiny sizes, constant factors and cache behavior beat asymptotics — the same pattern catalogued in [[Which algorithms sorting arrays used in Java]].

> [!warning] Adaptive does not mean fast on random data
> On uniformly random input insertion sort does ~`n²/4` shifts — 10 000 random elements cost ~25 million writes, while an `O(n log n)` sort needs ~130 000. The second trap is the swapped cousin: "insertion sort and bubble sort are interchangeable" — they are both quadratic and stable, but insertion does strictly less work per move (one write vs three), which is why real code ships insertion and never bubble; the head-to-head is in [[What is bubble sort]].

> [!tip] Interview answer
> Insertion sort grows a sorted prefix: lift the next element, shift larger ones right, settle it in the gap — O(n²) worst and average, O(n) on nearly-sorted input, stable, in-place, and it works online as elements arrive. Production relevance: it finishes short runs inside Timsort and handles tiny ranges inside the JDK's quicksort, because small n is all constant factors. Great for nearly-sorted or tiny data, never for large random arrays.
