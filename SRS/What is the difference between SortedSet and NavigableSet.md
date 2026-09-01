<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS

# What is the difference between SortedSet and NavigableSet?

> [!abstract] Short answer
> **`SortedSet` (1.2) is a totally ordered `Set`: ascending iterator, `comparator()`, `first()` / `last()`, and half-open `headSet` / `tailSet` / `subSet` views.** **`NavigableSet` (1.6) extends `SortedSet` with closest-match lookups, poll, inclusive bounds, and a reverse-order view.** `TreeSet` and `ConcurrentSkipListSet` implement `NavigableSet`, so they implement both.

## What `SortedSet` already is

A `SortedSet` is a `Set` with a total order — natural ordering or a `Comparator` supplied at creation. The iterator walks **ascending**. All elements must be mutually comparable. Ordering must be **consistent with equals** for the `Set` contract to hold; if it is not, behavior is still defined but the `Set` contract is broken.

Range views are **half-open**: `subSet(from, to)` is `[from, to)`, `headSet(to)` is `< to`, `tailSet(from)` is `≥ from`. They are backed by the original set ([[What do TreeSet headSet tailSet and subSet return]]). Java 21 adds `SequencedSet` defaults: `getFirst`/`getLast` delegate to `first`/`last`; `addFirst`/`addLast` throw `UnsupportedOperationException`; `reversed()` returns a reverse-ordered `SortedSet` view.

## What `NavigableSet` adds

`NavigableSet` extends `SortedSet`. Extra operations:

- Neighbours: `lower` (strict `<`), `floor` (`≤`), `ceiling` (`≥`), `higher` (strict `>`), or `null` if none.
- `pollFirst` / `pollLast` — return and **remove** the lowest / highest, or `null` if empty.
- `descendingSet()` — reverse-order **view** (backed, mutations write through). `descendingIterator()` ≡ `descendingSet().iterator()`.
- Inclusive/exclusive overloads: `subSet(from, fromInc, to, toInc)`, `headSet(to, inclusive)`, `tailSet(from, inclusive)`, returning `NavigableSet`.

The short `SortedSet` range methods stay typed as `SortedSet` so old implementations could be retrofitted. `NavigableSet` encourages implementations to override them to return `NavigableSet`. `TreeSet` still declares the two-arg forms as `SortedSet`. Java 21 `NavigableSet.reversed()` is specified as **equivalent to** `descendingSet()` ([[How do you iterate a TreeSet in reverse order]]).

Ascending operations and views are **likely faster** than descending ones.

```d2
direction: down
ss: "SortedSet (1.2)\norder, first/last, half-open views" {
  width: 360
  height: 80
  style.fill: "#e3f2fd"
}
ns: "NavigableSet (1.6)\nfloor/ceiling/lower/higher\npoll, descendingSet, inclusive bounds" {
  width: 380
  height: 100
  style.fill: "#fff3e0"
}
impl: "TreeSet · ConcurrentSkipListSet" {
  width: 320
  height: 60
  style.fill: "#e8f5e9"
}

ss -> ns
ns -> impl
```

**Fig. 1.** `NavigableSet` is `SortedSet` plus navigation. There is no JDK `SortedSet` that is not a `NavigableSet` today.

```java
NavigableSet<Integer> s = new TreeSet<>(List.of(10, 20, 30, 40));
s.first();         // 10   SortedSet
s.last();          // 40
s.floor(25);       // 20   ≤ 25
s.ceiling(25);     // 30   ≥ 25
s.descendingSet(); // reverse-order view: 40, 30, 20, 10
s.pollFirst();     // 10, and it is removed
```

**Listing 1.** Typed as `NavigableSet` so `floor` / `ceiling` / `pollFirst` compile. A `SortedSet` variable would not see those methods.

JDK implementations: `TreeSet` (not concurrent) and `ConcurrentSkipListSet` ([[What is ConcurrentSkipListSet]], [[What NavigableSet operations does TreeSet provide]]).

> [!warning] A `SortedSet` reference hides navigation
> `SortedSet<Integer> s = new TreeSet<>();` has `first` and `subSet(from, to)`, not `floor` or `descendingSet`. Declare `NavigableSet` (or `TreeSet`) when you need the Java 6 API. `s.subSet(a, b)` is still a `SortedSet` even on a `TreeSet` — use the four-arg overload to keep a `NavigableSet`.

> [!warning] `pollFirst` mutates; `first` does not
> `first()` / `last()` throw `NoSuchElementException` on an empty set. `pollFirst()` / `pollLast()` return `null` and, when the set is non-empty, **remove** the element. `descendingSet()` is a live view, not a reversed copy.

> [!tip] Interview answer
> **`SortedSet` is the ordered-set interface from Java 1.2: comparator, endpoints, half-open range views.** **`NavigableSet` (Java 6) extends it with `floor`/`ceiling`/`lower`/`higher`, poll, inclusive bounds, and `descendingSet`.** `TreeSet` implements `NavigableSet`. Type the variable as `NavigableSet` if you want those methods.
