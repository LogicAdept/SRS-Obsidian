<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Versions/8 #SRS

# Can `HashMap` degrade to a linked list when keys have different `hashCode`s?

> [!abstract] Short answer
> **Yes — same bucket, not same `hashCode`.** The index is `(n - 1) & mixedHash`. Only `log2(n)` bits of the mixed hash matter, so many distinct `hashCode()` values share a bin. That bin is a **list**, then Java 8+ may **treeify** it. The whole table becomes one list only if every key hashes to **one** index; resize and trees make that a short-lived or non-list shape.

## Bucket index ≠ `hashCode()`

`HashMap` javadoc: expected `get`/`put` are constant-time **if** hashes spread among buckets; many keys with the **same** `hashCode()` slow any hash table. The converse is false: **different** `hashCode()`s can still collide in one slot. [[When does a hashCode collision occur in a HashMap]] [[What is the internal structure of HashMap]]

OpenJDK 21 `hash(key)` is `0` for null, else `h ^ (h >>> 16)` with `h = key.hashCode()`. The bucket is `(table.length - 1) & hash`. Length is a power of two, so that is the low bits. Distinct `h` can yield the same mixed hash, or different mixed hashes that agree on those low bits. [[How does HashMap handle collisions]] [[What are hash collisions in HashMap bucket chains]]

```java
Map<Integer, String> map = new HashMap<>(16);
map.put(1, "a");
map.put(17, "b");
// Integer.hashCode is the int: 1 and 17 differ.
// hash = h ^ (h >>> 16) → 1 and 17.
// (16 - 1) & 1 == 1, (16 - 1) & 17 == 1 — one bin, a two-node list.
```

**Listing 1.** Different `hashCode()`, same bucket at capacity 16. Degeneration to a **list** is that chain, not “the whole map is `LinkedList`.”

```d2
direction: down
hc: "distinct hashCode() values" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
mix: "hash = h ^ (h >>> 16)" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
idx: "(n-1) & hash\nsame index possible" {
  width: 280
  height: 70
  style.fill: "#ffe0b2"
}
bin: "one bin: list, then tree if long" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}

hc -> mix
mix -> idx
idx -> bin
```

**Fig. 1.** The method that picks the bucket is the mix plus bitmask, not `hashCode()` alone.

If **every** key maps to one index, `putVal` grows that list. At 8 nodes `treeifyBin`: if the table is still shorter than 64 it **resizes** instead (`TREEIFY_THRESHOLD` 8, `MIN_TREEIFY_CAPACITY` 64); resize splits by `e.hash & oldCap` (the new bit). Keys whose mixed hashes differ in that bit **leave** the single chain. Keys whose mixed hashes are identical stay together even after growth — that is the “same `hashCode` after mix” case, which different raw `hashCode()`s can still produce. Java 8+ then treeifies a fat bin (`Comparable` keys get O(log n) in that bin). [[What happens to HashMap if all keys share the same hashCode]] [[What happens when two HashMap keys have the same hashCode but are not equal]]

> [!warning] “Different `hashCode` ⇒ different bucket” is false
> Interview answers that treat `hashCode()` as the index miss the mask and the mix. A small table makes collisions cheap. After Java 8 a long **bin** is not forever a linked list: it becomes a tree (or the table grows first). Do not say the entire `HashMap` “is a LinkedList” just because two keys share a slot.

> [!tip] Interview answer
> **Yes. Distinct `hashCode()`s can still land in one bucket because the index uses only the low bits of a mixed hash. That bin is a list of nodes. The whole map is one list only while every key shares that index; resize can split the chain, and Java 8+ may treeify a long bin. Same `hashCode()` is sufficient for a bad bin, not necessary.**
