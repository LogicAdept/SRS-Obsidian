<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #SRS

# How does `HashMap` access elements internally?

> [!abstract] Short answer
> **`get` and `containsKey` both call `getNode`.** Mix the key’s `hashCode`, index one bucket with `(n - 1) & hash`, test that bin’s first node, then walk `next` or a tree. A hit is stored hash plus identity or `equals`. `get` returns the node’s value or `null`; `containsKey` is “node exists,” so a mapping to `null` is not a miss.

## From `get` to one bucket

```java
public V get(Object key) {
    Node<K,V> e;
    return (e = getNode(key)) == null ? null : e.value;
}
```

**Listing 1.** OpenJDK `get` (Java 21). `getOrDefault` is the same search with a fallback. `containsKey` is `getNode(key) != null`.

The `Map` contract: return `v` iff there is a key `k` with `Objects.equals(lookup, k)`. `HashMap`’s javadoc also warns that `get` returning `null` can mean “no mapping” or “mapped to `null`.”

```d2
direction: down
mix: "hash(key)\nnull → 0, else hashCode ^ >>> 16" {
  width: 320
  height: 80
  style.fill: "#e3f2fd"
}
idx: "first = table[(n-1) & hash]" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
miss: "table null / empty / slot null\n→ miss" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
first: "first.hash == hash\nand == or equals?" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
hit: "return that node" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
rest: "first.next != null?" {
  width: 240
  height: 60
  style.fill: "#ffe0b2"
}
tree: "TreeNode\ngetTreeNode → find" {
  width: 240
  height: 70
  style.fill: "#ffe0b2"
}
list: "walk e = e.next\nsame hash / == / equals" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}

mix -> idx
idx -> miss
idx -> first
first -> hit: yes
first -> rest: no
rest -> tree: first is TreeNode
rest -> list: list bin
```

**Fig. 1.** One mix, one slot, first node always, then list or tree. Empty table or empty slot is an immediate miss.

`hash` XORs high bits downward so a power-of-two mask does not ignore them. Layout of `table` and `Node`: [[What is the internal structure of HashMap]]. High-level picture: [[What is java.util.HashMap at a high level]].

## What “found” means in the bin

The first node is always checked, even if the bin later turns out to be a tree (OpenJDK comment: “always check first node”):

```java
if (first.hash == hash &&
        ((k = first.key) == key || (key != null && key.equals(k))))
    return first;
```

**Listing 2.** Conceptual first-node test from `getNode`. `equals` runs only if hashes match, references differ, and the lookup key is non-null.

If that fails and `first.next != null`:

* a `TreeNode` head delegates to `getTreeNode` → `find` on the tree root;
* otherwise a `do/while` walks `next` with the same hash / `==` / `equals` test.

A matching **stored hash** is required before `equals`. Two keys can share a bucket with different hashes; that walk can skip `equals`. [[When does a hashCode collision occur in a HashMap]] vs a mere index collision. One-node bins still use this test: [[Is equals invoked when a HashMap bucket contains a single element]]. Collision structure: [[How does HashMap handle collisions]].

The `null` key is mixed to `0` and compared only by identity in this method (`key != null && key.equals(k)`), which is the `null`-safe form of the documented `key==null ? k==null : key.equals(k)`.

> [!warning] `get` is not LinkedHashMap “access”
> `HashMap.afterNodeAccess` is empty. A successful `get` does **not** move the entry. Access-order LRU behavior is [[What are LinkedHashMap ordering guarantees]], and only when that map is constructed with access order. Another trap: `get` → `null` is not “absent” if you stored a null value — use `containsKey`.

> [!tip] Interview answer
> **Access is `getNode`: mix `hashCode`, mask to one bucket, test the first node, then walk the list or the tree. A hit needs the stored hash and then `==` or `equals`. `get` returns the value or `null`; `containsKey` tells those two `null`s apart. `HashMap` does not reorder on get.**
