<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Versions/8 #SRS

# Can `HashMap` degrade to a linked list when keys have different `hashCodes`

> [!abstract] Short answer
> **Yes, a bucket can become a linked collision chain even when the keys have different `hashCode()` values.** Different hash values can still map to the same bucket index. In Java 8+, a sufficiently crowded bin can later be converted into a red-black tree, so a heavily colliding bucket does not necessarily remain a linked list.

## How different hashes reach the same bucket

`HashMap` does not use the entire `hashCode()` directly as the array index. It first spreads the hash and then derives the bucket index from the current table length.

```java
int hash = key.hashCode() ^ (key.hashCode() >>> 16);
int index = (n - 1) & hash;
```

**Listing 1.** Conceptual bucket-index calculation. Two different processed hash values can still produce the same `index`.

```d2
direction: down
hashA: "Key A\nhash A" {
  width: 240
  height: 80
}
hashB: "Key B\nhash B" {
  width: 240
  height: 80
}
bucket: "same bucket index" {
  width: 260
  height: 80
}
node1: "Node" {
  width: 180
  height: 70
}
node2: "Node" {
  width: 180
  height: 70
}
node3: "Node" {
  width: 180
  height: 70
}

hashA -> bucket
hashB -> bucket
bucket -> node1
node1 -> node2
node2 -> node3
```

**Fig. 1.** Different hashes can collide at the bucket-index level. The bucket can therefore contain a linked chain of nodes.

The important distinction is **different `hashCode()` values** versus **different bucket indexes**. A hash collision in the usual `equals` contract means equal hash values for different keys; a bucket collision can also happen when the hash values differ but the derived indexes are equal.

## What happens when the bucket gets crowded

In Java 8+, `HashMap` uses tree bins to avoid an arbitrarily long linked-list lookup path. The implementation defines a treeification threshold of `8`, but it also requires a minimum table capacity of `64` before converting a crowded bin to a tree.

```java
static final int TREEIFY_THRESHOLD = 8;
static final int MIN_TREEIFY_CAPACITY = 64;
```

**Listing 2.** The relevant Java 8+ `HashMap` thresholds for treeifying a crowded bin.

Conceptually, the process is:

```text
same bucket
    |
    v
linked nodes
    |
    +---- table too small ----> resize
    |
    +---- table large enough -> tree bin
```

**Fig. 2.** A crowded bin is not immediately treeified when the table is small; `HashMap` may resize first. Once the table is large enough, the bin can become a tree bin.

Tree bins are red-black trees. Their ordering uses the stored hash and, when necessary, additional key-comparison rules, so lookup in a heavily colliding bin can avoid the worst linear scan of a long linked chain.

> [!warning] Different hashes do not mean different buckets
> A common interview mistake is to say that two different `hashCode()` values cannot collide in a `HashMap`. They can still produce the same bucket index because the table uses a derived index rather than the complete hash value. Another mistake is to claim that a crowded bucket always stays a linked list in Java 8+; it can be treeified.

## Why this is not a permanent linked-list degradation

For a normal bin, entries are connected through each node's `next` reference. With enough collisions, Java 8+ can replace that structure with tree nodes. Thus the simplified mental model is:

```text
low collision load  -> Node -> Node -> Node
high collision load -> TreeNode / red-black tree
```

**Listing 3.** Simplified representation of the two bucket shapes used by modern `HashMap` bins.

This is why the precise answer to “does `HashMap` degrade to a linked list?” is **yes, a collision chain can be a linked list, but a heavily populated bin is not required to remain one**.

See also [[When does a hashCode collision occur in a HashMap]] and [[How does HashMap handle collisions]].

> [!tip] Interview answer
> **Yes. Different `hashCode()` values can still map to the same `HashMap` bucket, so that bucket can contain a linked collision chain. In Java 8+, once a bin becomes sufficiently crowded and the table is large enough, `HashMap` can convert it into a red-black tree, so severe collisions do not necessarily leave you with a long linked-list lookup.**
