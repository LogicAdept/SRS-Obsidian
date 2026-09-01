<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS

# What is the difference between TreeSet and SortedSet?

> [!abstract] Short answer
> **`SortedSet` is the interface (Java 1.2): a `Set` with a total order, `first`/`last`, and half-open range views.** **`TreeSet` is a class: the `TreeMap`-backed `NavigableSet` (hence `SortedSet`).** You program to the interface; you construct `new TreeSet<>()`. It is not the only `SortedSet`.

## Interface vs the usual implementation

`SortedSet` extends `Set` (and, since 21, `SequencedSet`). It promises a total ordering (natural order or a `Comparator`), an **ascending** iterator, `comparator()`, `first()` / `last()`, and backed views `headSet` / `tailSet` / `subSet` ([[What is the difference between SortedSet and NavigableSet]]). It cannot be instantiated.

`TreeSet` is `public class TreeSet<E> extends AbstractSet<E> implements NavigableSet<E>, Cloneable, Serializable`. Because `NavigableSet` extends `SortedSet`, every `TreeSet` *is a* `SortedSet`. The extra Java 6 surface — `floor` / `ceiling` / `lower` / `higher`, `pollFirst` / `pollLast`, `descendingSet`, inclusive range overloads — lives on `NavigableSet`, not on `SortedSet` ([[What NavigableSet operations does TreeSet provide]]).

The class is a `TreeMap` of keys ([[Which tree data structure backs Java TreeSet]]). `add` / `remove` / `contains` are **guaranteed log(n)**. Not synchronized; wrap with `Collections.synchronizedSortedSet` at creation if needed. Iterators are fail-fast. `addFirst` / `addLast` throw `UnsupportedOperationException` — order comes from the comparator.

```d2
direction: down
iface: "SortedSet\ninterface, since 1.2" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
nav: "NavigableSet\nextends SortedSet, since 1.6" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
cls: "TreeSet\nTreeMap keys, log(n)" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

iface -> nav
nav -> cls
```

**Fig. 1.** `TreeSet` implements the newer interface. A `SortedSet` variable still compiles against a `TreeSet`, but hides navigation methods.

```java
SortedSet<Integer> sorted = new TreeSet<>(List.of(10, 20, 30));
sorted.first();      // 10
sorted.headSet(20);  // 10 — SortedSet view

NavigableSet<Integer> nav = (NavigableSet<Integer>) sorted;
nav.floor(25);       // 20 — not on SortedSet
```

**Listing 1.** Construction is `TreeSet`. The static type decides which methods you see. Prefer declaring `NavigableSet` when you need `floor` / `descendingSet`.

JDK `SortedSet` implementations named on the interface: `TreeSet` and `ConcurrentSkipListSet` ([[What is ConcurrentSkipListSet]]). `TreeSet` is the non-concurrent general-purpose choice ([[When should you choose HashSet LinkedHashSet or TreeSet]]). `SortedSet` also recommends four constructor shapes (empty / `Comparator` / `Collection` / `SortedSet`); `TreeSet` provides them.

> [!warning] `SortedSet` is not “the TreeSet interface”
> Typing `SortedSet` is like typing `List` instead of `ArrayList`: you lose `NavigableSet` methods, and the runtime object might be a `ConcurrentSkipListSet`. `new SortedSet<>()` does not compile.

> [!warning] Comparator equality is not `Set.equals`
> A `TreeSet` (any `SortedSet`) treats `compare == 0` as the same element. If that ordering is not consistent with `equals`, the `Set` contract is broken even though the tree still behaves. That is an interface rule, not a `TreeSet` quirk.

> [!tip] Interview answer
> **`SortedSet` is the ordered-set interface; `TreeSet` is the `TreeMap`-backed class that implements `NavigableSet` (and therefore `SortedSet`).** Say `new TreeSet<>()` and usually declare `NavigableSet` so you get `floor` and `descendingSet`. The other JDK sorted set is `ConcurrentSkipListSet`.
