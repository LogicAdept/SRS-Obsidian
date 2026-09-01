<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #SRS

# What is a `HashSet`?

> [!abstract] Short answer
> **A `Set` backed by a hash table — in the JDK, `java.util.HashSet`, a `HashMap` whose keys are the elements.** It stores unique objects (`equals` / `hashCode`), allows one `null`, does not keep order, and gives expected constant-time `add` / `contains` / `remove` / `size` when hashes spread.

## The collections-framework hash set

`public class HashSet<E> extends AbstractSet<E> implements Set<E>, Cloneable, Serializable` in `java.util` since **1.2**. Direct subclass for encounter order: `LinkedHashSet`. It wraps a `HashMap`: elements are keys, every value is one dummy `PRESENT` ([[How is HashSet implemented in terms of HashMap]], [[What internal structures back HashSet and TreeSet]]). That is why its rules match hash-map keys, not a second data structure.

```d2
direction: down
api: "Set<E>\nunique members, no list indexes" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
impl: "java.util.HashSet\nHashMap<E, PRESENT>" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
cost: "expected O(1) add / contains / remove\niteration ~ size + capacity" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}

api -> impl
impl -> cost
```

**Fig. 1.** You program to `Set`. You pay a hash table. Order is not part of the deal.

```java
Set<String> set = new HashSet<>();
set.add("b");
set.add("a");
set.add("b");      // false; size stays 2
set.contains("a"); // true
set.add(null);     // true; at most one null
```

**Listing 1.** Membership only. A second equal element is rejected. Iteration order of `"a"` vs `"b"` is unspecified and may change.

## What the class actually promises

- **Uniqueness:** `add(e)` succeeds only if no `e2` with `Objects.equals(e, e2)` is present.
- **Null:** the class “permits the `null` element” ([[Does HashSet allow a null element]]).
- **Time:** basic ops expected constant time if `hashCode` spreads keys; iterating is proportional to **size plus backing capacity** (oversized tables are expensive to walk).
- **Order:** none. Insertion order is `LinkedHashSet`; sorted order is `TreeSet` ([[When should you choose HashSet LinkedHashSet or TreeSet]], [[How does HashSet differ from LinkedHashSet]]).
- **Threads:** not synchronized. Wrap at creation with `Collections.synchronizedSet`, or use `ConcurrentHashMap.newKeySet()` ([[Is HashSet synchronized]]). Iterators are fail-fast (`ConcurrentModificationException` is best-effort, not a lock). This class is not in `java.util.concurrent`.
- **Defaults:** empty constructor → capacity 16, load factor 0.75 on the map. Java 19+ `HashSet.newHashSet(n)` sizes for *n* elements. `HashSet(Collection)` copies another collection and throws `NullPointerException` only if that **collection reference** is null.

It is not a `List`. Index `get(i)` does not exist. It is not a `Map` you can `get` a value from — contrast [[What is the difference between HashMap and HashSet]]. Mutable elements whose `equals`/`hashCode` change while in the set are unspecified, like any hash-based collection.

> [!warning] A `HashSet` is not “a HashMap of values”
> Interview shorthand that drops the dummy is wrong. There is always a value object; it is unused. The set is the **key set**.

> [!warning] “All operations delegate to HashMap” skips HashSet’s own methods
> `add` / `contains` / `remove` / `size` / `clear` / `iterator` do. `clone`, serialization, `spliterator`, and `newHashSet` are HashSet’s. The model is a map of keys; not every method is `map.foo`.

> [!warning] Constant time is a hash-quality claim
> A constant `hashCode` still compiles. Then every element shares a bin and `contains` becomes a walk. The javadoc’s “constant time” assumes a dispersing hash.

> [!tip] Interview answer
> **`HashSet` is the hash-table `Set` (`java.util.HashSet` since 1.2): unique elements as `HashMap` keys, one dummy value, no order, expected O(1) membership.** It allows one `null` and is not synchronized. Pick `LinkedHashSet` or `TreeSet` when you need encounter order or sorted order.
