<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS

# What NavigableSet operations does TreeSet provide?

> [!abstract] Short answer
> **All of them: `TreeSet` implements `NavigableSet` (Java 6).** Closest-match lookups are `floor` / `ceiling` / `lower` / `higher` (or `null` if none). You also get `pollFirst` / `pollLast`, `descendingSet` / `descendingIterator`, and inclusive `headSet` / `tailSet` / `subSet` overloads. `HashSet` has none of this.

## Neighbour lookups

`NavigableSet` reports closest matches for a search target ([[What is the difference between SortedSet and NavigableSet]]):

| Method | Meaning |
| --- | --- |
| `floor(e)` | greatest element **≤** `e` |
| `ceiling(e)` | least element **≥** `e` |
| `lower(e)` | greatest element **strictly <** `e` |
| `higher(e)` | least element **strictly >** `e` |

If no such element exists, these four return **`null`** — they do not throw `NoSuchElementException`. `ClassCastException` if `e` cannot be compared; `NullPointerException` if `e` is null and the set uses natural ordering (or a comparator that rejects null).

```java
NavigableSet<Integer> s = new TreeSet<>(List.of(10, 20, 30));
s.floor(20);    // 20
s.lower(20);    // 10
s.ceiling(20);  // 20
s.higher(20);   // 30
s.floor(5);     // null — nothing ≤ 5
```

**Listing 1.** `floor` / `ceiling` may return the argument when it is a member. `lower` / `higher` skip it. `first()` on this set is `10` and **throws** on an empty set; `floor` does not.

`TreeSet` documents **guaranteed log(n)** for `add`, `remove`, and `contains`. These lookups sit on the same `TreeMap`; they are not a linear `List` scan.

## The rest of `NavigableSet` on `TreeSet`

- **Poll:** `pollFirst()` / `pollLast()` return and **remove** the lowest / highest, or `null` if empty.
- **Reverse:** `descendingSet()` is a live reverse-order view; `descendingIterator()` ≡ `descendingSet().iterator()` ([[How do you iterate a TreeSet in reverse order]]). Java 21 `reversed()` is the same view.
- **Ranges:** `headSet` / `tailSet` / `subSet` with inclusive flags, returning `NavigableSet`. The older two-arg / one-arg forms stay `SortedSet` and half-open ([[What do TreeSet headSet tailSet and subSet return]]).
- **Ascending `iterator()`** is the default walk. Ascending views are likely faster than descending.

```d2
direction: down
nav: "NavigableSet on TreeSet" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
nbr: "floor ceiling lower higher\nnull if absent" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
more: "pollFirst/Last · descendingSet\ninclusive subSet/headSet/tailSet" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}

nav -> nbr
nav -> more
```

**Fig. 1.** Navigation is the Java 6 surface. `SortedSet` already had `first` / `last` / half-open views.

> [!warning] `floor`/`pollFirst`/`first` are three different empty behaviors
> Neighbour methods return `null` when there is no match. `pollFirst` returns `null` on an empty set **and removes** when it is not empty. `first()` / `last()` throw `NoSuchElementException` if the set is empty. Callers must null-check `floor` — there is no exception to catch.

> [!warning] `HashSet` has no navigation API
> `floor` / `descendingSet` / `subSet` exist only on `NavigableSet` (`TreeSet`, `ConcurrentSkipListSet`). A `HashSet` variable will not compile them. Inclusive-both-ends range is the four-arg `subSet`, not `floor`+`ceiling` glued together.

> [!tip] Interview answer
> **`TreeSet` is a `NavigableSet`: `floor`/`ceiling` are inclusive neighbours, `lower`/`higher` are strict, and all four return `null` if missing.** You also get poll, a reverse view, and inclusive range views. `first()` throws on empty; `HashSet` has none of these methods.
