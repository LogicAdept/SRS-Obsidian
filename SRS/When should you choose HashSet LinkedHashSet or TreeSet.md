<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Set/LinkedHashSet #Java/Collections/Set/TreeSet #SRS

# When should you choose `HashSet`, `LinkedHashSet`, or `TreeSet`?

> [!abstract] Short answer
> **`HashSet` when you only need membership** (no encounter order). **`LinkedHashSet` when uniqueness must keep insertion (encounter) order.** **`TreeSet` when you need a sorted `NavigableSet`** — ranges, first/last, successor — and you accept `log(n)` and a comparison order.

## Decide on order, then on cost

All three are unsynchronized `Set` implementations. They differ in **how they decide duplicates** and **what iteration means**.

```d2
direction: down
need: "Need a Set?" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
sorted: "Sorted / range queries?" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
ts: "TreeSet\nNavigableSet, log(n)" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
ins: "Stable encounter order?" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
lhs: "LinkedHashSet\nhash + linked list" {
  width: 260
  height: 70
  style.fill: "#ffe0b2"
}
hs: "HashSet\nhash table, chaotic order" {
  width: 280
  height: 70
  style.fill: "#ffcdd2"
}

need -> sorted
sorted -> ts: "yes"
sorted -> ins: "no"
ins -> lhs: "yes"
ins -> hs: "no"
```

**Fig. 1.** Order requirement first. “Fastest set” is not a fourth axis until you know whether iteration walks **size** or **capacity**.

```java
Set<String> hs = new HashSet<>(List.of("b", "a", "c"));
Set<String> lhs = new LinkedHashSet<>(List.of("b", "a", "c"));
Set<String> ts = new TreeSet<>(List.of("b", "a", "c"));
// hs  — unspecified order
// lhs — b, a, c  (insertion / encounter order)
// ts  — a, b, c  (natural order)
```

**Listing 1.** Same elements, three contracts. `List.of` here is only a source; each set constructor copies.

### `HashSet` — default membership

Choose it when order does not matter and you want hash-table `add` / `contains` / `remove` in expected constant time (good `hashCode`). Iteration is **size plus backing capacity**, so an oversized table is expensive to walk. No insertion-order guarantee; the order can change over time. Permits one `null` ([[Does HashSet allow a null element]]). Duplicates are `hashCode` then `equals` ([[How do HashSet and TreeSet decide whether two elements are duplicates]]).

### `LinkedHashSet` — unique, but in the order you added them

It is a `HashSet` plus a doubly-linked list that defines **encounter order**: eldest (least recently inserted) first, youngest last. Re-`add` of an already present element **does not** move it. Java 21 `addFirst` / `addLast` **do** relocate. Permits `null`. Basic ops stay expected constant time, a little slower than `HashSet` because of the list; **iteration is proportional to size only**, independent of capacity — cheaper than iterating a sparse `HashSet`. Use it to copy a set and keep presentation order: `new LinkedHashSet<>(other)` ([[How does HashSet differ from LinkedHashSet]]).

### `TreeSet` — sorted, with ranges

A `NavigableSet` on a `TreeMap`. `add` / `contains` / `remove` are **guaranteed `log(n)`**. Order is natural order or a constructor `Comparator`, not insertion. You get `headSet` / `tailSet` / `subSet` and the navigable methods ([[What NavigableSet operations does TreeSet provide]]). Comparison **must be consistent with equals** or you break the `Set` contract. `addFirst` / `addLast` throw `UnsupportedOperationException` — you cannot restamp encounter order. Default (natural order) **rejects `null`** ([[Can a TreeSet contain null]]). Elements must be mutually comparable ([[What is the difference between TreeSet and HashSet]]).

| Need | Pick |
| --- | --- |
| Membership only | `HashSet` |
| Unique + insertion encounter order | `LinkedHashSet` |
| Sorted iteration, ranges, successor | `TreeSet` |
| All values are one enum type | `EnumSet` — not one of these three |

> [!warning] `HashSet` is not always the fastest walk
> LinkedHashSet’s own javadoc: iteration over `HashSet` is likely **more expensive** (size **plus capacity**) than over `LinkedHashSet` (size only). “HashSet is fastest” applies to `add` / `contains` / `remove`, not to dumping the set.

> [!warning] `TreeSet` is not “HashSet with sort”
> Uniqueness is `compare == 0`, not `equals`. Two objects that `equals` would split can be one tree node, or the reverse if ordering disagrees with `equals`. You also pay `log(n)` and a `Comparable`/`Comparator` on every insert.

> [!warning] Enum universe → `EnumSet`, not these three
> If every element is a constant of one enum, `EnumSet` is a bit vector: compact, constant-time, declaration-order iteration, no `null`. That is the fourth choice interview dumps forget to name ([[Why does Java provide EnumSet in addition to HashSet and TreeSet]]).

> [!tip] Interview answer
> **`HashSet` for unordered membership, `LinkedHashSet` to keep insertion order, `TreeSet` when you need a sorted navigable set.** Hash vs tree also changes the duplicate test (`equals`/`hashCode` vs `compare`). For a single enum type, say `EnumSet` instead.
