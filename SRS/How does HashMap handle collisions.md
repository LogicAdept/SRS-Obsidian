<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/Hashtable #Java/HashCodeEquals #Java/Versions/8 #SRS

# How does `HashMap` handle collisions?

> [!abstract] Short answer
> It uses **separate chaining**. An occupied bucket becomes a linked list of nodes. `put` appends a new node only when the stored hash matches and identity/`equals` still say the keys differ; equal keys replace the value. In Java 8+, a crowded bin can become a red-black tree, but only after both a count threshold and a minimum table capacity. Tree lookup is O(log n) when hashes differ or the keys are `Comparable`; that is not a blanket worst-case guarantee.

## First: find the bin, then the key

`HashMap` mixes `hashCode()` and indexes with `(n - 1) & hash`. Two unequal keys in that slot are a collision; [[When does a hashCode collision occur in a HashMap]] separates that from a mere shared index. The map never treats a matching hash as “same key.”

```d2
direction: down
idx: "(n-1) & mixed hash" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
empty: "Empty slot\nstore one Node" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
hit: "Same hash and equals\nreplace value" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
chain: "Collision\nlink another Node" {
  width: 260
  height: 80
  style.fill: "#ffe0b2"
}
tree: "Java 8+ crowded bin\nmaybe TreeNode" {
  width: 260
  height: 80
  style.fill: "#ffe0b2"
}

idx -> empty
idx -> hit
idx -> chain
chain -> tree
```

**Fig. 1.** Collision handling is chaining, then optional treeification. Overwrite happens only on key equality.

```java
if (node.hash == hash &&
        (key == node.key || key.equals(node.key))) {
    // existing mapping
} else {
    // walk next (or the tree); append if no equal key
}
```

**Listing 1.** Conceptual Java 8+ test from `putVal` / `getNode`. See [[Is equals invoked when a HashMap bucket contains a single element]] and [[Can a HashMap contain two equal keys at the same time]].

The public contract still claims constant-time `get`/`put` only **assuming** hashes disperse among buckets. Many keys with the same `hashCode()` slow any hash table. [[What is the algorithmic complexity of HashMap operations]] is that caveat.

## Java 8+: list, then maybe a tree

A normal bin is `Node` objects linked by `next`. The implementation converts when **adding** to a list bin that already has at least `TREEIFY_THRESHOLD` (8) nodes — that is, `treeifyBin` runs as the **9th** node is linked (`binCount >= 7`):

```java
static final int TREEIFY_THRESHOLD = 8;
static final int UNTREEIFY_THRESHOLD = 6;
static final int MIN_TREEIFY_CAPACITY = 64;
```

**Listing 2.** Java 8+ thresholds from the OpenJDK implementation. `putVal` uses `binCount >= TREEIFY_THRESHOLD - 1` because `binCount` starts at 0 on the first successor.

If `table.length < 64`, `treeifyBin` **resizes instead of converting**. Only when the table is already large enough does it replace the list with `TreeNode`s and build a red-black tree. After a split or removal, a small tree bin can be turned back into a list once it has at most 6 nodes. [[Can HashMap degrade to a linked list when keys have different hashCodes]] is why a chain can exist even when `hashCode()` values differ.

Tree bins are ordered **primarily by the stored hash**. On a hash tie, if both keys have the form `class C implements Comparable<C>`, `compareTo` breaks the tie. Otherwise insertion uses a consistent stand-in (class name, then `identityHashCode`). The API documents only the `Comparable` case: the class **may** use comparison order to help break ties.

> [!warning] Tree bins are not “always O(log n)”
> OpenJDK states worst-case O(log n) when keys have **distinct hashes** or are **orderable**. If many keys share a `hashCode()` and are not `Comparable`, a tree lookup may still walk much of that bin. Interview answers that stop at “Java 8 replaced lists with trees, so collisions are log n” skip both the capacity-64 gate and this `Comparable` condition. [[What happens to HashMap if all keys share the same hashCode]] is the degenerate bin.

`Hashtable` did not receive this tree-bin change; Java 8 applied it to `HashMap`, `LinkedHashMap`, and `ConcurrentHashMap`. Iteration order of `HashMap` is unspecified and can change when bins become trees. [[What is the difference between HashMap and Hashtable]] is the legacy map that still chains.

> [!tip] Interview answer
> **`HashMap` resolves collisions by chaining: the bucket holds a list of nodes, and `equals` decides replace versus append. Java 8+ can convert a bin into a red-black tree when you add to a list that already has at least 8 nodes, but only if the table capacity is at least 64; a smaller table resizes first. Tree lookup is O(log n) when hashes differ or keys are `Comparable`, not in every collision scenario.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что поменялось в HashMap с Java 8?**

При 8 элементах в бакете и размере таблицы ≥ 64 список превращается в red-black tree. Поиск становится O(log n) вместо O(n) в худшем случае.
