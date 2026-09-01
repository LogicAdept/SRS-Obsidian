<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #SRS

# Does `HashSet` allow a null element?

> [!abstract] Short answer
> **Yes — at most one.** `HashSet` permits the `null` element. `add(null)`, `contains(null)`, and `remove(null)` are legal. A second `add(null)` is a duplicate and returns `false`; the set still has size one.

## Why one null is legal

`HashSet` is a `Set` backed by a `HashMap`. Elements are keys; every mapping’s value is the dummy `PRESENT` ([[How is HashSet implemented in terms of HashMap]]). `HashMap` permits the `null` key ([[Can HashMap store a null key]]), so the set permits a null element. `add` does not reject `null` itself: it is `map.put(e, PRESENT)`.

The `Set` contract already says a set contains no pair `e1`, `e2` with `Objects.equals(e1, e2)`, **and at most one null**. Two nulls are equal under that test, so they cannot both be members.

```d2
direction: down
add: "add(null)" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
put: "map.put(null, PRESENT)" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
hash: "hash(null) → 0" {
  width: 200
  height: 55
  style.fill: "#e8f5e9"
}
slot: "one null-key mapping" {
  width: 240
  height: 55
  style.fill: "#ffe0b2"
}

add -> put
put -> hash
hash -> slot
```

**Fig. 1.** The null element is the backing map’s null key. OpenJDK hashes a null key to `0`; uniqueness still comes from `equals`, not from hashing.

```java
public boolean add(E e) {
    return map.put(e, PRESENT) == null;
}
```

**Listing 1.** OpenJDK 21 `HashSet.add`. There is no `if (e == null)` guard. `put` returns `null` when there was no previous mapping, so the first `add(null)` is `true`.

```java
Set<String> set = new HashSet<>();
set.add(null);      // true
set.add(null);      // false — already present
set.size();         // 1
set.contains(null); // true
set.remove(null);   // true; now empty
```

**Listing 2.** One null occupies one slot. `contains` / `remove` use the same `Objects.equals` test, so they accept `null` too.

`HashSet(Collection)` throws `NullPointerException` only if the **collection reference** is null. A non-null collection that contains `null` is copied in; the null becomes that one element.

`LinkedHashSet` extends `HashSet` and keeps the same null rule ([[How does HashSet differ from LinkedHashSet]]).

## Other `Set` types do not copy this rule

The `Set` interface lets implementations forbid null. `add(null)` is then an optional NPE, not a `HashSet` behavior.

- `TreeSet` under natural ordering (the no-arg constructor) throws `NullPointerException` on `add(null)`: a null has no `compareTo`. A constructor `Comparator` that accepts null (for example `Comparator.nullsFirst`) is the documented exception ([[Can a TreeSet contain null]]). The tree is a `TreeMap`, not a `HashMap` ([[Can TreeMap have null keys or null values]]).
- `EnumSet` rejects `null` on insert with `NullPointerException`; `contains(null)` / `remove(null)` return `false` and do not throw ([[Does EnumSet allow null]]).
- `Set.of` and `Set.copyOf` disallow null elements. `Set.copyOf(set)` NPEs if the `HashSet` already holds `null`.

> [!warning] “A `Set` allows one null” names `HashSet`, not the interface
> Interview lists that say “`Set` allows a single null” are describing `HashSet` / `LinkedHashSet`. They are false for `EnumSet`, for `TreeSet` with natural order, and for `Set.of` / `Set.copyOf`. Saying “many nulls” is also wrong: uniqueness still applies; you get one.

> [!warning] `toArray(T[])` trailing-null is unsafe if the set holds `null`
> When the destination array is longer than the set, `toArray` writes a `null` after the last element as an end marker. That marker is usable only if you already know the collection contains no nulls. A `HashSet` that stores `null` makes that convention ambiguous.

> [!tip] Interview answer
> **Yes. `HashSet` allows one `null` because it is a `HashMap` whose keys are the elements, and `HashMap` allows one null key.** `add(null)` has no null check; a second `add(null)` returns `false`. Do not generalize that to `TreeSet`, `EnumSet`, or `Set.of`.
