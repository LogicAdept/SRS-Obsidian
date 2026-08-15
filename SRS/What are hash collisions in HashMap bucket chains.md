<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Versions/8 #SRS

# What are hash collisions in `HashMap` bucket chains?

> [!abstract] Short answer
> **Two or more unequal keys sitting in the same bin, linked by `next`.** That happens when mixed hashes share an index — either the same `hashCode()`, or different hashes that still mask to one slot. The chain is not an overwrite list: `put` appends a node only after stored hash plus `==`/`equals` say “different key.” Java 8+ may replace a long chain with a tree; `next` still exists for iteration.

## A chain is the collision structure

One occupied bucket is either a single `Node` or a list `Node → Node → …`. A second mapping in that slot is a **bucket collision**. [[How does HashMap handle collisions]] is why OpenJDK uses chaining rather than open addressing. [[What is the internal structure of HashMap]] is `Node.hash` / `key` / `value` / `next`.

`Object.hashCode` does **not** require unequal objects to differ. Distinct results “may improve the performance of hash tables”; many equal hashes are called out on `HashMap` as a sure way to slow any table.

```d2
direction: down
idx: "same (n-1) & mixed hash" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
n1: "Node\nhash, key A" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
n2: "Node\nhash, key B" {
  width: 220
  height: 70
  style.fill: "#ffe0b2"
}
n3: "…" {
  width: 120
  height: 50
  style.fill: "#ffe0b2"
}

idx -> n1
n1 -> n2: next
n2 -> n3: next
```

**Fig. 1.** Collision chain: same bucket index, distinct keys, linked with `next`. Equal keys never share two nodes.

Two ways into that list:

```text
same hashCode()     → same stored Node.hash → same index at every capacity
different hashCode  → different Node.hash   → same index until a bit the mask dropped
                      becomes live on resize
```

**Listing 1.** A `hashCode` collision is the first line. An index-only collision is the second. [[When does a hashCode collision occur in a HashMap]] vs [[Can HashMap degrade to a linked list when keys have different hashCodes]].

`"Aa"` and `"BB"` both have `String.hashCode` 2112; `equals` is false; both stay in the map.

## How the chain is walked

`get`/`put` do not scan by `equals` alone. On each node: stored hash, then identity, then `equals`. If `node.hash != lookupHash`, that node is skipped even though it is in the chain. That is why an index collision is cheaper than a true `hashCode` collision: mismatched hashes fail before `equals`.

```java
for (;;) {
    if ((e = p.next) == null) {
        p.next = newNode(hash, key, value, null); // append: real collision
        break;
    }
    if (e.hash == hash &&
            (e.key == key || (key != null && key.equals(e.key))))
        break; // same key: replace, do not chain
    p = e;
}
```

**Listing 2.** Conceptual list branch of OpenJDK `putVal` (Java 21). Append is “collision.” Break-with-`e != null` is “same mapping.”

A power-of-two resize splits a chain by `e.hash & oldCap`. Index-only collisions can separate; identical mixed hashes cannot. All-identical `hashCode`: [[What happens to HashMap if all keys share the same hashCode]].

Java 8+ `treeifyBin` may turn a list of ≥8 into `TreeNode`s if capacity ≥ 64 (otherwise it resizes). Tree bins still thread `next` for `entrySet` iteration; lookup then uses the tree, not a linear `equals` scan of the whole bin — with the usual `Comparable`/distinct-hash caveat.

> [!warning] Collision ≠ second `put` overwrites
> A chain exists because hashes (or indexes) collided **and** `equals` was false. Same `hashCode` plus `equals` true is one mapping. Another trap: calling every shared bucket a `hashCode` collision — the chain can hold mixed hashes, and `get` can skip `equals` on those nodes.

> [!tip] Interview answer
> **In `HashMap`, a hash collision in a bucket chain is extra `Node`s on `next` in one slot: unequal keys that hashed to the same index. `equals` decides append versus replace. The walk checks stored hash first. Same `hashCode` stays together forever; different hashes in one chain may split on resize. Java 8+ can treeify a long chain.**
