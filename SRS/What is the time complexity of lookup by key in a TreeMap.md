<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Map/HashMap #DSA/Complexity #DSA/DataStructures/Tree/RedBlack #SRS

# What is the time complexity of lookup by key in a `TreeMap`?

> [!abstract] Short answer
> **Guaranteed log(n) for `containsKey` and `get`.** The class javadoc states that cost for `containsKey`, `get`, `put`, and `remove`. `n` is the number of mappings. Lookup walks a red-black tree with `compareTo` or `Comparator.compare`, not `hashCode`. That bound is unconditional in the spec. `HashMap`’s constant-time `get` is only **assuming** hashes disperse.

## What Java SE actually guarantees

```text
TreeMap
  containsKey, get, put, remove
    guaranteed log(n)

HashMap
  get, put
    constant-time, assuming hashes disperse among buckets
```

**Listing 1.** Class-level wording from the Java SE 21 javadocs. `TreeMap` uses “guaranteed.” `HashMap` uses “assuming.” The `Map` interface itself does not give `get` a complexity.

`TreeMap` is a red-black tree `NavigableMap`. Keys are ordered by natural order or by a `Comparator` supplied at construction. `get` finds a mapping whose key **compares equal** under that ordering. `hashCode` is not part of the search. [[What data structure backs TreeMap in Java]] is the tree. [[Does HashMap guarantee its documented lookup time complexity]] is the contrast.

```d2
direction: down
key: "get(key) / containsKey(key)" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
cmp: "compareTo / Comparator.compare\ndown the red-black tree" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
hit: "log(n) comparisons\nguaranteed" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}

key -> cmp -> hit
```

**Fig. 1.** Key lookup is a tree walk. Bad `hashCode` does not turn this into a linear scan.

`put` and `remove` share the same guaranteed log(n). Building a `TreeMap` from an unsorted `Map` is documented as n log(n), which is n inserts, not a single lookup.

## What log(n) does not cover

`containsValue` is not a key lookup. Its javadoc says the operation will probably take time linear in the map size for most implementations. Iteration of a view is a tree traversal, not log(n) per element.

Ordering must be **consistent with `equals`** if the map is to obey the `Map` contract: two keys that `compare` as equal are one key to the tree, even if `equals` disagrees. The behavior is still well-defined when they disagree; it just fails the general `Map` contract. That is a correctness trap, not a different complexity.

A `null` key throws `NullPointerException` when the map uses natural ordering, or when its comparator does not permit nulls. That is not a log(n) miss.

> [!warning] “O(log n) like a balanced tree” vs the HashMap slogan
> Interview answers that say both maps are “average O(1)” mix the types. `TreeMap` does not hash. `HashMap` does not guarantee log(n) either: Java 8 tree bins are an implementation backstop with extra conditions. [[What is the algorithmic complexity of HashMap operations]] is that table. [[Compare HashMap and TreeMap tradeoffs]] is when you pick the slower, ordered map on purpose.

> [!tip] Interview answer
> **`TreeMap` key lookup is guaranteed log(n): `containsKey` and `get` walk a red-black tree with `compare`/`compareTo`. The same bound is documented for `put` and `remove`. It does not depend on `hashCode`. `HashMap.get` is expected constant-time only if hashes spread. `containsValue` is not log(n).**
