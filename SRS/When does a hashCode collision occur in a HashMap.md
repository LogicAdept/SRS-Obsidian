<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #SRS

# When does a `hashCode` collision occur in a `HashMap`?

> [!abstract] Short answer
> When two **unequal** keys return the same `hashCode()`. `HashMap` mixes that integer and stores it on the node; equal mixed hashes pick the same bucket for every table length. The map then tells the keys apart with identity or `equals`. Sharing a bucket is not the same event: different `hashCode` values can still land in one bin, and a later resize can split them.

## Two events people mix up

```d2
direction: down
keys: "Two unequal keys" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
sameHc: "Same hashCode()?" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
hc: "hashCode collision\nsame stored Node.hash\nsame bucket at every n" {
  width: 300
  height: 100
  style.fill: "#ffe0b2"
}
bucket: "Maybe only a bucket collision\nsame index now\nresize may split" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}

keys -> sameHc
sameHc -> hc: yes
sameHc -> bucket: no, but\n(n-1) & hash equal
```

**Fig. 1.** A `hashCode` collision is equal `hashCode()` values on unequal keys. A bucket collision is a shared index and is a larger set.

[[Why can two unequal objects share the same hashCode value]] is why the first case is legal. [[Can HashMap degrade to a linked list when keys have different hashCodes]] is the second case.

## How `HashMap` uses the integer

For a non-null key the implementation mixes `hashCode()` and then masks with the current table length. The default table length is a power of two, initially 16.

```java
int hash = key.hashCode() ^ (key.hashCode() >>> 16); // stored on the node
int index = (n - 1) & hash;                          // bucket
```

**Listing 1.** Conceptual Java 8+ index path. `n` is `table.length`. The `null` key is stored with mixed hash `0` and does not call `hashCode()`.

Same `hashCode()` therefore means same stored `Node.hash`, and `(n - 1) & hash` is the same for that `n`. Those two keys collide in the bin on every capacity. `"Aa"` and `"BB"` are a specified `String` example: both hash to `2112`, `equals` is false, and a map keeps both mappings.

Different `hashCode()` values can still share an index because only some bits survive the mask. In a table of length 16:

```text
mix(1)  = 1  →  1  & 15 = 1
mix(17) = 17 →  17 & 15 = 1
```

**Listing 2.** Same bucket, different stored hashes. This is not a `hashCode` collision.

On a power-of-two resize the implementation splits a chain by the new bit `e.hash & oldCap`. Keys with mixed hashes `1` and `17` separate when capacity goes from 16 to 32 (`17` moves by `oldCap`). Keys that share the full mixed hash cannot be split that way: the new bit is the same for both.

## Inside the bin it is not an overwrite

`get`/`put` still compare the stored hash, then `==`, then `equals`:

```java
if (node.hash == hash &&
        (key == node.key || key.equals(node.key))) {
    // same mapping: replace on put, return on get
}
```

**Listing 3.** Conceptual first-node test from `getNode` / `putVal` (Java 8+). See [[Is equals invoked when a HashMap bucket contains a single element]].

If `equals` is true, this is the **same** key: `put` replaces the value. [[Can a HashMap contain two equal keys at the same time]] forbids a second mapping. A `hashCode` collision is the other branch: hashes match, `equals` is false, so a second node is linked (or inserted in a tree bin). [[How does HashMap handle collisions]] is that chain.

> [!warning] Same bucket is not the same as same `hashCode`
> Saying “collision means two keys in one bucket” is true of hash tables in general and false as a definition of a **`hashCode` collision** in this map. `HashMap` can skip `equals` when `node.hash != hash` even though the keys share a bin. Another trap: treating a shared hash as “the second `put` overwrites.” It overwrites only when `equals` is true.

Many keys with the same `hashCode()` slow any hash table. Java 8+ may treeify a crowded bin once it has at least 8 nodes and the table capacity is at least 64; until then a crowded small table resizes instead. When keys are `Comparable`, comparison order may break ties. That is a performance mitigation, not a redefinition of collision. [[What happens to HashMap if all keys share the same hashCode]] is the all-in-one-bin extreme.

> [!tip] Interview answer
> **A `hashCode` collision in `HashMap` is two unequal keys with the same `hashCode()`. They get the same stored hash and therefore the same bucket at every capacity; `equals` still decides whether `put` replaces or appends. Two keys can also share a bucket with different hashes; that is only an index collision, and a power-of-two resize can separate them.**
