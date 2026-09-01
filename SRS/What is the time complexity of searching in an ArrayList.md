<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# What is the time complexity of searching in an `ArrayList`?

> [!abstract] Short answer
> **O(n)** for `contains`, `indexOf`, and `lastIndexOf`: a linear `Objects.equals` scan. `get(i)` is O(1) and is not a search. `Collections.binarySearch` is O(log n) comparisons only on an already **sorted** `ArrayList`; on an unsorted list the result is undefined.

## Linear `equals`, not a hash table

```d2
direction: down
q: "search ArrayList" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
lin: "contains / indexOf\nO(n) equals" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
log: "binarySearch\nsorted + RandomAccess\nO(log n)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

q -> lin
q -> log
```

**Fig. 1.** Default search is a scan. Binary search is a different, sorted contract ([[How do you search for an element in an ArrayList]]).

The class specification: `get`/`set` are constant time; end `add` is amortized constant; **“all of the other operations run in linear time (roughly speaking).”** Membership and index-of live in that linear family. OpenJDK `contains` is `indexOf(o) >= 0` and walks `0 .. size` (`==` for `null`, else `o.equals`). `hashCode` is not used.

`Collections.binarySearch(list, key)` on a random-access list (`ArrayList` implements `RandomAccess`) is O(log n) comparisons. The list **must** be sorted in ascending order; otherwise the result is **undefined** (you can miss a present element). Sorting first is O(n log n), not part of `contains`.

```java
List<String> names = new ArrayList<>();
names.add("Ada");
names.add("Grace");

names.contains("Grace"); // O(n) scan
names.indexOf("Ada");    // O(n), returns 0

Collections.sort(names);
Collections.binarySearch(names, "Grace"); // O(log n) if still sorted
```

**Listing 1.** Conceptual. Worst-case `contains` even when the element exists: [[What is the worst case time complexity of contains on an ArrayList when the element exists]]. Many independent lookups: a `HashSet` is a different structure ([[How do you convert an ArrayList to a HashSet in one line]]).

> [!warning] `get(i)` is not “search in O(1)”
> You already know the index. Finding *whether* a value is present still walks the list.

> [!warning] Do not binary-search an unsorted `ArrayList`
> That is not a faster `contains`. Sort (or keep the list ordered) first; duplicates: which index `binarySearch` returns is unspecified.

> [!tip] Interview answer
> **Searching an `ArrayList` is O(n): `contains`/`indexOf` compare with `equals` from one end.** It is not a hash lookup. `binarySearch` is O(log n) only after the list is sorted; otherwise use a `Set` if you need expected-constant membership.
