<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/Set/LinkedHashSet #Java/Collections/Set/HashSet #SRS

# How do you remove duplicates from an `ArrayList`?

> [!abstract] Short answer
> Copy through a `Set`. `new ArrayList<>(new LinkedHashSet<>(list))` keeps **first-insertion order** and uniqueness by `Objects.equals`. A `HashSet` copy also unique-ifies, but iteration order is unspecified. That does not mutate the original list.

## Unique by `equals`, then copy back

```d2
direction: down
list: "ArrayList\n[1, 1, 2, 3, 3]" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
lhs: "LinkedHashSet\ninsertion-order, first wins" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
hs: "HashSet\nunique, order unspecified" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
out: "new ArrayList<>(set)" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}

list -> lhs
list -> hs
lhs -> out
hs -> out
```

**Fig. 1.** A set constructor drops later equals-duplicates. Only `LinkedHashSet` documents encounter order as insertion order.

`Set.add` refuses a second element `e` when the set already has `e2` with `Objects.equals(e, e2)` and returns `false`. `LinkedHashSet(Collection)` / `HashSet(Collection)` build such a set from the list. `ArrayList(Collection)` then copies the set’s iterator into a new list ([[How do you convert a String array to an ArrayList]] uses the same copy constructor).

`LinkedHashSet` is a hash table plus a doubly-linked list that defines **insertion-order** encounter order. Re-inserting an element already in the set (`add` when `contains` is already true) does **not** move it. `HashSet` “makes no guarantees as to the iteration order of the set.” Both permit `null` (several `null`s collapse to one).

```java
ArrayList<Integer> numbers = new ArrayList<>(
        Arrays.asList(1, 1, 2, 3, 3, 3, 4, 5, 6, 6, 6, 7, 8));

ArrayList<Integer> unique = new ArrayList<>(new LinkedHashSet<>(numbers));
// unique is [1, 2, 3, 4, 5, 6, 7, 8]; numbers is unchanged
```

**Listing 1.** Usual interview copy: wrap in `LinkedHashSet`, copy back to `ArrayList`. First occurrence wins.

To **mutate** the same `ArrayList`, scan in list order and drop later hits. `Collection.removeIf` (Java 8) removes elements whose predicate is true. `Set.add` returns `false` on a duplicate, so `!seen.add(e)` means “already seen — remove”:

```java
ArrayList<Integer> numbers = new ArrayList<>(
        Arrays.asList(1, 1, 2, 3, 3, 3, 4, 5, 6, 6, 6, 7, 8));
Set<Integer> seen = new HashSet<>();
numbers.removeIf(n -> !seen.add(n)); // numbers is now [1, 2, 3, 4, 5, 6, 7, 8]
```

**Listing 2.** In-place: the list iterator supplies order, so a `HashSet` is enough as the seen-set. First occurrences stay; later equals-duplicates go. A `LinkedHashSet` seen-set is not required here.

Stream form (Java 8+): `ArrayList.spliterator` reports `ORDERED`, so `list.stream().distinct()` is **stable** — it keeps the first equal element. Collect with `Collectors.toCollection(ArrayList::new)` if you need an `ArrayList`. `Stream.toList()` and `Collectors.toSet()` are not a resizable `ArrayList` (and `toSet` does not promise order).

> [!warning] `new ArrayList<>(new HashSet<>(list))` shuffles relative order
> Uniqueness is the same (`Objects.equals`). Encounter order is not. Use `LinkedHashSet` (or in-place `removeIf`, or `distinct()` on an ordered stream) when the caller still wants first-seen list order.

> [!warning] Custom types need `equals` and `hashCode` together
> Hash-based sets treat two objects as one element only when `equals` says so **and** hashes match. Default identity `equals` means two “same field” instances both stay. Override both ([[Why should equals and hashCode be overridden together]]). `TreeSet` is a different contract: it uniques by `compareTo`/`compare`, must be consistent with `equals` to obey `Set`, sorts rather than keeping insertion order, and rejects `null` under natural ordering.

> [!tip] Interview answer
> **Copy through `LinkedHashSet`, then `new ArrayList<>(set)`.** That drops equals-duplicates and keeps first-insertion order. `HashSet` is fine if order does not matter, or as a seen-set with `removeIf` on the list itself. For a pipeline, `stream().distinct()` on an `ArrayList` is stable.
