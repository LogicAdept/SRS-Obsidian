<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Versions/8 #SRS

# How many steps does `HashMap.get` take when the key is present?

> [!abstract] Short answer
> **There is no fixed “1 or 4 hops.”** `get` hashes, picks a bucket, then walks that bin until a matching node. If the key is the **first** node, that is one comparison and you return. Collisions add `next` hops; a tree bin is logarithmic. Expected time is constant if hashes spread. `getForNullKey()` is a **Java 7** helper, not today’s `get`.

## What `get` actually does

Java SE 21 `get` is `getNode(key)` then `e.value`. `getNode` (OpenJDK 21): mix `hash(key)` (`null` → 0, else `hashCode() ^ (h >>> 16)`), index `(n - 1) & hash`, read `table[i]`. **Always** test the first node (`hash` then `==` then `equals`). If that is the mapping, return. If `first.next != null`, either `getTreeNode` or a `do/while` on the chain. [[What is the internal structure of HashMap]] [[Is equals invoked when a HashMap bucket contains a single element]]

```d2
direction: down
get: "get(key)  [key is in the map]" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
hash: "hash(key) → bucket" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
first: "first node matches?" {
  width: 240
  height: 50
  style.fill: "#ffe0b2"
}
done: "return value" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
walk: "chain next… or tree" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}

get -> hash
hash -> first
first -> done: yes
first -> walk: no
walk -> done
```

**Fig. 1.** Present key: you still pay hash + bucket. Node visits depend on **where in the bin** it sits, not a universal “4 transitions.”

Dump “4”: compute hash, index, find value, return — a **sketch of the method**, not a count of pointer hops. The find step is 1..length-of-bin (or tree depth). [[How does HashMap handle collisions]] [[When does a hashCode collision occur in a HashMap]]

OpenJDK’s Poisson model at load 0.75: most bins have 0 or 1 node (~60% empty, ~30% one node). For a key that **is** in the table, you often hit it on the first node of its bin. Longer chains are rare if hashes spread; they are not rare if every key shares a `hashCode`. [[How many linked nodes are visited on average for HashMap get with an existing key]] [[What happens to HashMap if all keys share the same hashCode]]

```java
// OpenJDK 21 — conceptual
public V get(Object key) {
    Node<K,V> e = getNode(key);
    return e == null ? null : e.value;
}
// hash(key) includes: key == null ? 0 : hashCode() ^ (h >>> 16)
```

**Listing 1.** Conceptual: one public `get`, one `getNode`. Null keys use the same path (hash 0), not a public `getForNullKey`.

Java 7 `get` branched `if (key == null) return getForNullKey();`. That helper walked **`table[0]`** until `e.key == null`. Other keys can live in bucket 0, so even a present null key was **not** “always one step.” Java 8 dropped the helper. Worst case today: O(n) on a list bin, or better if the bin was treeified (`Comparable` keys). [[What is the worst case time complexity of get on a HashMap when the key is present]]

> [!warning] “1 for null, 4 otherwise” is a Java 7 dump, not a hop count
> `getForNullKey` is gone. Null is `hash == 0` and the same first-node / chain / tree walk. A present non-null key is **not** four transitions: if it is first in the bin you compare that node and return; if not, you follow `next` (or the tree). Counting bytecode steps in an old listing is not the interview answer. Javadoc: expected constant time **if** the hash spreads.

> [!tip] Interview answer
> **When the key is present, `get` hashes, indexes the bucket, and compares nodes until `==` or `equals` hits. That is often one node if hashes spread; collisions add hops; Java 8+ may tree-search a fat bin. There is no fixed 1-or-4. Null uses the same path (hash 0). Java 7’s `getForNullKey` is history.**
