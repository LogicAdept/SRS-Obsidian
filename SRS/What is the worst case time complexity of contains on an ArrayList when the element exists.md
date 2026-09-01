<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# What is the worst-case time of `contains` on an `ArrayList` when the element exists?

> [!abstract] Short answer
> **O(n).** `contains` is a linear `Objects.equals` scan. If the match is the **last** live slot, you still compare every element. Existence does not make `contains` O(1). `get(i)` is O(1) only when you already have the index.

## Found last still means a full scan

```d2
direction: right
scan: "contains(x)\nwalk 0 .. size-1" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
hit: "equals at last index\nstill n comparisons" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}

scan -> hit
```

**Fig. 1.** A hit at the end is the worst case among “present” inputs ([[What is the time complexity of searching in an ArrayList]], [[How do you search for an element in an ArrayList]]).

The class specification puts `contains` with “all of the other operations” that run in **linear** time (`get`/`set` are the constant-time indexed ops). OpenJDK implements `contains(o)` as `indexOf(o) >= 0` and walks `elementData` from `0` to `size` (`==` for `null`, else `o.equals`). There is no hash probe and no early exit except the first match.

So:

- Present at index `0` → one comparison (best case among hits).
- Present at index `size - 1` → **n** comparisons (worst case among hits).
- Absent → **n** comparisons (same as “exists last”).

Duplicates: `contains` stops at the **first** `equals` hit, so the worst *present* case is “only the last element matches.”

```java
List<Integer> list = new ArrayList<>();
list.add(1);
list.add(2);
list.add(3);
list.contains(3); // true, but three equals checks from the front
```

**Listing 1.** Conceptual. `indexOf` has the same worst-case scan when the first hit is last. `Collections.binarySearch` is O(log n) only on a **sorted** list and is not `contains`.

> [!warning] “It exists, so O(1)” confuses `get` with `contains`
> `ArrayList` random access is by **index**. Finding a **value** still walks. A `HashSet` is a different type ([[How do you convert an ArrayList to a HashSet in one line]]).

> [!warning] `equals` cost is extra
> The O(n) bound counts list slots visited. If `equals` itself is linear in the payload, the wall-clock cost is larger; the list still does not hash.

> [!tip] Interview answer
> **Still O(n) when the element is present:** `contains` scans from the front with `equals` and only stops at the first hit. Worst case among hits is the last index. Existence does not give you `get`-style O(1).
