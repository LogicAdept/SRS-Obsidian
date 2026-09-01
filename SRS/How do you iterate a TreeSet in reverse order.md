<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS

# How do you iterate a TreeSet in reverse order?

> [!abstract] Short answer
> **Call `descendingSet()` (a reverse-order *view*) or `descendingIterator()`.** Both walk largest-to-smallest on the existing tree. Java 21 `reversed()` is the same view as `descendingSet()`. Do not copy into a new `TreeSet` just to reverse a walk.

## `NavigableSet` descending APIs

`TreeSet` is a `NavigableSet` (since **1.6** for these methods; the class itself is 1.2). Default `iterator()` is **ascending**. Reverse traversal is:

- `descendingSet()` — a `NavigableSet` view of the same elements, ordering equivalent to `Collections.reverseOrder(comparator())`. Backed by the original: changes show up on both sides. `s.descendingSet().descendingSet()` is essentially `s` again.
- `descendingIterator()` — descending order; **equivalent to** `descendingSet().iterator()`.
- `reversed()` (Java **21**) — specified as equivalent to `descendingSet()`.

Ascending operations and views are **likely faster** than descending ones. You still do not rebuild or re-sort the tree for a reverse walk ([[What NavigableSet operations does TreeSet provide]], [[What is the difference between SortedSet and NavigableSet]]).

```d2
direction: down
tree: "TreeSet / NavigableSet\nascending iterator() = small → large" {
  width: 360
  height: 80
  style.fill: "#e3f2fd"
}
view: "descendingSet() / reversed()\nlive reverse-order view" {
  width: 340
  height: 80
  style.fill: "#fff3e0"
}
it: "descendingIterator()\n== descendingSet().iterator()" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}

tree -> view
tree -> it
```

**Fig. 1.** Reverse iteration is a view or iterator on the same `TreeSet`, not a second sorted copy.

```java
NavigableSet<Integer> s = new TreeSet<>(List.of(1, 2, 3));

for (int n : s.descendingSet()) {
    System.out.print(n + " "); // 3 2 1
}

Iterator<Integer> it = s.descendingIterator();
while (it.hasNext()) {
    it.next(); // 3, then 2, then 1
}
```

**Listing 1.** Enhanced-for uses the view’s iterator. `descendingIterator()` is the same order without keeping the view around.

A constructor `new TreeSet<>(Comparator.reverseOrder())` stores the set itself in reverse. Use that when reverse is the **permanent** order. For an occasional walk of an already-built natural-order set, take the descending view.

If either the set or the descending view is structurally modified while an iteration over either is in progress (except through that iterator’s own `remove`), iteration results are **undefined**. `TreeSet`’s `iterator()` is fail-fast (`ConcurrentModificationException` is best-effort).

> [!warning] `descendingSet()` is a live view, not a copy
> `descendingSet().remove(x)` removes `x` from the original `TreeSet`. Assigning the view to a variable does not snapshot the elements. If you need an independent reverse-ordered set, copy: `new TreeSet<>(s.descendingSet())` still uses the view only as a source.

> [!warning] `HashSet` has no descending view
> Reverse order here is a `NavigableSet` contract (`TreeSet`, `ConcurrentSkipListSet`). `HashSet` has no encounter order and no `descendingSet`. Do not call `Collections.reverse` on the set itself — that method is for lists.

> [!tip] Interview answer
> **Use `TreeSet.descendingSet()` or `descendingIterator()` — reverse order on a live view of the same tree, since Java 6.** `descendingIterator()` is `descendingSet().iterator()`. Java 21 `reversed()` is the same view. Do not rebuild with `Comparator.reverseOrder()` unless reverse should be the set’s stored order.
