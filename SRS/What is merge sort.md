<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Sorting #SRS

# What is merge sort

> [!abstract] Short answer
> A divide-and-conquer sort: split the array in half, sort each half recursively, then **merge** the two sorted halves with a two-pointer pass. It guarantees **O(n log n)** in every case — best, average, worst — and it is **stable**, but the classic array version needs an **O(n) auxiliary buffer**, so it is not in-place.

## The merge step

Merging two already-sorted halves is the whole trick: keep one index per half, repeatedly take the smaller front element into the output, advancing that half's index. On a tie, take from the **left half first** — that one-line convention is what makes merge sort stable, because left-half elements originally stood before right-half elements. Each merge level processes all `n` elements, and halving gives `log n` levels, hence `O(n log n)` regardless of the input's initial order.

```java
// Merge a[lo..mid) and a[mid..hi) — both sorted — into a scratch buffer
static void merge(int[] a, int[] buf, int lo, int mid, int hi) {
    System.arraycopy(a, lo, buf, lo, hi - lo);
    int i = lo, j = mid;
    for (int k = lo; k < hi; k++) {
        if (i >= mid)            a[k] = buf[j++];
        else if (j >= hi)        a[k] = buf[i++];
        else if (buf[j] < buf[i]) a[k] = buf[j++];   // strictly less:
        else                      a[k] = buf[i++];   // tie -> left, stable
    }
}
```

**Listing 1.** The stable merge: `buf[j] < buf[i]` takes from the right only when strictly smaller, so equal elements keep their original left-first order.

## Bottom-up variant and where Java uses it

The recursive top-down form halves indices; the iterative **bottom-up** form merges runs of width 1, 2, 4, … over the array — same complexity, no recursion. Java's object sorting long used a plain merge sort and today runs **Timsort**, which is a merge-sort hybrid — see [[What is Timsort]]. Outside the JDK, merge sort owns two niches where its "flaws" don't matter: **external sorting** (data far larger than memory is sorted as disk runs merged in passes) and **linked lists**, where merging rewires pointers and needs only `O(log n)` stack — no `O(n)` buffer.

> [!warning] "Merge sort is in-place" is the popular lie
> The textbook array version copies each merge into a scratch buffer of up to `n` elements. In-place merge algorithms exist but are intricate and rarely shipped. Quoting merge sort as "stable **and** in-place" in an interview invites the follow-up "then where does the output go?" — the honest pairing is [[What is an in-place sorting algorithm]] for contrast: quicksort and heap sort are in-place, merge sort trades memory for its guarantees.

> [!tip] Interview answer
> Merge sort splits in half, sorts recursively, and merges with a two-pointer pass — O(n log n) worst case guaranteed, stable when ties are taken from the left, but O(n) extra memory, so it's not in-place. Java uses its hybrid descendant Timsort for objects; merge itself dominates external sorting and linked lists. I'd pick it over quicksort when I need a guaranteed bound or stable order.
