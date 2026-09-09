<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Search #Java/Arrays #SRS

# What search algorithms exist for arrays

> [!abstract] Short answer
> Two workhorses: **linear search** — scan elements one by one, works on any array, O(n); **binary search** — repeatedly halve a sorted array by comparing the middle element, O(log n), implemented by `java.util.Arrays.binarySearch`. Binary search is only valid on sorted data: on an unsorted array its result is undefined.

## Linear search

Compare every element with the key and return the index of the first match, or `-1`. It needs no ordering, no comparability beyond equality, and it is optimal for small or unsorted arrays. Its cost is the whole scan: for n elements the worst case is n comparisons, so on large data you either sort once and switch to binary search or move to hash-based structures (`HashSet` / `HashMap`), which trade memory for O(1) average lookup.

## Binary search and the sorted precondition

Binary search compares the key with the middle element and discards the half that cannot contain it, halving the search space each step: 10 million elements need about 24 comparisons. The precondition is total order — the array must be sorted (by the same ordering the search uses; for object arrays, the same comparator). Sorting costs O(n log n), so the win materializes when you search many times; a single lookup on unsorted data is cheaper with one linear scan. The JDK ships the algorithm as `Arrays.binarySearch` for every primitive type and object arrays, and the same contract lives in `Arrays.binarySearch`'s behavior on misses — see [[What does Arrays.binarySearch return for an unsorted array]].

```java
String[] names = {"Carol", "Alice", "Bob", "Dave"};
int linear = indexOf(names, "Bob");
System.out.println("linear search for Bob: index " + linear);
Arrays.sort(names);
System.out.println("sorted: " + Arrays.toString(names));
int binary = Arrays.binarySearch(names, "Bob");
System.out.println("binary search for Bob: index " + binary);
```

**Listing 1.** Output on JDK 21: `linear search for Bob: index 2`, then after sorting `[Alice, Bob, Carol, Dave]` the binary search finds `Bob` at index 1 — indexes shift once the array is sorted.

```d2
direction: right
linear: "Linear scan\ncompare a[0], a[1], ...\nany array, O(n)" {
  width: 280
  height: 120
  style.fill: "#e3f2fd"
}
sort: "Sorted?\nsort first, O(n log n)" {
  width: 240
  height: 100
  style.fill: "#fff3e0"
}
binary: "Binary halving\ndiscard half each step\nO(log n)" {
  width: 260
  height: 120
  style.fill: "#e8f5e9"
}
linear -> sort: "many lookups ahead"
sort -> binary
```

**Fig. 1.** Linear search needs no preconditions; binary search buys O(log n) with a sorted array, so the sort cost must amortize over many searches.

> [!warning] No exception for the unsorted case
> `Arrays.binarySearch` does not verify sortedness and does not throw: on `{8, -3, 10, 4}` searching `8` returned `-3` on JDK 21 — a well-formed-looking number that means nothing. The sorting algorithms the JDK uses for arrays are covered in [[Which algorithms sorting arrays used in Java]].

> [!tip] Interview answer
> Linear search: O(n), any array, first match wins. Binary search: O(log n), requires the array to be sorted by the same ordering, and the JDK's `Arrays.binarySearch` returns the index or the negated insertion point minus one — undefined garbage if the input was never sorted.

