<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/LinkedHashSet #SRS

# What is `java.util.LinkedHashSet`?

> [!abstract] Short answer
> **A `HashSet` with a doubly-linked list that records encounter order (Java 1.4).** Iteration is insertion order: eldest first, youngest last. `add` of an element already present does **not** move it. You get hash-set membership plus a predictable walk, without `TreeSet`’s log(n) sort.

## Hash table plus a list of entries

`public class LinkedHashSet<E> extends HashSet<E> implements SequencedSet<E>, Cloneable, Serializable`. Same hash table as `HashSet`, plus a **doubly-linked list through all entries**. That list *is* iteration order. It spares clients the “generally chaotic” `HashSet` order without `TreeSet`’s cost ([[How does HashSet differ from LinkedHashSet]], [[What is a HashSet]]).

Re-`add` of a member leaves its position alone (`add` returns `false` and does not relocate). Java 21 `addFirst` / `addLast` **do** relocate an existing element to the front or back. `reversed()` is a live reverse-order `SequencedSet` view. `getFirst` / `getLast` / `removeFirst` / `removeLast` throw `NoSuchElementException` if empty.

```d2
direction: down
api: "Set + SequencedSet\nunique, encounter order" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
impl: "LinkedHashSet\nHashSet + doubly-linked list" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
walk: "iterator: eldest → youngest\ntime ~ size, not capacity" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

api -> impl
impl -> walk
```

**Fig. 1.** Membership is the hash table. Order is the list. `HashSet` iteration is proportional to **capacity**; this class’s iteration is proportional to **size**.

```java
Set<String> s = new LinkedHashSet<>();
s.add("b");
s.add("a");
s.add("b");           // false; still b, then a
s.iterator().next();  // "b"
```

**Listing 1.** Second `add("b")` does not send `b` to the end. `new LinkedHashSet<>(other)` copies elements in `other`’s iterator order — useful to preserve presentation order regardless of the source set’s type.

Basic ops (`add`, `contains`, `remove`) are **constant time** if hashes spread, **slightly slower** than `HashSet` because of the list. One exception: iteration here is **O(size)**; a bloated `HashSet` capacity is expensive to walk. Default capacity 16, load factor 0.75. Java 19 `LinkedHashSet.newLinkedHashSet(n)` sizes for *n* elements.

Permits **null**. Not synchronized — wrap with `Collections.synchronizedSet` at creation. Iterators are fail-fast (`ConcurrentModificationException` is best-effort).

> [!warning] `add` does not refresh position
> Re-inserting with `add` leaves the element where it was. To move a member to the front or back, `addFirst` / `addLast` (Java 21). There is no access-order mode on this class.

> [!warning] Still a `Set`, not a `List`
> No `get(int)`. Duplicate `equals` is rejected. Encounter order does not make `List.equals` apply ([[What is the difference between List and Set]]). For sorted order use `TreeSet`, not this list ([[When should you choose HashSet LinkedHashSet or TreeSet]]).

> [!tip] Interview answer
> **`LinkedHashSet` is `HashSet` plus a doubly-linked list of entries (Java 1.4): unique elements, iteration in insertion order, re-`add` does not move.** Slightly slower than `HashSet` except iteration, which is O(size) not O(capacity). Java 21 `addFirst`/`addLast` relocate; `TreeSet` is the sorted alternative.
