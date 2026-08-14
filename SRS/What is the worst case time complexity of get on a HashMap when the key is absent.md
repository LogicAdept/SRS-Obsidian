<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #DSA/Complexity #Java/Versions/8 #SRS

# What is the worst case time complexity of `get` on a `HashMap` when the key is absent?

> [!abstract] Short answer
> **Linear in the map size, Θ(n), when every mapping sits in the looked-up bucket as a linked list and none equals the key.** Absence is proven only after that bin is exhausted. An empty bucket is a constant-time miss. In Java 8+ a tree bin can make the miss O(log n) **if** hashes differ or the keys are `Comparable`; that is an implementation bound, not a new public guarantee. The javadoc still only promises constant-time `get` when hashes disperse.

## A miss still opens one bucket

`get` (and `containsKey`) call the same node search. Mix `hashCode()`, index with `(n - 1) & hash`, then inspect that slot. [[Is equals invoked when a HashMap bucket contains a single element]] is the first-node checks. If the slot is empty, the method returns `null` immediately: best-case miss.

If the slot is occupied, a miss cannot return early on “not the first node.” A later node might still match.

```java
// list bin: keep walking until next == null
if (e.hash == hash &&
        (key == e.key || key.equals(e.key))) {
    return e; // hit
}
// else continue; hash mismatch only skips equals
```

**Listing 1.** Conceptual loop from `getNode` (Java 8+). For an absent key the loop runs to the end of the chain. Different stored hashes in the same bucket still cost a visit each; they just avoid `equals`.

```d2
direction: down
idx: "Index one bucket" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
empty: "Slot null\nmiss O(1)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
list: "Linked bin of k nodes" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
tree: "Tree bin" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
scan: "Walk all k nodes\nthen miss Θ(k)" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
log: "O(log k) if hashes differ\nor keys Comparable" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
lin: "Same hash, not Comparable\nmay still visit the bin" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}

idx -> empty
idx -> list -> scan
idx -> tree
tree -> log
tree -> lin
```

**Fig. 1.** Worst-case absent `get` is “scan this bin and fail,” not “scan the whole table.” The table walk is `containsValue`, not `get`.

When all `n` keys collide in that one list, k = n and the miss is Θ(n). Resize does not split identical mixed hashes. [[What happens to HashMap if all keys share the same hashCode]] is that table. Pre-Java 8 there is no tree bin, so that is the only overloaded-bin shape.

## Java 8+ does not make every miss logarithmic

A crowded bin may become a red-black tree after the usual thresholds (enough nodes, table capacity at least 64). OpenJDK states worst-case O(log n) **when keys have distinct hashes or are orderable.** JEP 180 aimed at O(log n) for `Comparable` keys and did not change the `HashMap` specification. [[How does HashMap handle collisions]] and [[Does HashMap guarantee its documented lookup time complexity]] are those caveats.

On a hash tie without `Comparable`, tree `find` cannot branch on hash and may search both children. A miss of a non-comparable, same-hash key can still visit much of that bin.

> [!warning] Absence is not cheaper than a hit
> A common guess is that a missing key is O(1) because “there is nothing to return.” An empty bucket is cheap. A full colliding bucket is **more** work than a hit that matches the first node: the miss must prove every candidate failed. Another false answer is “since Java 8 worst-case `get` is O(log n), always.” Treeification needs capacity and count, and the log bound needs distinct hashes or `Comparable`.

The documented expected case remains constant-time `get` when hashes spread keys. [[What is the algorithmic complexity of HashMap operations]] and [[How many linked nodes are visited on average for HashMap get with an existing key]] are that side. A miss in a well-spread table is still typically one empty slot or a handful of nodes.

> [!tip] Interview answer
> **Worst-case absent `get` is Θ(n): every entry is in the target bucket’s linked list, none equals the key, and the search walks the whole chain. An empty bucket is O(1). Java 8+ may treeify that bin and then a miss can be O(log n) if hashes differ or keys are `Comparable`; otherwise even a tree miss can stay linear in the bin. The public javadoc never guaranteed a worst-case bound.**
