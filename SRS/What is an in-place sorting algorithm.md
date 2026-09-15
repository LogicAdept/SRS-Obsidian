<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Sorting #SRS

# What is an in-place sorting algorithm

> [!abstract] Short answer
> A sort that rearranges elements **inside the original storage** using only a bounded amount of extra memory beyond the input — `O(1)` working space, or `O(log n)` if the recursion stack counts. Insertion, bubble and selection sorts, heapsort and quicksort are in-place; the classic merge sort (`O(n)` buffer) and counting sort (`O(n + k)`) are not. In-place means memory-frugal **and** input-destructive: the original order is gone.

## Why the property matters

Two reasons keep the property on interview checklists. First, memory: a sort running inside a tight heap, an embedded runtime, or a streaming pipeline cannot afford a second copy of a multi-gigabyte array — heapsort, for example, sorts by reusing the input array as its own binary heap. Second, cache behavior: data moved within the same array stays near the CPU's cache lines, which is a real part of why quicksort and insertion sort outperform their paper complexity in benchmarks.

## The gray zone: stacks, buffers, and semantics

"Extra memory" needs a definition to be honest about. Quicksort writes everything into the input array but holds an `O(log n)` recursion stack — conventionally still called in-place, and `O(n)` stack on degenerate pivots is exactly the leak. Bottom-up heapify uses `O(1)` auxiliary storage outright, making heapsort the cleanest `O(n log n)`-worst-case in-place sort — its array packing is described in [[What is a heap as a data structure]]. Classic merge sort, by contrast, copies each merge into a scratch buffer; its linked-list form sneaks back to `O(log n)` because it rewires pointers instead of copying elements. Research-level "in-place merge" variants exist and are too intricate for production — a nuance spelled out in [[What is merge sort]].

```java
int[] data = {5, 3, 1, 4};
int[] copy = data.clone();

Arrays.sort(data);                       // in-place: data now {1, 3, 4, 5}
System.out.println(Arrays.equals(data, copy)); // false — original is gone
```

**Listing 1.** The JDK sorts mutate their argument; anything needing the original order must copy first — `clone()`, or keep the original untouched by sorting indices instead.

> [!warning] In-place does not mean O(1) — and it means destructive
> Two traps in one term. The recursion stack of quicksort is extra memory even though every write lands in the input array; quoting a blanket "quicksort uses O(1) extra" invites the degenerate-pivot counterexample. And every in-place sort overwrites the input — passing a caller's array to `Arrays.sort` when order must survive is a live bug pattern, the same one [[Which algorithms sorting arrays used in Java]] walks through for the JDK's primitive and object paths.

> [!tip] Interview answer
> In-place means the sort reorders the original array with bounded extra memory — O(1) for heapsort and the elementary sorts, O(log n) counting quicksort's recursion stack, still conventionally in-place. Merge sort and counting sort are the standard counterexamples, needing O(n) and O(n+k) buffers. Two consequences I always state: it is memory- and cache-friendly, and it destroys the input order — copy first if the original matters.
