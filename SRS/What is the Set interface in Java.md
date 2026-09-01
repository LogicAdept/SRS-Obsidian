<!--
reps: 0
priority: 0
-->
#Java/Collections/Set #SRS

# What is the Set interface in Java?

> [!abstract] Short answer
> **`java.util.Set` (Java 1.2) is a `Collection` that models a mathematical set: no pair `e1.equals(e2)`, and at most one null.** It adds uniqueness rules on constructors, `add`, `equals`, and `hashCode`. There is no index `get`. Iteration order is unspecified unless the implementation promises one.

## Contract on top of `Collection`

`Set` extends `Collection` only. Extra stipulations:

- **Constructors** must produce a duplicate-free set.
- **`add(e)`** inserts `e` if no member `e2` satisfies `Objects.equals(e, e2)`; otherwise it leaves the set unchanged and returns `false`.
- **`equals`** is true when the other object is also a `Set`, same size, same members — **order ignored**. That is why a class cannot implement both `List` and `Set` correctly (`Collection` JavaDoc).
- **`hashCode`** is the sum of element hash codes (`null` counts as 0).

`contains` / `remove` use `Objects.equals`. When the other argument is also a `Set`, `addAll` is union, `retainAll` is intersection, `removeAll` is asymmetric difference — they **mutate the receiver** ([[How do you compute union intersection and difference of two Sets]]). Mutators are **optional** and may throw `UnsupportedOperationException`.

The iterator returns elements in **no particular order** unless the class documents one (`LinkedHashSet` encounter order, `TreeSet` sorted order). The default `spliterator` reports `DISTINCT` (Java 8).

```d2
direction: down
coll: "Collection" {
  width: 160
  height: 45
  style.fill: "#eceff1"
}
set: "Set" {
  width: 140
  height: 45
  style.fill: "#e3f2fd"
}
sorted: "SortedSet" {
  width: 140
  height: 45
  style.fill: "#fff3e0"
}
nav: "NavigableSet" {
  width: 160
  height: 45
  style.fill: "#fce4ec"
}

coll -> set
set -> sorted
sorted -> nav
```

**Fig. 1.** `Set` in the hierarchy. `SortedSet` / `NavigableSet` add ordering, not indexes ([[What is the difference between SortedSet and NavigableSet]]). Contrast: [[What is the difference between List and Set]].

```java
Set<String> s = new HashSet<>();
s.add("a");
s.add("a");              // false; size stays 1
s.contains("a");         // true
```

**Listing 1.** Membership is by `equals`, not by insert count. Default `HashSet` ([[What is a HashSet]]). Catalog: [[What are the main Java Set implementations]].

`Set.of` / `Set.copyOf` (Java 9 / 10) return **unmodifiable** sets: mutators throw, duplicates at `of` throw `IllegalArgumentException`, `null` throws `NPE` ([[What does Set.of return and what happens with duplicates]]).

Implementations choose cost and order: `HashSet` (hash table), `LinkedHashSet` (insertion encounter order), `TreeSet` (`TreeMap`, comparator / natural order). Some reject `null` or restrict element types (`NPE` / `ClassCastException`). Querying an ineligible element may throw or return `false`.

> [!warning] Mutable keys break the set
> If you mutate an element so that `equals` (or a `TreeSet` comparator) changes while it is in the set, behavior is unspecified. A set must not contain itself. Sorted implementations that are **not consistent with `equals`** violate the `Set` contract: two elements can be unique by comparator yet `equals` each other ([[How do HashSet and TreeSet decide whether two elements are duplicates]]).

> [!warning] Unmodifiable is not deeply immutable
> `Set.of` still wraps mutable elements. Changing those objects can make membership look different. `HashSet` allows one `null`; `TreeSet` with natural order and `Set.of` do not ([[Does HashSet allow a null element]]).

> [!tip] Interview answer
> **`Set` is a `Collection` of unique members by `equals`, since Java 1.2, with no positional access.** `add` returns `false` on a duplicate. `equals` compares membership, not order. Name `HashSet`, `LinkedHashSet`, and `TreeSet` as the usual implementations.
