<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Versions/8 #SRS

# What is the internal structure of `HashMap`?

> [!abstract] Short answer
> **An array of bins.** Each slot is empty, a linked list of `Node`s, or (Java 8+) a red-black tree of `TreeNode`s. A node holds the mixed hash, the key, the value, and `next`. The table length is a power of two; the bin index is `(n - 1) & hash`. Capacity is that array length, not the number of mappings.

## The table is an array of bin heads

The public javadoc calls capacity **the number of buckets**. OpenJDK stores those buckets in `transient Node<K,V>[] table`. The array is created on first use, not in the no-arg constructor. Once allocated, `table.length` is always a power of two. The default initial capacity is 16. The documented maximum is `1 << 30`.

A slot holds the **first** node of that bin, or `null`. There is no second array of entries. Iteration cost is capacity plus size because empty slots are still visited.

```d2
direction: down
table: "table[]\npower-of-two length" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
empty: "null\nempty bin" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
list: "Node → Node → …\nplain bin" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
tree: "TreeNode\nred-black bin (Java 8+)" {
  width: 260
  height: 80
  style.fill: "#ffe0b2"
}

table -> empty
table -> list
table -> tree
```

**Fig. 1.** One array. Each index is a bin: empty, a `next` chain, or a tree whose nodes still form a `next` traversal order.

## What a `Node` stores

```java
static class Node<K,V> implements Map.Entry<K,V> {
    final int hash;
    final K key;
    V value;
    Node<K,V> next;
}
```

**Listing 1.** OpenJDK bin node. `hash` and `key` are fixed at construction; `value` and `next` can change.

`hash` is **not** the raw `hashCode()`. For a non-null key the implementation mixes high bits downward, then keeps that mixed `int` on the node. The `null` key uses mixed hash `0` and lives in the bin that index `0` selects. Lookup recomputes the mix from the key’s **current** `hashCode()` and matches it against the stored field before `equals`. That is why mutating a key after `put` can hide the node: [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]].

```java
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
int index = (n - 1) & hash;
```

**Listing 2.** Conceptual mix and index. `n` is `table.length`. Power-of-two length makes `& (n - 1)` a mask, not a `%`.

Two keys can share a bin without sharing `hashCode()`; [[When does a hashCode collision occur in a HashMap]] splits those events. The first-node checks are [[Is equals invoked when a HashMap bucket contains a single element]].

## Java 8+: a crowded bin can be a tree

A normal bin is `Node` objects linked by `next`. When a list bin is already long enough and the table is large enough, OpenJDK replaces those nodes with `TreeNode`s (red-black links plus the same `hash` / `key` / `value` / `next`). Tree bins are ordered primarily by the stored hash; on a tie, `Comparable` keys of the same class may use `compareTo`. [[How does HashMap handle collisions]] is the conversion rule (`TREEIFY_THRESHOLD` 8, `MIN_TREEIFY_CAPACITY` 64, `UNTREEIFY_THRESHOLD` 6).

JEP 180 changed only the implementation. The public `Map` contract still does not mention trees. `Hashtable` and `WeakHashMap` did not get tree bins. Iteration order of `HashMap` stays unspecified and can change when a bin becomes a tree.

> [!warning] Capacity is not `size()`
> Capacity is bucket count. `size()` is mapping count. Load factor (default 0.75) times current capacity is the resize threshold. When `size` exceeds that product, the table is rebuilt with about twice as many buckets. [[How and when does HashMap resize its buckets]] and [[What are the initial capacity and load factor parameters of HashMap]] are that growth.

> [!tip] Interview answer
> **`HashMap` is a power-of-two array of bins. Each bin is empty, a linked list of nodes, or (Java 8+) a red-black tree. A node stores the mixed hash, the key, the value, and `next`. The bucket is `(n - 1) & hash`; equality still decides which node is the mapping. Capacity is the array length, not the number of entries.**
