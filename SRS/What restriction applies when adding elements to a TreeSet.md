<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS

# What restriction applies when adding elements to a TreeSet?

> [!abstract] Short answer
> **Every insert must be mutually comparable with the elements already in the set.** With the no-arg constructor, every element must implement `Comparable`, and `e1.compareTo(e2)` must not throw. A comparator constructor uses `comparator.compare(e1, e2)` instead. A violation throws **`ClassCastException`**. **`null` throws `NullPointerException`** under natural order (or any comparator that rejects null).

## Comparable keys, not hash keys

`TreeSet` is a `NavigableSet` on a `TreeMap`. `add` compares with `compareTo` / `compare`, not `equals` / `hashCode`. That is the insert restriction: the new element must sit in the same total order as the rest.

`TreeSet()` and `TreeSet(Collection)` document:

- all elements implement `Comparable`
- all pairs are mutually comparable (`e1.compareTo(e2)` does not throw)
- mixing incomparable types (for example a `String` into a set of `Integer`) makes **`add` throw `ClassCastException`**

`TreeSet(Comparator)` has the same pairwise rule through the comparator. Passing `null` as the comparator falls back to natural order.

`add` also throws **`NullPointerException`** if the element is null and the set uses natural ordering, or the comparator does not permit null ([[Can a TreeSet contain null]]). `addAll` uses the same throws.

```d2
direction: down
add: "add(e)" {
  width: 140
  height: 45
  style.fill: "#eceff1"
}
ok: "comparable with current members" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
cce: "ClassCastException" {
  width: 200
  height: 45
  style.fill: "#ffcdd2"
}
npe: "NullPointerException" {
  width: 200
  height: 45
  style.fill: "#ffe0b2"
}

add -> ok: "compareTo / compare succeeds"
add -> cce: "incomparable type"
add -> npe: "null + natural order"
```

**Fig. 1.** Inserts fail unless `e` can be ordered against what is already in the tree.

```java
Set<Object> nums = new TreeSet<>();
nums.add(1);
nums.add("two");           // ClassCastException

Set<String> names = new TreeSet<>();
names.add(null);           // NullPointerException
```

**Listing 1.** Default `TreeSet` rejects mixed types and null. `Comparator.nullsFirst(Comparator.naturalOrder())` can allow one null ([[Can a TreeSet contain null]]).

Uniqueness is **`compare == 0`**, not `equals`. An ordering that is not consistent with `equals` still inserts, but then the set does not obey the `Set` contract ([[How do HashSet and TreeSet decide whether two elements are duplicates]], [[Why must TreeMap ordering be consistent with equals]]). Sorted inserts do not unbalance the red-black tree ([[What happens when you insert elements into a TreeSet in ascending order]]).

> [!warning] `addFirst` / `addLast` never insert
> Since Java 21 those `SequencedSet` methods throw **`UnsupportedOperationException` always**. Encounter order is the comparator order; you cannot pin an element at an end.

> [!warning] `HashSet` does not have this restriction
> `HashSet.add` needs a stable `hashCode` / `equals`. It accepts mixed types and one null. Putting a type that is not `Comparable` into a default `TreeSet` compiles as `TreeSet<Object>` and fails at run time.

> [!tip] Interview answer
> **Elements in a `TreeSet` must be mutually comparable.** With natural order they must implement `Comparable`, and null is forbidden. Otherwise `add` throws `ClassCastException` or `NullPointerException`. Duplicates are `compareTo == 0`, not `equals`.
