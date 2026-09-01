<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Set #SRS

# What is `ConcurrentSkipListSet`?

> [!abstract] Short answer
> **A scalable concurrent `NavigableSet` backed by a `ConcurrentSkipListMap` (`java.util.concurrent`, since 1.6).** Elements stay sorted (natural order or a constructor `Comparator`). `contains` / `add` / `remove` are expected average **log(n)**. Several threads may insert, remove, and access at once. It is not a hash set and not a synchronized `TreeSet`.

## Sorted, concurrent, not locked `TreeSet`

`public class ConcurrentSkipListSet<E> extends AbstractSet<E> implements NavigableSet<E>, Cloneable, Serializable`. The set is the keys of a `ConcurrentSkipListMap`. You get the same navigation surface as `TreeSet`: `lower` / `floor` / `ceiling` / `higher`, `pollFirst` / `pollLast`, `headSet` / `tailSet` / `subSet`, `descendingSet` / `descendingIterator` ([[What do TreeSet headSet tailSet and subSet return]], [[How do you iterate a TreeSet in reverse order]]).

Ascending views and iterators are **faster than descending** ones. Range views are still live and backed; out-of-range `add` throws `IllegalArgumentException`.

`null` is forbidden (`NullPointerException`): concurrent collections cannot tell a null argument from “no element.” Constructors that copy a collection or `SortedSet` also reject null elements. Java 21 `addFirst` / `addLast` always throw `UnsupportedOperationException` — order comes from the comparator, not from explicit positioning.

```d2
direction: down
api: "NavigableSet\nsorted unique elements" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
impl: "ConcurrentSkipListSet\nConcurrentSkipListMap keys" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
cost: "expected log(n) contains / add / remove\nsize() walks; bulk ops not atomic" {
  width: 360
  height: 80
  style.fill: "#e8f5e9"
}

api -> impl
impl -> cost
```

**Fig. 1.** Concurrent *and* ordered. Unsorted uniqueness is `ConcurrentHashMap.newKeySet()`, not this class.

```java
NavigableSet<Integer> ranks = new ConcurrentSkipListSet<>();
ranks.add(30);
ranks.add(10);
ranks.add(20);
ranks.first();     // 10
ranks.ceiling(15); // 20
ranks.headSet(20); // 10  (live view, exclusive high)
```

**Listing 1.** Natural order. A second `add(10)` returns `false`. `add(null)` throws `NullPointerException`.

## Concurrency contract

Insertion, removal, and access **safely run concurrently**. Iterators and spliterators are **weakly consistent** (not fail-fast `ConcurrentModificationException`, not a copy-on-write snapshot). The spliterator reports `CONCURRENT`, `NONNULL`, `DISTINCT`, `SORTED`, `ORDERED` (ascending).

`size()` is **not** constant time: it traverses, and the count can change while it runs, so the result may be **inaccurate**. The class says `size` is typically not very useful in concurrent applications. `equals` needs equal sizes, so equality under concurrent mutation is similarly shaky.

Bulk operations (`addAll`, `removeIf`, `forEach`, …) are **not** atomic as a whole. A `forEach` concurrent with `addAll` may see only some of the added elements.

For a concurrent **hash** set, use `ConcurrentHashMap.newKeySet()` ([[How do you get a concurrent Set in Java]]). For small read-mostly sets, `CopyOnWriteArraySet` ([[What is CopyOnWriteArraySet]]). For a non-thread-safe sorted set, `TreeSet`.

> [!warning] Not “synchronized” and not “fail-safe”
> This is not `Collections.synchronizedSortedSet(new TreeSet<>())`. There is no table-wide lock. Iterators are weakly consistent, not fail-safe and not a snapshot. Do not write a program that needs `size()` or `equals` to be a stable concurrent snapshot.

> [!warning] `newKeySet()` is the concurrent hash set
> `ConcurrentSkipListSet` pays log(n) and a sort order you may not need. If you only want thread-safe uniqueness, `ConcurrentHashMap.newKeySet()` is the hash-table answer. If you need ranges and `ceiling` / `headSet` under concurrent writers, stay here.

> [!tip] Interview answer
> **`ConcurrentSkipListSet` is the concurrent `NavigableSet` (Java 6), keys of a `ConcurrentSkipListMap`, expected log(n), no nulls.** Several threads may mutate it; iterators are weakly consistent; `size()` walks and can be wrong mid-update. Use it for sorted/range concurrency; use `newKeySet()` for an unsorted concurrent set.
