<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/LinkedHashMap #Java/Collections/Map/TreeMap #Java/HashCodeEquals #SRS

# How do `HashMap`, `TreeMap`, and `LinkedHashMap` work at a high level?

> [!abstract] Short answer
> **`HashMap` indexes an array of bins with a mixed `hashCode`, then walks a list (or a per-bin tree).** **`LinkedHashMap` does the same lookup and also threads every entry on a doubly-linked list that is the iteration order.** **`TreeMap` ignores hashes: it walks a red-black tree with `compareTo` / `Comparator.compare`.** Lookup is “which bucket?” versus “which child?” versus “bucket, then also move a list pointer.”

## Three machines

```d2
direction: down
hm: "HashMap\n(n-1) & hash → bin" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
lhm: "LinkedHashMap\nsame bins + before/after list" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
tm: "TreeMap\ncompare → left / right" {
  width: 280
  height: 80
  style.fill: "#ffe0b2"
}

hm -> lhm: extends HashMap
```

**Fig. 1.** `LinkedHashMap` is a `HashMap` with an extra list through all entries. `TreeMap` is a different structure.

`HashMap` keeps `Node[] table`. Mix the key’s `hashCode`, take `(n - 1) & hash`, follow `next` (or a `TreeNode` bin in Java 8+). Equality is identity then `equals`. Order of bins is not an API. [[What is the internal structure of HashMap]] and [[How does HashMap handle collisions]] are that path.

`TreeMap` keeps one `root`. Each `Entry` has `left`, `right`, `parent`, and a red-black color. Insert and `get` branch on key order, then rotate to restore the tree. There is no table length and no `hashCode` in the search. [[What data structure backs TreeMap in Java]] is that node.

`LinkedHashMap` javadoc: hash table **and** linked list. OpenJDK’s entry is a `HashMap.Node` plus list links:

```java
static class Entry<K,V> extends HashMap.Node<K,V> {
    Entry<K,V> before, after;
}
```

**Listing 1.** The same bin `next` chain as `HashMap`, plus `before`/`after` for encounter order. `head` is eldest, `tail` is youngest.

`get` still hashes into the table. The list is for **iteration** (and, in access-order mode, for moving an entry to the tail on access). That is why iteration is proportional to size, not capacity: you walk `after`, not empty buckets. [[What are LinkedHashMap ordering guarantees]] is insertion-order versus access-order.

## What a `put` does

A new `HashMap` key lands in one bin and may trigger resize when `size` exceeds `capacity × loadFactor`. A new `LinkedHashMap` key does that **and** is linked at the tail (insertion-order). A new `TreeMap` key is placed in the BST and the tree is recolored/rotated; cost is guaranteed log(n).

Re-`put` of an equal `HashMap`/`LinkedHashMap` key replaces the value in that node. Insertion-order `LinkedHashMap` does **not** relink. Access-order does, on the documented access methods. `TreeMap` replace is still a tree find; `compare == 0` is the same key.

> [!warning] Two kinds of “linked”
> Bin `next` is collision chaining inside one bucket. `LinkedHashMap.before`/`after` is a list of **all** mappings. Do not call `TreeMap` “a linked HashMap.” Sorted order is tree shape, not a list of insertion times. [[How do HashMap, TreeMap, and LinkedHashMap differ at a high level]] is which one to choose.

> [!tip] Interview answer
> **`HashMap` works by hashing into an array of chains (sometimes trees). `LinkedHashMap` is that table plus a doubly-linked list through every entry so iteration has a defined encounter order. `TreeMap` works by comparing keys in a red-black tree. Same `Map` API, three lookup machines.**
