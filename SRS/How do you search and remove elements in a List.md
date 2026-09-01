<!--
reps: 0
priority: 0
-->
#Java/Collections/List #SRS

# How do you search and remove elements in a List?

> [!abstract] Short answer
> **Search with `contains` (present?) or `indexOf` / `lastIndexOf` (where?) — all `Objects.equals`.** **Remove the first match with `remove(Object)`, a slot with `remove(int)`, a predicate with `removeIf`, a range with `subList(from, to).clear()`, or the current cursor with `Iterator.remove()` after `next()`.** Those search methods are linear in many implementations. `Collections.binarySearch` is log(n) only on a **sorted** `RandomAccess` list.

## Find, then delete — two different contracts

`List` documents two search methods. Use them with caution: in many implementations they are costly linear scans (`LinkedList` also makes each `get(i)` a link walk). `contains(o)` is membership: some `e` with `Objects.equals(o, e)`. `indexOf` / `lastIndexOf` return the lowest / highest such index, or `-1`.

Removal is optional. `remove(Object o)` deletes the **first** occurrence (lowest `i` with `Objects.equals(o, get(i))`) and returns whether the list changed. `remove(int index)` deletes that slot, shifts later elements left, and returns the old element. `removeAll(c)` drops every element also in `c`; `retainAll(c)` keeps only those. Java 8 `removeIf(predicate)` removes every match; the default walks `iterator()` and calls `Iterator.remove()` (first match throws `UnsupportedOperationException` if that iterator cannot remove). Java 21 `removeFirst` / `removeLast` are the two ends.

Range delete is a view, not a special `removeRange` on the interface: `list.subList(from, to).clear()` [[What is an efficient way to remove a contiguous block from the middle of an ArrayList]]. Structural edits must go through that subList, or the view’s semantics become undefined.

During a walk, use the **iterator’s** `remove()` once per `next()`, not `list.remove(...)` inside enhanced `for` [[How do you remove an element from a collection while iterating]]. `ListIterator.remove()` is the same idea after `next` or `previous`.

`Collections.binarySearch(list, key)` (or with a `Comparator`) requires the list already sorted the same way. Unsorted → undefined. `RandomAccess` lists: log(n) positional probes. A large sequential list: O(n) link traversals plus O(log n) comparisons. Duplicate keys: no guarantee which index is returned.

```d2
direction: right
find: "contains / indexOf\nlastIndexOf" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
byval: "remove(Object)\nfirst equals" {
  width: 180
  height: 80
  style.fill: "#fff3e0"
}
byidx: "remove(int)\nshift left" {
  width: 160
  height: 80
  style.fill: "#fff3e0"
}
bulk: "removeIf / removeAll\nsubList.clear" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}

find -> byval
find -> byidx
find -> bulk
```

**Fig. 1.** Search answers “is it here / at which index.” Delete is a separate optional mutator: by value, by index, by predicate, or by range view.

```java
class ListSearchRemove {
    static void demo(java.util.List<String> list) {
        boolean present = list.contains("b");
        int i = list.indexOf("b");          // -1 if absent
        if (i >= 0) {
            list.remove(i);                 // remove(int)
        }
        list.remove("c");                   // remove(Object) — first equals
        list.removeIf(s -> s.startsWith("x"));
        list.subList(0, Math.min(2, list.size())).clear();
    }
}
```

**Listing 1.** `indexOf` then `remove(int)` is “that slot.” `remove("c")` is “first equal to `c`.” `removeIf` is every match in one pass.

```java
java.util.List<Integer> nums = new java.util.ArrayList<>(java.util.List.of(10, 20, 30));
nums.remove(1);                    // removes 20 — index 1, not value 1
nums.remove(Integer.valueOf(10));  // removes the Integer 10
```

**Listing 2.** Both `remove` overloads exist. `remove(1)` on `List<Integer>` is `remove(int)`. Use `Integer.valueOf` (or `remove((Integer) 10)`) for the value. `List.of(...)` itself rejects `remove` with `UnsupportedOperationException` — copy to an `ArrayList` first [[How do you search for an element in an ArrayList]] [[How does removing elements from an ArrayList work and how does size change]].

> [!warning] `remove(int)` is not “remove the number”
> Overload resolution picks the index method whenever the argument is `int`. That is a structural change and, inside a fail-fast for-each, usually `ConcurrentModificationException` [[What is ConcurrentModificationException]]. `indexOf` returning `-1` passed to `remove(int)` is `IndexOutOfBoundsException`.

> [!warning] `binarySearch` is not `indexOf`
> The list must already be sorted. `indexOf` is a linear `equals` scan and does not require order. `binarySearch` on an unsorted list is undefined, not “slow but correct.”

> [!tip] Interview answer
> **`contains` / `indexOf` search by `equals`; `remove(Object)` deletes the first match, `remove(int)` deletes a slot.** `removeIf` or the iterator’s `remove` after `next()` for many elements or a live walk. Range: `subList(from, to).clear()`. On `List<Integer>`, `remove(1)` is an index. Do not use `binarySearch` unless the list is sorted.
