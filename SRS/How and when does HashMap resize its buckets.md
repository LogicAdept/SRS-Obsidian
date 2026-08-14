<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Versions/8 #SRS

# How and when does `HashMap` resize its buckets?

> [!abstract] Short answer
> **When a new mapping makes `size` exceed `capacity × loadFactor`, the table is rebuilt with about twice as many buckets.** Overwriting a value does not count. The first `put` also allocates the array (it starts null). In Java 8+, a crowded bin on a table smaller than 64 buckets resizes instead of becoming a tree. Growth is power-of-two: each node keeps its index or moves by the old capacity, using one bit of the stored hash.

## When the javadoc says “rehash”

Capacity is bucket count. Load factor (default 0.75) is how full the table may get. When the number of mappings **exceeds** that product, `HashMap` rebuilds internal structures so the table has **approximately twice** the buckets. [[What is the internal structure of HashMap]] is that array. [[What are the initial capacity and load factor parameters of HashMap]] is how those two knobs are chosen. [[What rule governs when HashMap grows its number of buckets]] is the threshold sentence alone.

Defaults: capacity 16, load factor 0.75, so the first growth is after the 13th distinct key (OpenJDK `threshold` is 12; `++size > threshold`). Replacing the value for an existing key does not increment `size` and does not resize.

```d2
direction: down
put: "put of a new key" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
first: "table == null\nallocate (resize)" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
grow: "size > threshold\ndouble the table" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
tree: "Java 8+ crowded list\nand capacity < 64\nresize, do not treeify" {
  width: 280
  height: 100
  style.fill: "#ffe0b2"
}
same: "put that only replaces\nno resize" {
  width: 260
  height: 80
  style.fill: "#eeeeee"
}

put -> first
put -> grow
put -> tree
put -> same
```

**Fig. 1.** Three real resizes (first allocation, load-factor growth, small-table treeify path) and one non-event (overwrite).

## What OpenJDK actually runs

After a **new** mapping, `putVal` does `if (++size > threshold) resize()`. `threshold` is documented as the next size at which to resize (`capacity * loadFactor`). The no-arg constructor leaves `table` null and `threshold` 0; the first `put` calls `resize()` to allocate 16 buckets and set `threshold` to 12.

A specified initial capacity is rounded up to a power of two (`tableSizeFor`) and parked in `threshold` until that first allocation. `putAll` may double repeatedly before copying if the incoming map is already larger than the current threshold.

Java 8+ `treeifyBin` **resizes instead of converting** when `table.length < MIN_TREEIFY_CAPACITY` (64). That can grow the table because one bin is long, even if `size` has not yet passed the load-factor threshold. [[How does HashMap handle collisions]] is that gate.

If capacity is already `MAXIMUM_CAPACITY` (`1 << 30`), `resize` sets `threshold` to `Integer.MAX_VALUE` and returns the same array. [[How many buckets can a HashMap table hold]] is that ceiling.

## How a power-of-two doubling moves nodes

`resize` allocates `new Node[oldCap << 1]` and **reuses** existing nodes. It does not call `hashCode()` again. Because the new length is twice the old, each stored hash either keeps index `j` or goes to `j + oldCap`:

```java
if ((e.hash & oldCap) == 0) {
    // same index in the new table
} else {
    // index + oldCap
}
```

**Listing 1.** Conceptual split from OpenJDK `resize`. `oldCap` is a power of two, so that test is the one extra bit the new mask uses.

A singleton bin is placed with `e.hash & (newCap - 1)`. A tree bin is split by `TreeNode.split`. After a split, a small tree can become a list again (`UNTREEIFY_THRESHOLD` 6).

If every key shares the same mixed hash, that bit is the same for all of them, so the live chain **does not shorten**. Load-factor resizes still run; you just pay for extra empty buckets. [[What happens to HashMap if all keys share the same hashCode]] is that bin. A `put` that rehashes is not constant-time; [[What is the algorithmic complexity of HashMap operations]] is that exception.

> [!warning] Interview traps
> Resize is not “at 75% of `size()`.” It is `size` versus `capacity × loadFactor`. It is not every `put`. The implementation does not re-mix `hashCode()` on each node; it uses the hash stored at insertion. Java 8 does not treeify a 9-node bin on a 16-bucket table: it resizes first. Doubling does not scatter identical hashes.

> [!tip] Interview answer
> **`HashMap` resizes when a new mapping pushes `size` past `capacity × loadFactor` (defaults 16 and 0.75, so after 13 keys), and also to allocate the table on first `put`. Java 8+ may resize a small table instead of treeifying a crowded bin. Growth doubles a power-of-two array; each node stays or moves by the old capacity according to one bit of its stored hash. Overwrite does not resize; identical hashes do not split.**
