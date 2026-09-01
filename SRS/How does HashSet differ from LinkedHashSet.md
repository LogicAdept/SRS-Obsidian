<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Set/LinkedHashSet #SRS

# How does `HashSet` differ from `LinkedHashSet`?

> [!abstract] Short answer
> **`HashSet` has no encounter-order contract. `LinkedHashSet` is a `HashSet` subclass that keeps a doubly-linked list of entries so iteration is insertion (encounter) order.** Same uniqueness (`equals` / `hashCode`), same null rule, same “not synchronized.” The list costs a little on `add`/`remove` and makes iteration **O(size)** instead of **O(size + capacity)**.

## Order is the public difference

`HashSet` “makes no guarantees as to the iteration order of the set; in particular, it does not guarantee that the order will remain constant over time.” `LinkedHashSet` exists to spare clients that “unspecified, generally chaotic ordering” without `TreeSet`’s `log(n)` ([[When should you choose HashSet LinkedHashSet or TreeSet]]).

Encounter order is **eldest (least recently inserted) first, youngest last**. `add` of an element that is **already** in the set does **not** move it. Java 21 `addFirst` / `addLast` **do** relocate ([[How is HashSet implemented in terms of HashMap]] is the map; here the map is linked).

```java
Set<String> hash = new HashSet<>();
hash.add("b");
hash.add("a");
hash.add("b"); // still size 1 for "b"; order unspecified

Set<String> linked = new LinkedHashSet<>();
linked.add("b");
linked.add("a");
linked.add("b"); // false; "b" stays first
// linked iterates b, a
```

**Listing 1.** Duplicate `add` is a no-op for membership **and** for LinkedHashSet encounter order.

```d2
direction: down
hs: "HashSet\nHashMap keys, chaotic walk" {
  width: 300
  height: 70
  style.fill: "#ffcdd2"
}
lhs: "LinkedHashSet extends HashSet\nLinkedHashMap + list of entries" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}
ops: "add / contains / remove\nsame Set contract" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

hs -> ops
lhs -> ops
```

**Fig. 1.** LinkedHashSet is not a second hash algorithm. It is HashSet plus a list that defines iteration.

## OpenJDK: same `HashSet` methods, different map

`LinkedHashSet` constructors call the package-private `HashSet(int, float, boolean)` constructor, which installs a `LinkedHashMap` instead of a `HashMap`. Inherited `add` is still `map.put(e, PRESENT)`.

```java
public LinkedHashSet() {
    super(16, .75f, true); // dummy flag → LinkedHashMap
}
```

**Listing 2.** OpenJDK 21. The `true` is only a overload discriminator, not a public “access order” switch (`LinkedHashMap` access-order is a different class feature).

Both permit the `null` element ([[Does HashSet allow a null element]]). Both are unsynchronized ([[Is HashSet synchronized]]); wrap `LinkedHashSet` the same way: `Collections.synchronizedSet`. Fail-fast iterators on both.

| | `HashSet` | `LinkedHashSet` |
| --- | --- | --- |
| Since | 1.2 | 1.4 |
| Backing (OpenJDK) | `HashMap` | `LinkedHashMap` |
| Iteration order | unspecified | insertion / encounter |
| Iteration time | size + capacity | size only |
| `add`/`contains`/`remove` | expected constant | expected constant, slightly slower |
| `SequencedSet` | no | yes (`addFirst` / `reversed`, Java 21) |
| Spliterator | `SIZED`, `DISTINCT` | plus `ORDERED` |

Copying any set while keeping **presentation order**: `new LinkedHashSet<>(other)` — that is the javadoc’s stated use.

> [!warning] “The only difference is LinkedHashMap” is the implementation, not the interview stop
> Naming the map is correct in OpenJDK. The **contract** difference is encounter order, iteration cost vs capacity, and (since 21) sequenced ops. Uniqueness is not different.

> [!warning] `add` does not refresh order; `addFirst` / `addLast` do
> Dumps that say “insertion order never changes” miss Java 21: `addLast(e)` on an existing element **moves** it to the end. Plain `add(e)` still does not.

> [!tip] Interview answer
> **`HashSet` is unordered; `LinkedHashSet` is a `HashSet` that also walks in insertion order via a doubly-linked list (a `LinkedHashMap` in OpenJDK).** Re-`add` does not move an element. You pay a little per update and you iterate in **O(n)** even if the table is sparse. Use it when uniqueness must be replayed in first-seen order.
