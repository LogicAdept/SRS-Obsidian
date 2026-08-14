<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #DSA/Complexity #Java/Versions/8 #SRS

# What is the worst case time complexity of `get` on a `HashMap` when the key is present?

> [!abstract] Short answer
> **Linear in the map size, Θ(n), when every mapping sits in one linked bin and the match is the last node.** A hit can stop as soon as identity or `equals` succeeds, so the first node is O(1). The worst present key is the one you only recognize after walking the whole chain. Java 8+ may make that bin O(log n) if hashes differ or the keys are `Comparable`; that is implementation, not a new javadoc guarantee.

## A hit still searches one bin

`get` is `getNode` then `.value`. Mix `hashCode()`, index `(n - 1) & hash`, then test that slot. The first node is always checked. A later match is a `do`/`while` on `next`. [[Is equals invoked when a HashMap bucket contains a single element]] is that first-node test. [[What is the worst case time complexity of get on a HashMap when the key is absent]] is the same walk when nothing matches: a miss cannot stop early.

```java
if (first.hash == hash &&
        (key == first.key || key.equals(first.key)))
    return first;           // best-case hit
do {
    if (e.hash == hash &&
            (key == e.key || key.equals(e.key)))
        return e;           // hit at this node
} while ((e = e.next) != null);
```

**Listing 1.** Conceptual `getNode` (OpenJDK, Java 8+). Presence does not skip the chain. It only lets you return before `next == null`.

```d2
direction: down
idx: "Index one bucket" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
first: "First node matches\nhit O(1)" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
list: "Match is last of k\nhit Θ(k)" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
tree: "Tree bin" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
log: "O(log k) if hashes differ\nor keys Comparable" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

idx -> first
idx -> list
idx -> tree -> log
```

**Fig. 1.** Worst-case present `get` is “the equal key is at the end of this bin,” not a scan of every bucket. `containsValue` is the full-table search.

If all `n` keys share one list, k = n. Finding the last key is Θ(n). Resize does not split identical mixed hashes. [[What happens to HashMap if all keys share the same hashCode]] is that table. Pre-Java 8 that overloaded bin cannot be a tree.

## Java 8+ log n is conditional

A crowded bin may treeify after the usual count and capacity-64 gates. OpenJDK states worst-case O(log n) when keys have **distinct hashes** or are **orderable**. JEP 180 targeted `Comparable` keys and did not change the public spec. [[How does HashMap handle collisions]] and [[Does HashMap guarantee its documented lookup time complexity]] are those limits.

Same hash and not `Comparable`: a tree `find` cannot branch on hash. A present key can still cost a large fraction of the bin, not a balanced log.

The documented **expected** `get` is constant-time if hashes disperse. Typical hits then inspect one node or a short chain. [[How many linked nodes are visited on average for HashMap get with an existing key]] is that average. [[What is the algorithmic complexity of HashMap operations]] is the class-level wording.

> [!warning] “It is present, so O(1)”
> Presence only means the walk **may** stop. Worst case is still last in a colliding list. A first-node hit is cheap; that is best case, not worst case. “Java 8 made `get` O(log n)” is the same overclaim as on a miss: trees are optional, and the log bound needs distinct hashes or `Comparable`.

> [!tip] Interview answer
> **Worst-case present `get` is Θ(n): one linked bin holds every entry, and the equal key is last. A first-node hit is O(1). Java 8+ can treeify that bin; then a hit can be O(log n) if hashes differ or keys are `Comparable`. The javadoc never promised a worst-case bound, only expected constant time when hashes spread.**
