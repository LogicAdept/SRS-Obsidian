<!--
reps: 0
priority: 0
-->
#Java/Arrays #Java/Collections/Sorting #SRS

# Which sorting algorithms does Java use for arrays?

> [!abstract] Short answer
> **`Arrays.sort` on primitives is Dual-Pivot Quicksort; on objects it is TimSort** (stable, adaptive mergesort). That split is the Java 7 implementation. Through Java 6 it was a tuned Bentley–McIlroy quicksort vs a modified mergesort. These are **implementation notes**, not the spec — object sorts must stay **stable**. `Integer[]` is objects, not `int[]`.

## Primitives versus objects

`Arrays.sort` is overloaded. Primitive arrays (`int[]`, `long[]`, `short[]`, `char[]`, `byte[]`, `float[]`, `double[]`) and object arrays (`Object[]`, `T[]` plus a `Comparator`) do **not** share an algorithm.

**Since Java 7** (still the Java SE 21 note):

- **Primitives:** Dual-Pivot Quicksort (Yaroslavskiy, Bentley, Bloch). Documented as O(n log n) on all data sets in SE 21, typically faster than one-pivot quicksort. **Not** required to be stable.
- **Objects:** TimSort — stable, adaptive, iterative mergesort from Tim Peters's Python list sort. Fewer than n lg(n) comparisons when the input is partially sorted; about n when nearly sorted; workspace from a small constant up to n/2 references. Equal elements keep their relative order.

**Through Java 6:**

- **Primitives:** tuned quicksort from Bentley and McIlroy, *Engineering a Sort Function* (1993). n log n on many data sets that send other quicksorts quadratic.
- **Objects:** modified mergesort (skip the merge when the two halves are already in order). Guaranteed n log n, **stable**.

`List.sort` / `Collections.sort` copy the list to an array, sort that array (TimSort since 7), and write back with `set` [[How do you sort a list of strings with a lambda in Java]].

Since 8, `Arrays.parallelSort` is a **parallel sort-merge**: split, sort subarrays, merge. Below a granularity threshold it calls `Arrays.sort`. It uses the ForkJoin common pool and extra working space up to the array (or range) size. Primitive `parallelSort` still Dual-Pivot at the leaves; object `parallelSort` is still stable.

```d2
direction: down
api: "Arrays.sort" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
prim: "int[] / long[] / …" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
obj: "Object[] / T[]" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
dp: "Dual-Pivot Quicksort\n(Java 7+; not spec-stable)" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
ts: "TimSort\n(Java 7+; must be stable)" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
api -> prim
api -> obj
prim -> dp
obj -> ts
```

**Fig. 1.** The overload decides the algorithm. TimSort itself: [[What is Timsort]]. Dual-pivot vs classic quicksort: [[What is quicksort]]. Pre-7 object path: [[What is merge sort]].

```java
import java.util.Arrays;
import java.util.Comparator;

class Demo {
    static void primitiveVersusBoxed() {
        int[] primitives = { 3, 1, 2 };
        Arrays.sort(primitives);              // Dual-Pivot Quicksort

        Integer[] boxed = { 3, 1, 2 };
        Arrays.sort(boxed);                   // TimSort — Integer is an object
        Arrays.sort(boxed, Comparator.reverseOrder());
    }
}
```

**Listing 1.** `int[]` and `Integer[]` take different overloads. `parallelSort` (Java 8) is the parallel entry point; small ranges still land in `Arrays.sort`.

> [!warning] `Integer[]` is not `int[]`
> Autoboxing does not pick the primitive overload. `Arrays.sort(new Integer[] { … })` is TimSort (stable, extra workspace). `Arrays.sort(new int[] { … })` is Dual-Pivot Quicksort (not specified as stable). Equal primitive values may change relative order; equal objects must not.

> [!warning] Algorithm names are notes, stability is the contract
> `Arrays` says implementors may substitute another algorithm as long as the spec holds: `sort(Object[])` **must** be stable, it need not be mergesort/TimSort. Do not write production code that depends on Dual-Pivot internals. `float`/`double` use `Float.compareTo` / `Double.compareTo` total order: `-0.0` before `0.0`, every `NaN` last and equal to every other `NaN`.

> [!tip] Interview answer
> **Primitives: Dual-Pivot Quicksort since Java 7; objects: TimSort, which is a stable adaptive mergesort. Before 7 it was Bentley–McIlroy quicksort vs a modified mergesort. `Integer[]` takes the object path. Those names are implementation notes — the spec only requires object sorts to be stable — and `parallelSort` since 8 is a ForkJoin sort-merge that falls back to `Arrays.sort`.**
