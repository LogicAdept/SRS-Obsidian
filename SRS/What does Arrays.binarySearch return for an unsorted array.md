<!--
reps: 0
priority: 0
-->
#Java/Arrays #SRS

# What does Arrays.binarySearch return for an unsorted array

> [!abstract] Short answer
> **Undefined.** The contract requires the array to be sorted first; on unsorted input the method neither throws nor reports an error — it returns some `int` that means nothing. On a sorted array the result is the index of the key, or `-(insertion point) - 1` when the key is absent.

## The contract

`Arrays.binarySearch(a, key)` returns a non-negative value if and only if the key was found. On a miss it returns `-(insertion point) - 1`, where the insertion point is the index of the first element greater than the key, or `a.length` when all elements are smaller. The encoding is deliberately unambiguous: `-1` means the key is smaller than everything (insertion point 0), `-(a.length) - 1` means larger than everything, and `ret >= 0` always means "found at that index". With duplicate keys there is no guarantee **which** matching index you get. None of this is valid unless the array was sorted (as by `Arrays.sort`); the unsorted case is simply declared "results are undefined" — see [[What search algorithms exist for arrays]] for when binary search is the right tool at all.

```java
int[] array = {8, -3, 10, 4};
System.out.println(Arrays.binarySearch(array, 8));  // -3 on JDK 21 — undefined by contract
Arrays.sort(array);                                  // [-3, 4, 8, 10]
System.out.println(Arrays.binarySearch(array, 8));   // 2  — found
System.out.println(Arrays.binarySearch(array, 9));   // -4 — insertion point 3: -(3) - 1
System.out.println(Arrays.binarySearch(array, -5));  // -1 — insertion point 0
System.out.println(Arrays.binarySearch(array, 99));  // -5 — insertion point 4 == a.length
```

**Listing 1.** Output on JDK 21: on the unsorted `{8, -3, 10, 4}` the search for `8` returned `-3`, which decodes to "insertion point 2" but has no real meaning; after sorting, every value matches the contract exactly.

## How the encoding is used

```d2
direction: down
search: "Arrays.binarySearch(a, key)" {
  width: 320
  height: 90
  style.fill: "#e3f2fd"
}
found: "ret >= 0\nkey at index ret" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
miss: "ret < 0\ninsertion point = -ret - 1" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
insert: "insert at that index\nto keep the array sorted" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
search -> found: "sorted input"
search -> miss: "sorted input"
miss -> insert
```

**Fig. 1.** On sorted input the return value answers two questions at once: where the key is, or where it would belong — the negative value is a usable insertion point.

The insertion-point behavior is the practical reason to remember the formula: to insert while keeping sorted order, compute `int ip = -(Arrays.binarySearch(a, key)) - 1;` and place the key at that index. The algorithm behind the contract is the classic halving loop, so it is O(log n) — but only meaningful after a sort, which costs O(n log n) and shifts indexes, as the sorted output in the listing shows. The JDK sort algorithms themselves are compared in [[Which algorithms sorting arrays used in Java]].

> [!warning] The formula is not a validity check
> On unsorted input the returned number can still look like a legitimate insertion point (here `-3`), which makes the bug silent: no exception, no flag. If the data is not provably sorted, sort it first or fall back to a linear scan.

> [!tip] Interview answer
> For an unsorted array the result is undefined — the precondition is sortedness, and nothing is thrown if it is violated. On a sorted array you get the key's index, or `-(insertion point) - 1` on a miss, so `-1` means "smaller than all" and `-(length) - 1` means "larger than all"; the negative return doubles as the insertion index.

