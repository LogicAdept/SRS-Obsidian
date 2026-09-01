<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS

# What do TreeSet `headSet`, `tailSet`, and `subSet` return?

> [!abstract] Short answer
> **Live range *views* of the same `TreeSet`, not copies.** One-arg / two-arg forms are the original `SortedSet` bounds: `headSet(to)` is strictly below `to`, `tailSet(from)` is `from` and above, `subSet(from, to)` is the half-open interval `[from, to)`. Java 6 `NavigableSet` overloads add inclusive/exclusive flags and return `NavigableSet`.

## Bounds, not snapshots

All six methods return a set **backed by** this set: changes in the view show in the original and vice versa. The view supports the same optional set operations. Endpoints are **comparison bounds**; they need not be members.

| Call | Elements kept | Declared return |
| --- | --- | --- |
| `headSet(to)` | `< to` (exclusive high) | `SortedSet` |
| `headSet(to, inclusive)` | `< to`, or `≤ to` if inclusive | `NavigableSet` |
| `tailSet(from)` | `≥ from` (inclusive low) | `SortedSet` |
| `tailSet(from, inclusive)` | `≥ from`, or `> from` if not inclusive | `NavigableSet` |
| `subSet(from, to)` | `[from, to)` | `SortedSet` |
| `subSet(from, fromInc, to, toInc)` | flags choose each end | `NavigableSet` |

The short forms are defined as the long ones: `headSet(to)` ≡ `headSet(to, false)`, `tailSet(from)` ≡ `tailSet(from, true)`, `subSet(from, to)` ≡ `subSet(from, true, to, false)`. Inclusive both ends is the four-arg call, not the two-arg `subSet`. If `from` and `to` compare equal, two-arg `subSet` is **empty**; four-arg is empty unless **both** ends are inclusive ([[What is the difference between SortedSet and NavigableSet]], [[What NavigableSet operations does TreeSet provide]]).

The one-arg / two-arg methods stay typed as `SortedSet` so older `SortedSet` implementations could be retrofitted. On a `TreeSet` that means `s.subSet(a, b).descendingSet()` does not compile without a cast — use the four-arg / boolean overloads when you still need navigable methods.

```d2
direction: right
orig: "TreeSet\n10 20 30 40" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
head: "headSet(30)\n10 20" {
  width: 160
  height: 80
  style.fill: "#fff3e0"
}
tail: "tailSet(20)\n20 30 40" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}
sub: "subSet(20, 40)\n20 30" {
  width: 180
  height: 80
  style.fill: "#fce4ec"
}

orig -> head
orig -> tail
orig -> sub
```

**Fig. 1.** Three views of one tree. Inserts and removes through a view write through; inserts outside the view’s range fail.

```java
NavigableSet<Integer> s = new TreeSet<>(List.of(10, 20, 30, 40));

s.headSet(30);                // 10, 20
s.tailSet(20);                // 20, 30, 40
s.subSet(20, 40);             // 20, 30
s.subSet(20, true, 40, true); // 20, 30, 40

s.headSet(30).add(15);        // original now contains 15
s.headSet(30).add(30);        // IllegalArgumentException — 30 is not < 30
```

**Listing 1.** Half-open `subSet(from, to)` excludes `to`. Closed range needs `subSet(from, true, to, true)`. `add(15)` on the head view mutates `s`.

`from > to` on `subSet` throws `IllegalArgumentException`. A view is itself a restricted-range set: asking it for a bound **outside its range** also throws. For an independent copy with the same ordering, `new TreeSet<>(view)` hits the `TreeSet(SortedSet)` constructor (not a `Collection` copy that would drop the comparator).

> [!warning] Views are not snapshots
> Clearing or adding through `headSet` / `tailSet` / `subSet` mutates the backing `TreeSet`. `remove` of an in-range element is allowed and removes it from the original. `add` of an out-of-range element throws `IllegalArgumentException` — it does not silently go into the backing set.

> [!warning] Default `subSet` is half-open
> `subSet(20, 40)` is `[20, 40)`, so `40` is absent even if it is in the tree. Inclusive-inclusive needs the Java 6 four-argument overload. The endpoint `40` does not have to be present for that exclusive high bound to apply.

> [!tip] Interview answer
> **They return backed range views, not copies: `headSet(to)` is `< to`, `tailSet(from)` is `≥ from`, `subSet(from, to)` is `[from, to)`.** Navigable overloads (Java 6) take inclusive flags and return `NavigableSet`; the short forms return `SortedSet`. Out-of-range `add` throws `IllegalArgumentException`; copy with `new TreeSet<>(view)` if you need a snapshot.
