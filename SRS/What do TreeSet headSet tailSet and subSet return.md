<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: they return **range views** of a sorted set — **not copies**. `headSet(to)` is everything below `to`, `tailSet(from)` is everything from `from` up, `subSet(from, to)` is the half-open range `[from, to)`. NavigableSet overloads toggle inclusive/exclusive bounds.

```java
NavigableSet<Integer> s = new TreeSet<>(List.of(10, 20, 30, 40));
s.headSet(30);                 // [10, 20]      (exclusive end)
s.tailSet(20);                 // [20, 30, 40]  (inclusive start)
s.subSet(20, 40);              // [20, 30]      (half-open)
s.subSet(20, true, 40, true);  // [20, 30, 40]
```

Dump: **backed by the original set** — changes flow both ways. Adding an element **outside** the view’s bounds throws **`IllegalArgumentException`**. Wrap in `new TreeSet<>(view)` for an independent snapshot.

> [!warning] Unverified traps from the dump
> - These are live views, not snapshots.
> - Default `subSet` is half-open; inclusive both ends needs the four-arg overload.
