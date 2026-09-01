<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/Set/HashSet #SRS

# How do you convert an `ArrayList` to a `HashSet` in one line?

> [!abstract] Short answer
> **`new HashSet<>(arrayList)`.** The `HashSet(Collection)` constructor copies the list’s elements into a new set. Duplicates (by `equals` / `hashCode`) collapse to one member. Order is not kept.

## The collection copy constructor

`HashSet(Collection<? extends E> c)` “constructs a new set containing the elements in the specified collection.” The backing `HashMap` uses load factor 0.75 and an initial capacity large enough for those elements. A null list is `NullPointerException`.

```java
List<Integer> list = new ArrayList<>();
list.add(1);
list.add(2);
list.add(1);

HashSet<Integer> set = new HashSet<>(list);
set.size(); // 2 — the second 1 is a duplicate
```

**Listing 1.** One constructor call. The set is a **snapshot of references**: later `list.add` / `list.remove` does not change `set`, and later `set.add` does not change `list`.

`ArrayList` iterator order is index order. `HashSet` does **not** promise to iterate in that order ([[When should you choose HashSet LinkedHashSet or TreeSet]]). Need unique elements **and** first-seen order? `new LinkedHashSet<>(list)` is the same one-liner on a different class.

```d2
direction: right
list: "ArrayList\nindex order, duplicates allowed" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
ctor: "new HashSet<>(list)" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
set: "HashSet\nunique, no order" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

list -> ctor
ctor -> set
```

**Fig. 1.** Dedup is a consequence of `Set.add`, not a second pass. The list is unchanged.

A stream line that is actually a `HashSet` is `list.stream().collect(Collectors.toCollection(HashSet::new))`. `Collectors.toSet()` does not specify the set type. `Set.copyOf(list)` is an **unmodifiable** set, not a `HashSet`, and it rejects nulls.

`ArrayList` may contain `null`. `HashSet` keeps **at most one** ([[Does HashSet allow a null element]]). `Set.of` / `Set.copyOf` throw `NullPointerException` instead.

This is also the usual “remove duplicates from a list” trick: `new ArrayList<>(new HashSet<>(list))` — uniqueness with **lost** order ([[How do you remove duplicates from an ArrayList]]).

The reverse one-liner is `new ArrayList<>(hashSet)` ([[How do you convert a HashSet to an ArrayList in one line]]).

> [!warning] `new HashSet<>(new ArrayList<>())` converts an empty list
> Pass the **existing** list: `new HashSet<>(list)`. A nested `new ArrayList<>()` compiles and gives you an empty set.

> [!warning] This is not a view
> The `HashSet` does not wrap the `ArrayList`. Two structures, shared element objects. Mutating a mutable element after the copy can break set lookup the same way as any `HashSet` key.

> [!tip] Interview answer
> **`HashSet<E> set = new HashSet<>(arrayList);` — the collection constructor copies and drops duplicates.** You lose list order; use `LinkedHashSet` if first-seen order matters. One `null` in the list becomes one `null` in the set.
