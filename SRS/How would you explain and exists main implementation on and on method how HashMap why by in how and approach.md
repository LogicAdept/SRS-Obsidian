<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/IdentityHashMap #DSA/Algorithms/Hashing #Java/Versions/8 #SRS

# How is `HashMap` implemented — chaining or open addressing — and why?

> [!abstract] Short answer
> **Separate chaining, then trees.** Each bucket is a list of `Node`s (`next` links). A collision **adds another node in that bin**, it does not walk empty table slots. Java 8+ may turn a long bin into a tree. Open addressing (linear probe) is what `IdentityHashMap` uses, not `HashMap`. Chaining lets the table grow with a 0.75 load factor, unlink on `remove`, and degrade to a tree instead of a probe sequence.

## Two hash-table families; `HashMap` is the chained one

A hash table maps a hash to a slot. When two keys land together you either **chain** (store several entries in that slot) or **open-address** (probe later slots in the same array). `HashMap` javadoc: an array of **buckets**; expected `get`/`put` are constant-time if hashes spread; many identical `hashCode()`s slow any hash table. OpenJDK: “this map usually acts as a **binned (bucketed)** hash table”; overpopulated bins become `TreeNode`s. [[What is the internal structure of HashMap]] [[How does HashMap handle collisions]]

`IdentityHashMap`’s implementation note is the JDK naming the other family: a **linear-probe** table (Sedgewick / Knuth), interleaved keys and values, “better performance than `HashMap`, which uses **chaining** rather than linear-probing” for many JREs and mixes. [[How does IdentityHashMap resolve collisions]] [[Why can IdentityHashMap be faster than HashMap]]

```d2
direction: down
collision: "two keys, same slot" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
chain: "chaining\nHashMap: list / tree in the bin" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
open: "open addressing\nIdentityHashMap: linear probe" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}

collision -> chain
collision -> open
```

**Fig. 1.** Same collision problem. `HashMap` hangs extra nodes off the bucket. `IdentityHashMap` searches the next array slots.

```java
// HashMap bin (OpenJDK 21): chain, then maybe a tree
static class Node<K,V> implements Map.Entry<K,V> {
    final int hash;
    final K key;
    V value;
    Node<K,V> next;
}
```

**Listing 1.** Conceptual: collision fields only (`Node` also implements `Map.Entry`). A collision is another `Node` on `next`, or `putTreeVal` if the head is already a `TreeNode`. `putVal` links a new node on the **tail** of a list bin. That is chaining, not probing.

## Why chaining for a general-purpose `HashMap`

Default **load factor 0.75**: resize when `size` exceeds capacity × load factor. OpenJDK models bin lengths as roughly Poisson with mean ~0.5 at that threshold — most bins have 0–1 nodes. Chaining *can* theoretically hold more entries than buckets (λ > 1). **`HashMap` does not run that way**: it grows the table so average chains stay short. If a bin still explodes (bad or identical hashes), Java 8+ **treeifies** at 8 nodes when the table is at least 64; otherwise it resizes first. Worst case becomes O(log n) when keys are `Comparable`, not an unbounded probe run. [[What are the initial capacity and load factor parameters of HashMap]] [[What happens to HashMap if all keys share the same hashCode]]

`remove` unlinks: replace the bucket head or `p.next = node.next` (trees have `removeTreeNode`). No Knuth-style “close the hole.”

Open addressing in the JDK (`IdentityHashMap`): at least one **null** slot must remain or `get`/`put`/`remove` loop forever (`MAXIMUM_CAPACITY - 1` entries). After delete it runs **`closeDeletion`** — “adapted from Knuth Section 6.4 Algorithm R” — to slide later colliding keys so a `null` still means “stop probing.” That is the deletion cost textbooks warn about. Iteration walks **bucket count**, not size. Linear probe packs keys in one array (no `Node` object per entry) — the locality win the javadoc cites.

`HashMap` is the general `equals`/`hashCode` map, allows a null key, and must stay usable when hashes clump. Chaining plus trees and a 0.75 resize fits that. Linear probe is reserved for the identity table that can skip `equals` and pack slots. [[What is the difference between HashMap and IdentityHashMap]]

> [!warning] Not “just a linked list,” and not `IdentityHashMap`’s table
> Pre-Java 8 interview answers stop at “array of lists.” After 8, a **long** bin is a tree (and tree bins are about twice a plain `Node`). Do not call `HashMap` open addressing, linear/quadratic probe, or double hashing. Do not say chaining “always allows load factor > 1” as if that were `HashMap`’s policy — it resizes at 0.75. Dump talk of primary/secondary clustering describes **probe** sequences, not `HashMap` bins. [[What are hash collisions in HashMap bucket chains]] [[When does a hashCode collision occur in a HashMap]]

> [!tip] Interview answer
> **`HashMap` uses separate chaining: each bucket is a list of nodes, treeified when a bin gets long. Collisions stay in that bucket; they do not probe the next slots. The JDK’s linear-probe map is `IdentityHashMap`. Chaining plus a 0.75 load factor keeps typical bins tiny, `remove` is an unlink, and trees cap the disaster if every key collides. Open addressing packs better in one array but needs a hole to stop probes and extra work to delete.**
