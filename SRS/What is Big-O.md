<!--
reps: 0
priority: 0
-->
#DSA/Complexity #SRS

# What is Big-O

> [!abstract] Short answer
> Big-O describes how a running time (or memory need) **grows as the input grows**, ignoring constant factors and machine details: `f(n) = O(g(n))` when, for large enough `n`, `f(n)` never exceeds `c·g(n)` for some constant `c`. It is a growth **bound**, not a stopwatch measurement, and not by itself a statement about worst or average cases.

## The definition and what it hides

`f(n) = O(g(n))` means there exist constants `c > 0` and `n₀ ≥ 1` such that `f(n) ≤ c·g(n)` for all `n ≥ n₀`. For example, a loop body doing `3n² + 5n + 7` operations is `O(n²)` — pick `c = 4`, and `4n²` dominates everything from some small `n₀` on. What the notation deliberately drops: constant multipliers (a hash lookup costing 5 units is still `O(1)`), lower-order terms (`n² + n` is `O(n²)`), and any fixed input-independent overhead. Sibling notations tighten the picture: `Ω(g(n))` is a lower growth bound and `Θ(g(n))` means the growth matches `g(n)` from both sides — saying `O(n²)` about an `O(n)` algorithm is true but misleadingly loose.

One strong fact comes from the model itself: any sort that only **compares** pairs of elements needs `Ω(n log n)` comparisons in the worst case, which is why merge sort, heap sort and Timsort all sit at `O(n log n)` and why non-comparing algorithms like counting sort can go faster.

## Common growth classes

| Growth | Typical source in this vault |
|---|---|
| `O(1)` | hash-table lookup on average, array index access |
| `O(log n)` | binary search, balanced-tree operations |
| `O(n)` | one linear scan, building a visited set |
| `O(n log n)` | comparison sorts: merge sort, Timsort, heap sort |
| `O(n²)` | insertion sort, bubble sort on random data, nested loops |
| `O(2ⁿ)` | naive recursive Fibonacci, exhaustive subsets |

```java
// Two scans over the same array: n + n = O(n), not 2n — constants vanish
int sum = 0;
for (int x : a) sum += x;          // n steps
int max = Integer.MIN_VALUE;
for (int x : a) if (x > max) max = x;  // n steps
```

**Listing 1.** Sequential loops **add** their costs (`O(n) + O(n) = O(n)`); nested loops **multiply** (`O(n) × O(n) = O(n²)`).

## Bound is a separate axis from case

Big-O says nothing about *which* input you got — worst case, average case, and amortized cost are independent dimensions. Quicksort is `O(n log n)` on average but `O(n²)` in the worst case, and both statements use Big-O. Hash lookup is `O(1)` on average under a decent hash function and degrades to `O(n)` when all keys collide — see [[Does HashMap guarantee its documented lookup time complexity]]. Quoting only the average without its preconditions is the classic interview miss.

> [!warning] "Big-O = worst case" is a conflation
> The `O`-notation bounds growth; the *case* (best/average/worst/amortized) is chosen separately. Quicksort's `O(n log n)` average and `O(n²)` worst case are both Big-O statements. Similarly, an `O(1)` claim for a hash lookup is true only on average and only with a sane hash — the guarantee lives in [[Does HashMap guarantee its documented lookup time complexity]], not in the notation itself.

> [!tip] Interview answer
> Big-O gives an upper bound on how cost grows with input size, up to constant factors: formally `f ≤ c·g` for large `n`. It ignores constants and lower-order terms, so `3n² + n` is `O(n²)`. I always pair it with the case — worst, average, amortized — because they are independent: HashMap get is `O(1)` average, `O(n)` worst; quicksort is `O(n log n)` average, `O(n²)` worst. Comparison sorting can't beat `O(n log n)` in the worst case, which fixes the floor for comparison-based sorts.
