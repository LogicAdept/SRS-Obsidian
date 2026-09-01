<!--
reps: 0
priority: 0
-->
#Java/Collections/Set #SRS

# What are the main Java Set implementations?

> [!abstract] Short answer
> **General-purpose: `HashSet`, `LinkedHashSet`, `TreeSet`.** Specialized: `EnumSet` for a single enum type. Concurrent: `ConcurrentHashMap.newKeySet()`, `ConcurrentSkipListSet`, `CopyOnWriteArraySet`. There is no `ConcurrentHashSet` class. All implement `Set` (unique by `equals`, except sorted sets which use the comparator).

## The three you name first

| Class | Since | Backing | Order | Null | Cost (documented) |
| --- | --- | --- | --- | --- | --- |
| `HashSet` | 1.2 | `HashMap` | none | one | expected constant `add`/`contains`/`remove` |
| `LinkedHashSet` | 1.4 | hash table + linked list | insertion encounter order | one | like `HashSet`, plus list cost |
| `TreeSet` | 1.2 | `TreeMap` (red-black) | sorted / `NavigableSet` | not with natural order | guaranteed log(n) |

Pick **order first**, then cost ([[When should you choose HashSet LinkedHashSet or TreeSet]]). Default interview answer is `HashSet` ([[What is a HashSet]], [[How does HashSet differ from LinkedHashSet]]). Need ranges / `floor` → `TreeSet`. Need insertion order → `LinkedHashSet`.

```d2
direction: down
set: "Set" {
  width: 140
  height: 45
  style.fill: "#e3f2fd"
}
hash: "HashSet" {
  width: 140
  height: 45
  style.fill: "#e8f5e9"
}
linked: "LinkedHashSet" {
  width: 160
  height: 45
  style.fill: "#fff3e0"
}
tree: "TreeSet" {
  width: 140
  height: 45
  style.fill: "#fce4ec"
}
enum: "EnumSet" {
  width: 140
  height: 45
  style.fill: "#f3e5f5"
}

set -> hash
set -> linked
set -> tree
set -> enum
```

**Fig. 1.** General-purpose trio plus `EnumSet`. Concurrent types live in `java.util.concurrent` and are not subclasses of `HashSet`.

```java
Set<String> hash = new HashSet<>();           // default membership
Set<String> linked = new LinkedHashSet<>();   // encounter order
NavigableSet<String> tree = new TreeSet<>();  // sorted + navigation
```

**Listing 1.** Program to `Set` / `NavigableSet`. Construct the class that matches order and cost.

## Specialized and concurrent

**`EnumSet`** (1.5): all elements from **one** enum type; internal **bit vector**. Factories `noneOf` / `allOf` / `of` / `range` / `complementOf` — not `new EnumSet`. No null insert (`NPE`). Iterator is declaration order, weakly consistent. Basic ops constant time; bulk ops vs another `EnumSet` also constant. Typesafe bit flags ([[What is EnumSet]]).

**Concurrent** ([[How do you get a concurrent Set in Java]]):

- `ConcurrentHashMap.newKeySet()` — concurrent **hash** set (`Boolean.TRUE` values, no null, Java 8).
- `ConcurrentSkipListSet` — concurrent `NavigableSet`, expected log(n), no null ([[What is ConcurrentSkipListSet]]).
- `CopyOnWriteArraySet` — array, copy on write, snapshot iterators; small read-mostly ([[What is CopyOnWriteArraySet]]).

`Collections.synchronizedSet` is a mutex **wrapper**, not a concurrent implementation. `Set.of` / `Set.copyOf` are unmodifiable factories, not `HashSet` ([[What does Set.of return and what happens with duplicates]]).

> [!warning] There is no `ConcurrentHashSet`
> Interview lists that invent that class are wrong. The hash concurrent set is `ConcurrentHashMap.newKeySet()`. `Hashtable`-style “synchronized HashSet” is `Collections.synchronizedSet(new HashSet<>())` — one lock, still lock around iteration.

> [!warning] `TreeSet` is not “the ordered HashSet”
> It is a different structure (tree, comparator, no hash). Sorted uniqueness is slower than `HashSet` and rejects null under natural order. `LinkedHashSet` is the hash set that keeps insertion order.

> [!tip] Interview answer
> **Main general-purpose sets: `HashSet` (hash, no order), `LinkedHashSet` (hash plus insertion order), `TreeSet` (sorted `NavigableSet`).** `EnumSet` is the bit-vector set for one enum. For threads, `newKeySet()`, `ConcurrentSkipListSet`, or `CopyOnWriteArraySet` — not a class named `ConcurrentHashSet`.
