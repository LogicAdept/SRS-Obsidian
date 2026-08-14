<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #DSA/DataStructures/Tree/RedBlack #SRS

# What data structure backs `TreeMap` in Java?

> [!abstract] Short answer
> **A red-black tree.** The class javadoc calls `TreeMap` a red-black-tree `NavigableMap`. There is no hash table. One `root` points at `Entry` nodes with `left`, `right`, `parent`, and a color. Keys stay sorted by `compareTo` or a `Comparator`. That is why `get`/`put`/`remove` are guaranteed log(n).

## One tree, not an array of buckets

`TreeMap` stores mappings in a binary search tree that is kept balanced as a red-black tree. Algorithms are documented as adaptations of CLRS. OpenJDK keeps:

```java
private transient Entry<K,V> root;

static final class Entry<K,V> implements Map.Entry<K,V> {
    K key;
    V value;
    Entry<K,V> left;
    Entry<K,V> right;
    Entry<K,V> parent;
    boolean color = BLACK;
}
```

**Listing 1.** Backing node from OpenJDK `TreeMap` (Java 21). Each `Map.Entry` you see from `entrySet` **is** a tree node, not a copy sitting beside the tree.

```d2
direction: down
root: "root" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
n: "Entry\nkey, value, color" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
l: "left" {
  width: 140
  height: 60
  style.fill: "#e8f5e9"
}
r: "right" {
  width: 140
  height: 60
  style.fill: "#e8f5e9"
}

root -> n
n -> l
n -> r
```

**Fig. 1.** The map is the tree. Capacity in the `HashMap` sense does not exist here.

Search, insert, and delete walk by key **order**, not by `hashCode`. Natural ordering or a constructor `Comparator` chooses the branch. [[What is the time complexity of lookup by key in a TreeMap]] is the guaranteed log(n) that a balanced BST gives. [[Compare HashMap and TreeMap tradeoffs]] is when you want that order.

`TreeSet` is a `NavigableSet` backed by a `TreeMap` whose values are a dummy, the same idea as `HashSet` on `HashMap`. [[Which tree data structure backs Java TreeSet]] is that set.

## What this is not

It is not a B-tree, AVL tree, or heap. It is not `HashMap`’s array of bins. Java 8+ `HashMap` may turn **one crowded bucket** into `TreeNode`s that are also red-black; that is a collision backstop inside a hash table, not “`HashMap` became a `TreeMap`.” [[How does HashMap handle collisions]] is that bin. [[What is the internal structure of HashMap]] is the array.

`SortedMap` / `NavigableMap` are interfaces. `TreeMap` is the red-black implementation in `java.util`. Concurrent navigable maps are a different class.

> [!warning] “Balanced tree” is not enough on an interview
> Name **red-black**. “Just a binary tree” misses the balance that makes log(n) a guarantee. “It hashes, then trees” describes `HashMap` tree bins, not `TreeMap`.

> [!tip] Interview answer
> **`TreeMap` is a red-black tree of key/value entries (`left` / `right` / `parent` / color), sorted by `Comparable` or `Comparator`. No buckets, no `hashCode` in the lookup path. That structure is why contains/get/put/remove are guaranteed log(n). `HashMap` is an array of bins; its trees, if any, are per-bucket.**
