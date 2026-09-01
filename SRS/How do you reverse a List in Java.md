<!--
reps: 0
priority: 0
-->
#Java/Collections/List #Java/Collections/Sorting #SRS

# How do you reverse a `List` in Java?

> [!abstract] Short answer
> Call `Collections.reverse(list)`. It **mutates** that list in place, runs in linear time, and needs the `set` operation. It does **not** sort. Since 21, `list.reversed()` is a reverse-ordered **view** that leaves the original encounter order alone. `Collections.reverseOrder()` is a `Comparator` for sorting, not a flip of current positions.

## In-place reverse versus a reverse view

`Collections.reverse` is a static algorithm on the `Collections` utility class (Java 1.2). It rewrites the specified list so the former last element is first, and so on. `[3, 1, 2]` becomes `[2, 1, 3]`. No `Comparable` or `Comparator` is involved.

The documented failure mode is `UnsupportedOperationException` when the list or its list-iterator does not support `set`. Empty and one-element lists are legal: there is nothing to swap.

OpenJDK picks an implementation by size and `RandomAccess`:

- **RandomAccess, or size under 18** (`REVERSE_THRESHOLD`): pairwise `swap` from the ends toward the middle. `swap` is `list.set(i, list.set(j, list.get(i)))`.
- **Larger sequential lists** (typical `LinkedList`): two `ListIterator`s, one from index `0` and one from `size()`, exchanging with `set` as they meet. Indexed `get(i)` on a linked list would be quadratic.

Since 21, `List.reversed()` returns a reverse-ordered `List` **view**. Encounter order on the view is the inverse of the backing list. Order-sensitive operations flip orientation (`getFirst` on the view is `getLast` on the original). If the view allows mutation, writes go through. `reversed()` on that view returns the original list. Changes to the backing list may or may not show in the view, depending on the implementation.

```d2
direction: down
rev: "Collections.reverse(list)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
mut: "same list\npositions flipped" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
view: "list.reversed()  (21)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
live: "List view\noriginal order kept" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
cmp: "sort(reverseOrder())" {
  width: 280
  height: 50
  style.fill: "#f3e5f5"
}
ord: "new total order\nby compare, not positions" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
rev -> mut
view -> live
cmp -> ord
```

**Fig. 1.** `reverse` rewrites positions. `reversed()` is a view. `reverseOrder()` only feeds a sort. Reverse **iteration** without mutating: [[How do you iterate a List in reverse using ListIterator]].

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

class Demo {
    static void reverseIsNotSort() {
        var encounter = new ArrayList<>(List.of(3, 1, 2));
        Collections.reverse(encounter);
        // [2, 1, 3] — former last is first; 1 stays in the middle

        var descending = new ArrayList<>(List.of(3, 1, 2));
        descending.sort(Collections.reverseOrder());
        // [3, 2, 1] — reverse natural order, a different list
    }

    static void viewSince21() {
        var list = new ArrayList<>(List.of(3, 1, 2));
        List<Integer> view = list.reversed();
        // view is [2, 1, 3]; list is still [3, 1, 2]
        view.set(0, 9);
        // list is [3, 1, 9] — write-through to the former last slot
    }

    static void arraysAsListAllowsSet() {
        List<String> list = Arrays.asList("a", "b", "c");
        Collections.reverse(list);
        // [c, b, a] — fixed-size, but set is supported
    }
}
```

**Listing 1.** In-place reverse versus `sort(reverseOrder())`. `reversed()` is Java 21. `Arrays.asList` is a fixed-size array-backed list: size-changing methods throw, `set` does not. Independent reversed copy: wrap in `new ArrayList<>(…)` first — see [[What is the difference between List.of(1,2,3) and new ArrayList]]. `List.copyOf` is unmodifiable, so reverse on that copy throws.

> [!warning] `set` is required; unmodifiable lists throw
> `List.of`, `List.copyOf`, and `Collections.unmodifiableList` reject replace. `Collections.reverse(List.of(1, 2, 3))` throws `UnsupportedOperationException`. `Arrays.asList` looks similar and is fixed-size, but that list is **modifiable**: reverse succeeds and also rewrites the backing array. Copy into an `ArrayList` when you need both literals and a later reverse.

> [!warning] `reverse`, `reversed()`, and `reverseOrder` are three APIs
> `Collections.reverse` flips the current encounter order. `List.reversed()` (21) is a live view — iterating it does not reverse the original. `Collections.reverseOrder()` / `Comparator.reverseOrder()` only invert a **comparison**; use them with `List.sort` or a `TreeMap` constructor [[How do you customize TreeMap key order]]. `sort(reverseOrder())` on `[3, 1, 2]` yields `[3, 2, 1]`, not `[2, 1, 3]`.

> [!tip] Interview answer
> **`Collections.reverse(list)` flips current positions in place — `[3, 1, 2]` becomes `[2, 1, 3]`, not a descending sort — and it needs `set`, so `List.of` throws. Since 21, `list.reversed()` is a reverse view if you must not mutate. `reverseOrder()` is a comparator for `sort` or a sorted map, a different operation.**
