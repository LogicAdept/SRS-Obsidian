<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/TreeMap #Java/HashCodeEquals #Java/Versions/8 #SRS

# What is the algorithmic complexity of `HashMap` operations?

> [!abstract] Short answer
> **Key lookup and update are documented as constant-time only if hashes spread keys across buckets.** `get`, `put`, `containsKey`, and `remove` follow that sentence. A `put` that rehashes rebuilds the table. Iteration is proportional to **capacity plus size**. `containsValue` is a scan, not a hash lookup. Worst case in one overloaded bin is linear in that bin; Java 8+ may make it logarithmic when hashes differ or keys are `Comparable`. None of this is an unconditional O(1) guarantee. See [[Does HashMap guarantee its documented lookup time complexity]].

## What Java SE actually states

```text
get, put
  constant-time, assuming hashes disperse among buckets

iteration (keySet / values / entrySet)
  time ~ capacity + size

many identical hashCode() values
  slows any hash table; Comparable keys may break ties

rehash
  when size > loadFactor * capacity
  table rebuilt to about twice the buckets
```

**Listing 1.** Costs taken from the `HashMap` class javadoc (Java SE 21). `containsKey` and `remove` use the same hashed node search as `get` / `put`; they are not given a separate bound.

`TreeMap` is the contrast: **guaranteed** log(n) for `containsKey`, `get`, `put`, and `remove`. [[What is the time complexity of lookup by key in a TreeMap]] is that wording.

```d2
direction: down
key: "Lookup by key\n(get / containsKey / remove / put)" {
  width: 320
  height: 80
  style.fill: "#e3f2fd"
}
val: "Lookup by value\n(containsValue)" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
it: "Iterate a view" {
  width: 240
  height: 70
  style.fill: "#ffe0b2"
}
hash: "One bin + equals\ncheap if hashes spread" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
scanV: "Walk every mapping" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
scanT: "Walk every bucket\nthen every node" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}

key -> hash
val -> scanV
it -> scanT
```

**Fig. 1.** Only key-based methods use the hash table as a hash table. Value search and iteration do not.

## Expected, resize, and worst bin

When hashes disperse, a key operation indexes one bucket and compares a short chain. That is the “constant-time” claim. [[How many linked nodes are visited on average for HashMap get with an existing key]] is the typical chain length. Load factor still matters: a higher factor packs more entries per bucket and raises lookup cost; the documented default is 0.75.

If that `put` pushes `size` past the threshold, the implementation **rehashes**. That call is not constant-time; it rebuilds internal structures. [[How and when does HashMap resize its buckets]] is the growth rule.

If many keys share a `hashCode()` or only an index, one bin holds them. Then a `get` hit or miss walks that chain. Java 8+ may treeify a crowded bin (capacity at least 64, enough nodes); OpenJDK states O(log n) in the bin when hashes are distinct or keys are orderable. That is implementation, and JEP 180 did not change the public spec. [[What happens to HashMap if all keys share the same hashCode]] and [[What is the worst case time complexity of get on a HashMap when the key is absent]] are those bins. [[How does HashMap handle collisions]] is chaining versus trees.

## Operations that are not hashed lookups

`Map.containsValue` is documented as probably linear in map size for most implementations. `HashMap` overrides it and walks every bucket’s `next` chain, so an empty-but-large table still costs capacity. Do not quote the `get` sentence here.

OpenJDK `HashMap` keeps a `size` field, so `size()` and `isEmpty()` do not scan. `clear()` nulls every slot of the current table, so it scales with **capacity**, not only with size.

> [!warning] “Everything is O(1)”
> Common false answers: `containsValue` is O(1); iteration is O(size); every `put` is O(1) including resize; Java 8 made worst-case `get` O(1) or unconditionally O(log n). The javadoc never said “guaranteed O(1),” and it never said “amortized O(1).” Those are textbook glosses, not the spec.

> [!tip] Interview answer
> **`get`/`put`/`containsKey`/`remove` are expected constant-time if `hashCode` spreads keys; a rehashing `put` and a colliding bin are the exceptions. Iteration is O(capacity + size). `containsValue` scans. `TreeMap` is the map with a guaranteed log(n) lookup. Java 8 trees are a backstop for a bad bin, not a new contract.**
