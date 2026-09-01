<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS

# Can a TreeSet contain null?

> [!abstract] Short answer
> **Not under natural ordering: `add(null)` throws `NullPointerException`.** A `TreeSet` *can* hold one `null` if you construct it with a `Comparator` that permits null arguments (`Comparator.nullsFirst` / `nullsLast`). Default `new TreeSet<>()` does not.

## Natural order rejects null; a null-friendly comparator may not

`TreeSet.add` (and `contains` / `remove`) throw `NullPointerException` if the element is **null and this set uses natural ordering, or its comparator does not permit null elements**. Empty constructor and `TreeSet(Collection)` use **natural ordering**: every element must be `Comparable`, and `null` has no `compareTo`. `Comparator.naturalOrder()` / `reverseOrder()` also throw NPE when comparing `null`.

`Comparator`, unlike `Comparable`, **may optionally permit** null arguments. `Comparator.nullsFirst(c)` treats `null` as less than non-null (two nulls compare equal); `nullsLast` treats `null` as greater. Pass that comparator to `new TreeSet<>(...)` and `add(null)` succeeds. `Set` still allows **at most one** null ([[Does HashSet allow a null element]]).

```java
Set<String> natural = new TreeSet<>();
natural.add(null); // NullPointerException

Set<String> nullable = new TreeSet<>(Comparator.nullsFirst(Comparator.naturalOrder()));
nullable.add(null); // true
nullable.add("a");
nullable.add(null); // false — already one null
```

**Listing 1.** Default tree: no null. `nullsFirst` + natural order: one null, then strings.

`NavigableSet` **encourages** implementations not to insert null. Neighbour methods return `null` to mean “no such element,” so a stored null is ambiguous (`contains(null)` vs `floor(x) == null`). Sorted sets of `Comparable` elements intrinsically do not permit null ([[What NavigableSet operations does TreeSet provide]]). `ConcurrentSkipListSet` forbids null for the same concurrent-collection reason ([[What is ConcurrentSkipListSet]]).

```d2
direction: down
ask: "TreeSet.add(null)?" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
nat: "natural ordering\nNullPointerException" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
cmp: "Comparator that permits null\none null allowed" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

ask -> nat
ask -> cmp
```

**Fig. 1.** The constructor’s ordering, not the class name, decides. Interview default is NPE.

> [!warning] `HashSet` is the wrong mental model
> `HashSet` permits one `null`. `TreeSet` does not, unless the comparator says so. `new TreeSet<>(aHashSetThatContainsNull)` still uses natural ordering of the copy constructor and throws NPE on the null element.

> [!warning] Navigation `null` is not “the null element”
> `floor(e)` returning `null` means **no match** (or you passed a forbidden null argument). If you stored a null with `nullsFirst`, `first()` can be `null` and `pollFirst()` can return `null` on a **non-empty** set. That is why the default tree refuses null.

> [!tip] Interview answer
> **A default `TreeSet` cannot contain null — `add(null)` is `NullPointerException` because natural order uses `Comparable`.** You can allow one null only with a null-friendly comparator such as `Comparator.nullsFirst`. `HashSet` allows one null; `ConcurrentSkipListSet` never does.
