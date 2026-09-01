<!--
reps: 0
priority: 0
-->
#Java/Collections/List #Java/Collections/Set #SRS

# What is the difference between List and Set?

> [!abstract] Short answer
> **A `List` is an ordered sequence with indexes; it typically allows `equals`-duplicates.** **A `Set` models a mathematical set: no pair `e1.equals(e2)`, at most one `null`, and no `get(i)`.** A `Set` may have an encounter order (`LinkedHashSet`, `TreeSet`) and still is not a `List`. Both are interfaces since Java 1.2. No class can implement both correctly.

## Uniqueness vs position

`List` extends `SequencedCollection`. You control where each element is inserted and access it by a **zero-based index**: `get` / `set` / `add(index, e)` / `remove(index)`. Lists **typically allow** pairs `e1.equals(e2)` and multiple nulls if they allow null. A list that rejected duplicates would be legal but rare. `indexOf` / `lastIndexOf` and a `ListIterator` (bidirectional, can insert/replace) are List-only. The two search methods “should be used with caution”: in many implementations they are **costly linear scans**. Indexed access itself may be proportional to the index (`LinkedList`). Iteration is usually preferable when you do not know the implementation.

`Set` extends `Collection` only (not `SequencedCollection`). Duplicate means `Objects.equals`, not `==`. Constructors must produce a set with no duplicates. `add(e)` returns `false` and leaves the set unchanged when an equal element is already there. At most one `null`, and only if the implementation permits null at all ([[What is the Set interface in Java]], [[How do HashSet and TreeSet decide whether two elements are duplicates]]). Default `iterator()` has **no particular order** unless the class promises one. The default `Spliterator` reports `DISTINCT`.

`List.equals` is same size, same elements, **same order**, and only vs another `List`. `Set.equals` is same members, **order ignored**, and only vs another `Set`. `Collection` states it is not possible to write a class that correctly implements both.

Optional mutators on either interface may throw `UnsupportedOperationException` (`List.of`, `Set.of`, unmodifiable views). `Set.of("a", "a")` throws `IllegalArgumentException`; `List.of("a", "a")` is a two-element unmodifiable list ([[What does Set.of return and what happens with duplicates]]).

```d2
direction: right
list: "List\nSequencedCollection\nindex + typically duplicates" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
set: "Set\nCollection only\nunique by equals, no get(i)" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
neither: "cannot be both\nList.equals vs Set.equals" {
  width: 260
  height: 90
  style.fill: "#fce4ec"
}

list -> neither
set -> neither
```

**Fig. 1.** Sibling interfaces under `Collection`. Lists equal only lists (same elements, **same order**); sets equal only sets (same members, **order ignored**).

```java
List<String> list = new ArrayList<>();
list.add("a");
list.add("a");           // size 2
list.get(1);             // "a"

Set<String> set = new HashSet<>();
set.add("a");
set.add("a");            // false; size 1
// set.get(0) does not compile
```

**Listing 1.** Second `add` is a duplicate by `equals`. The list keeps both; the set keeps one.

## Order is not the List/Set split

`HashSet` iteration order is unspecified ([[What is a HashSet]]). `LinkedHashSet` is still a `Set`: hash table plus a linked list for **insertion encounter order**; re-`add` of an existing element does not move it ([[How does HashSet differ from LinkedHashSet]]). `TreeSet` is sorted, still unique by its comparator (which must be consistent with `equals` to honor `Set`). None of these have `get(int)`.

Membership cost is an **implementation** story, not “Set is O(1), List is O(n)”. `HashSet.contains` is expected constant time. `TreeSet.contains` is log(n). `CopyOnWriteArraySet.contains` scans. List search is often linear, but that is “many implementations,” not the `List` type’s Big-O.

> [!warning] `LinkedHashSet` is not a `List`
> Insertion order plus uniqueness is still `Set`: no index, `add` of an equal element is a no-op (except Java 21 `addFirst`/`addLast`, which *relocate* an existing member). Do not call `get(i)` or expect `List.equals`. `list.equals(set)` is false even with the same elements.

> [!warning] `equals` never crosses the fence
> A `List` and a `Set` with the same elements are **not** equal. `["a","b"]` is not equal to `["b","a"]`; `{a, b}` equals `{b, a}`. Mutating an element already in a `Set` in a way that changes `equals` is unspecified; a `List` that contains itself makes `equals`/`hashCode` ill-defined.

> [!tip] Interview answer
> **`List` is a sequence: indexes, typically duplicates, `equals` cares about order.** **`Set` is unique-by-`equals`, at most one null, no positional `get`.** Encounter order on `LinkedHashSet` or `TreeSet` does not make them lists. You cannot implement both interfaces in one class.
