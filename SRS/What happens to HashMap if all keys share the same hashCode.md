<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Versions/8 #SRS

# What happens to `HashMap` if all keys share the same `hashCode`?

> [!abstract] Short answer
> The map stays **correct** and becomes **slow**. Every key hashes to the same mixed value, so every entry sits in one bucket. `equals` still distinguishes unequal keys, so `size` grows and `get` still finds them. Resize cannot spread that bin: the new bit is identical for every node. Lookup and insert then walk one list (Java 7 and earlier, or a small table) or one tree bin (Java 8+, after the usual thresholds). Tree lookup is O(log n) in that bin only when the keys are `Comparable`.

## One bucket, still a map

A constant `hashCode()` is legal. Unequal objects are not required to differ; see [[Why can two unequal objects share the same hashCode value]] and [[How would you explain the hashCode method contract in Java]]. `HashMap` still rejects a second **equal** key. [[When does a hashCode collision occur in a HashMap]] is this situation at full scale: every pair of unequal keys collides.

```java
final class K {
    final int id;
    K(int id) { this.id = id; }

    @Override
    public boolean equals(Object o) {
        return o instanceof K other && id == other.id;
    }

    @Override
    public int hashCode() {
        return 1;
    }
}
```

**Listing 1.** Conceptual key type. Twenty `new K(i)` values are twenty mappings, not one overwrite. [[Can a HashMap contain two equal keys at the same time]] is the equal-`id` case.

```d2
direction: down
keys: "All keys\nhashCode() == 1" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
mix: "Same mixed Node.hash\nsame index for every n" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
bin: "Single occupied bucket" {
  width: 260
  height: 70
  style.fill: "#ffe0b2"
}
list: "Linked Node chain" {
  width: 240
  height: 70
  style.fill: "#ffe0b2"
}
tree: "Java 8+ TreeNode\nif count and capacity allow" {
  width: 280
  height: 80
  style.fill: "#ffe0b2"
}
empty: "Other buckets stay empty\n(resize still allocates them)" {
  width: 300
  height: 80
  style.fill: "#eceff1"
}

keys -> mix -> bin
bin -> list
list -> tree
bin -> empty
```

**Fig. 1.** Identical hashes collapse the table to one live bin. Empty slots still exist after growth; they just never receive these keys.

## Why resize does not save you

Power-of-two growth splits a chain by `e.hash & oldCap`. If every stored hash is equal, that bit is equal, so the whole chain stays together (same index, or all move by `oldCap`). Load-factor resizes still run: `size > threshold` doubles capacity and iteration pays for the extra empty buckets. The live bin does not get shorter.

Java 8+ `treeifyBin` also resizes when `table.length < 64` instead of converting. With one overloaded bin that still does not scatter keys; it only delays treeification until capacity is at least 64. Then a bin of at least 8 nodes can become a red-black tree. [[How does HashMap handle collisions]] is the general mechanism.

The documented `get`/`put` complexity is constant time **assuming** hashes disperse among buckets. Many keys with the same `hashCode()` are called out as a sure way to slow any hash table. [[Does HashMap guarantee its documented lookup time complexity]] is that assumption. Iteration remains proportional to capacity plus size, so a bloated empty table plus one huge bin is extra-linear in wasted capacity.

## `Comparable` is the mitigation, not a given

After treeification, nodes are ordered first by stored hash. With a total hash tie, keys of the form `class C implements Comparable<C>` may be ordered by `compareTo`, which is what the `HashMap` API describes as breaking ties. OpenJDK then gives worst-case O(log n) in that bin. If the keys are **not** `Comparable`, a tree `find` cannot branch on hash and may walk much of the bin; the implementation notes treat that as a poor `hashCode`, not a repaired table.

> [!warning] The map does not “lose” the keys
> A constant `hashCode` is not the same bug as mutating a key after `put`. Entries remain reachable through `equals`. The usual false answers are: “later `put` overwrites everything,” “Java 8 makes it O(1) or always O(log n),” “rehash spreads identical hashes,” and “it becomes `java.util.LinkedList`.” Pre-Java 8 there is no tree bin at all, so that one bucket is a list of length `n`. Unique hashes are not required; the map **works**, it is just slow.

> [!tip] Interview answer
> **Yes, it still works. If every key returns the same `hashCode()`, `HashMap` keeps all unequal mappings in a single bucket. It still uses `equals`, so nothing is overwritten by accident. Resize cannot split that bin. Operations become linear in the map size unless Java 8+ treeifies the bin and the keys are `Comparable`, in which case that bin can be logarithmic. The public contract never promised constant time for this hash.**

