<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Set/TreeSet #SRS

# What is the difference between `TreeSet` and `HashSet`?

> [!abstract] Short answer
> **`HashSet` hashes; `TreeSet` sorts.** `HashSet` is a `HashMap` of keys (unordered, expected O(1), one `null`). `TreeSet` is a `TreeMap` of keys — a red-black `NavigableSet` (sorted, guaranteed `log(n)`, `null` rejected under natural order). Duplicates follow `equals`/`hashCode` vs `compare` / `compareTo`.

## Same interface, different engine

Both implement `Set`. Both are unsynchronized, fail-fast, and treat elements as map **keys** with a dummy value. The maps differ ([[What internal structures back HashSet and TreeSet]]).

```d2
direction: down
q: "Set of unique elements" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
hash: "HashSet = HashMap\nno order, expected O(1)" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
tree: "TreeSet = TreeMap\nsorted red-black, log(n)" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}

q -> hash
q -> tree
```

**Fig. 1.** Choosing the class chooses the duplicate test and the walk order ([[How is HashSet implemented in terms of HashMap]], [[Is TreeSet implemented using TreeMap]], [[Which tree data structure backs Java TreeSet]]).

```java
Set<String> hash = new HashSet<>(List.of("b", "a", "b"));
Set<String> tree = new TreeSet<>(List.of("b", "a", "b"));
hash.size(); // 2
tree.size(); // 2
// hash iterates in unspecified order
// tree iterates a, b
```

**Listing 1.** Duplicate `"b"` is dropped on both. Only `TreeSet` promises `a` then `b`.

## What actually differs

| | `HashSet` | `TreeSet` |
| --- | --- | --- |
| Since | 1.2 | 1.2 |
| Backing | `HashMap` (hash table, bins) | `TreeMap` (red-black tree) |
| `add` / `contains` / `remove` | expected constant time | guaranteed `log(n)` |
| Iteration | unspecified; ~ size + capacity | sorted in-order |
| Sameness | `hashCode` then `equals` | `compare` == 0 |
| `null` | one element allowed | NPE if natural order (or comparator forbids null) |
| Extra | — | `NavigableSet` ranges / floor / ceiling |
| Java 21 sequenced | not a `SequencedSet` | `addFirst` / `addLast` throw UOE |

Ordering on `TreeSet` must be **consistent with equals** or the `Set` contract breaks: two `equals` objects can be two nodes, or `compare == 0` can collapse objects that are not `equals` ([[How do HashSet and TreeSet decide whether two elements are duplicates]]).

`HashSet` “permits the `null` element.” `TreeSet.add` throws `NullPointerException` “if the specified element is null and this set uses natural ordering, or its comparator does not permit null elements” ([[Does HashSet allow a null element]], [[Can a TreeSet contain null]]).

Need **insertion** order, not sort? `LinkedHashSet`, not `TreeSet` ([[When should you choose HashSet LinkedHashSet or TreeSet]]). Elements in a `TreeSet` must be mutually comparable (`ClassCastException` otherwise). Neither class is synchronized: wrap `HashSet` with `Collections.synchronizedSet` and `TreeSet` with `Collections.synchronizedSortedSet`.

> [!warning] “HashSet stores the element as key and value” is wrong
> The map value is the dummy `PRESENT`. Membership is “the key is there.” Saying both sides are the element confuses `HashSet` with a map you filled yourself.

> [!warning] Sorted is not “HashSet after Collections.sort”
> You cannot sort a `HashSet` in place. `new TreeSet<>(hashSet)` copies into a tree and requires comparability. The hash table is gone.

> [!warning] `O(1)` is conditional; `O(log n)` is not
> `HashSet`’s constant time assumes a dispersing `hashCode`. `TreeSet` documents guaranteed `log(n)` for the basics regardless of hash quality — it never hashes.

> [!tip] Interview answer
> **`HashSet` is unordered hashing (`HashMap`, expected O(1), one null). `TreeSet` is a sorted red-black tree (`TreeMap`, log n, `NavigableSet`).** Pick `HashSet` for membership, `TreeSet` for order and ranges, and `LinkedHashSet` if you meant first-seen order rather than sort.
