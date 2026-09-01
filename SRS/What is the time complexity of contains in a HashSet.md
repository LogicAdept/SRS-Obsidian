<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #SRS

# What is the time complexity of `contains` in a `HashSet`?

> [!abstract] Short answer
> **Expected constant time — O(1) — if `hashCode` spreads keys across buckets.** That is the HashSet javadoc for `contains` (with `add`, `remove`, and `size`). A bad hash, or a single crowded bin, makes `contains` walk that bin: a list in O(n), or a tree in O(log n) after OpenJDK treeifies it.

## `contains` is one map lookup

`HashSet.contains(o)` is `map.containsKey(o)` ([[How is HashSet implemented in terms of HashMap]]). OpenJDK `HashMap.containsKey` is `getNode(key) != null`. `getNode` hashes the argument, indexes one bin, then:

1. Compares the first node (`hash` and `==` / `equals`).
2. If that node is a tree node, searches the bin as a tree.
3. Otherwise walks the linked list.

```java
public boolean contains(Object o) {
    return map.containsKey(o);
}
```

**Listing 1.** OpenJDK 21 `HashSet.contains`. No scan of the whole set. Iteration is the operation whose cost is size **plus capacity** ([[What is a HashSet]]).

```d2
direction: down
c: "contains(o)" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
h: "hash(o) → one bin" {
  width: 220
  height: 55
  style.fill: "#fff3e0"
}
list: "list walk\nO(bin length)" {
  width: 200
  height: 70
  style.fill: "#ffcdd2"
}
tree: "TreeNode bin\nO(log bin length)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

c -> h
h -> list
h -> tree
```

**Fig. 1.** Average O(1) means “usually one or a few nodes in that bin,” not “the CPU does one instruction.” Collisions share a bin ([[When does a hashCode collision occur in a HashMap]], [[Is equals invoked when a HashMap bucket contains a single element]]).

The documented assumption is the same as `HashMap`’s `get`/`put`: the hash function **disperses elements properly among the buckets**. Load factor 0.75 keeps average bin length small; it does not cap worst-case length if every key hashes together.

OpenJDK treeifies a bin at `TREEIFY_THRESHOLD` (8) once the table is large enough. Tree search is O(log n) in that bin when keys are comparable. A constant `hashCode` on incomparable keys still leaves a long list. `TreeSet.contains` is a different contract: guaranteed `log(n)` on a red-black tree, no hash ([[What is the difference between TreeSet and HashSet]]).

`contains(null)` is the null-key path (`hash` 0). Still one bin, still expected O(1) ([[Does HashSet allow a null element]]).

> [!warning] “`contains` is O(1)” without the hash assumption is incomplete
> The javadoc states constant time **assuming** a dispersing hash. A class whose `hashCode` is `return 42` makes `HashSet.contains` scan every member. That still compiles.

> [!warning] Do not quote iteration cost for `contains`
> Walking the set is O(size + capacity). `contains` does not visit empty buckets. Oversizing the table hurts `iterator`, not a single membership test.

> [!tip] Interview answer
> **Average O(1): `contains` hashes to one `HashMap` bin and compares there.** Quote the javadoc’s “assuming the hash function disperses the elements.” Worst case is a full-bin scan — list O(n), or O(log n) if that bin has been treeified.
