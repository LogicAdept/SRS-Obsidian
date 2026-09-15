<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Sorting #SRS

# What is counting sort

> [!abstract] Short answer
> A sort for **integer keys in a small known range** `[0..k]`: tally how many times each key occurs, turn the tallies into prefix sums, and place elements into the output by their counts. It runs in **O(n + k)** time and space — beating the Ω(n log n) comparison-sort lower bound precisely because it **never compares** two elements; it is **stable** when placement sweeps right-to-left and **not in-place**. The JDK uses it inside Dual-Pivot Quicksort for `byte`, `short` and `char` arrays.

## Mechanism: count, prefix, place

Three linear passes. First, count occurrences of every key value into `count[key]`. Second, prefix-sum the counts so `count[v]` becomes the number of elements with key ≤ `v` — the end position of bucket `v` in the output. Third, sweep the input **right-to-left**, decrementing `count[key]` and copying each element to `output[count[key] − 1]`; the right-to-left sweep plus prefix sums is what preserves the original order of equal keys — stability, which makes the algorithm usable as a stable digit pass inside radix sort.

```java
// Stable counting sort for keys in [0..k] (conceptual)
static int[] countingSort(int[] a, int k) {
    int[] count = new int[k + 1];
    for (int x : a) count[x]++;                 // 1) tally
    for (int v = 1; v <= k; v++) count[v] += count[v - 1]; // 2) prefix sums
    int[] out = new int[a.length];
    for (int i = a.length - 1; i >= 0; i--)     // 3) right-to-left = stable
        out[--count[a[i]]] = a[i];
    return out;
}
```

**Listing 1.** `O(n + k)` in three passes: the cost is driven by the range `k`, not by `n log n`, because no two elements are ever compared.

## Preconditions and where the JDK hides it

The keys must be integers — or mappable to integers without losing order — and `k` must be modest: memory and time scale with the **range**, so sorting 1 000 arbitrary `int` values (range up to ~2³¹) by counting is a 2-gigabyte non-starter. Negative keys shift by an offset; a sparse huge range is the domain of comparison sorts instead. The JDK's Dual-Pivot Quicksort contains dedicated `countingSort` methods for `byte`, `short` and `char` arrays — types whose key range is tiny by construction — as documented in [[Which algorithms sorting arrays used in Java]]; general `int` arrays stay with quicksort, and object sorting stays with Timsort because objects have no integer identity to count.

> [!warning] It is not a general-purpose sort
> "Counting sort is O(n), so it is faster than quicksort" holds only while `k = O(n)`-ish: the bound is linear in the **value range**, and a range like 2³¹ breaks both time and memory regardless of `n`. It also cannot sort arbitrary objects by a comparator — there are no comparisons to make — and it is not in-place: the output goes to a separate buffer (the in-place semantics are contrasted in [[What is an in-place sorting algorithm]]).

> [!tip] Interview answer
> Counting sort tallies each integer key, prefix-sums the counts into bucket boundaries, and places elements right-to-left so equal keys keep their order — O(n + k) time and space, stable, no comparisons at all. That's how it beats the Ω(n log n) comparison lower bound: the bound simply doesn't apply. Preconditions are everything — keys must map to a small integer range, which is why the JDK reserves it for byte, short and char arrays inside its quicksort.
