<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/Set/HashSet #SRS

# How do you convert a `HashSet` to an `ArrayList` in one line?

> [!abstract] Short answer
> **`new ArrayList<>(hashSet)`.** The `ArrayList(Collection)` constructor copies the set’s elements in iterator order into a new, independent list. That is the one-liner. `Collectors.toList()` is not specified to return an `ArrayList`.

## The collection copy constructor

`ArrayList(Collection<? extends E> c)` “constructs a list containing the elements of the specified collection, in the order they are returned by the collection’s iterator.” `HashSet` is a `Collection`. A null set is `NullPointerException`.

```java
Set<Integer> set = new HashSet<>();
set.add(3);
set.add(1);
set.add(2);

ArrayList<Integer> list = new ArrayList<>(set);
```

**Listing 1.** One constructor call. The list is a **snapshot of references** (shallow copy): later `set.add` / `set.remove` does not change `list`, and later `list.add` does not change `set`. Element objects themselves are shared.

`HashSet` iteration order is unspecified and need not stay constant ([[When should you choose HashSet LinkedHashSet or TreeSet]]). The list’s index order is whatever that iterator emitted **this time**, not insertion order and not sorted order. Need a stable walk? Convert a `LinkedHashSet` or `TreeSet` the same way.

```d2
direction: right
set: "HashSet\niterator, no order" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
ctor: "new ArrayList<>(set)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
list: "ArrayList\nsame elements, list indexes" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

set -> ctor
ctor -> list
```

**Fig. 1.** No shared backing store. The set is not “viewed as” a list.

A stream one-liner that is actually an `ArrayList` is `set.stream().collect(Collectors.toCollection(ArrayList::new))`. `Collectors.toList()` explicitly gives **no** guarantee of type or mutability. `set.toArray()` is an `Object[]`, not a list.

`HashSet` may hold one `null` ([[Does HashSet allow a null element]]). The constructor copies that `null` into the list. That is different from `List.of` / `List.copyOf`, which reject nulls ([[What is the difference between List.of(1,2,3) new ArrayList]]).

The reverse one-liner is `new HashSet<>(arrayList)` — `HashSet(Collection)` — and is a different cue ([[How do you convert an ArrayList to a HashSet in one line]]). Duplicates in the list collapse.

> [!warning] `new ArrayList<>(new HashSet<>())` converts an empty set
> Interview snippets that construct a **fresh** `HashSet` inside the call compile and give you an empty `ArrayList`. Pass the **existing** set: `new ArrayList<>(set)`.

> [!warning] The list will not remember set uniqueness
> After the copy, `list.add(list.get(0))` is a legal duplicate. Uniqueness lived in the `HashSet`, not in `ArrayList`.

> [!tip] Interview answer
> **`ArrayList<E> list = new ArrayList<>(hashSet);` — the collection constructor copies iterator order.** Order is whatever `HashSet` happens to visit. The list is a separate mutable snapshot, including a possible `null` element.
