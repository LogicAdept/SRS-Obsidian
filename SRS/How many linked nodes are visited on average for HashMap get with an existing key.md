<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #DSA/Complexity #Math/Probability #SRS

# How many linked nodes are visited on average for `HashMap` `get` with an existing key?

> [!abstract] Short answer
> **A small constant, typically one.** The javadoc does not publish a node count. It only promises constant-time `get` if hashes spread keys among buckets. OpenJDK models bin occupancy, with random `hashCode`s and default load factor 0.75, as Poisson with mean about 0.5: most buckets are empty or hold a single node. A successful `get` always looks at least at the matching node; that is usually the first node in the bin.

## The spec gives a cost, not a length

`HashMap` documents constant-time `get` **assuming** the hash function disperses elements among buckets. A higher load factor is documented to raise lookup cost; the default 0.75 is the usual time/space tradeoff. That is expected time, not “always one comparison” and not a worst-case bound. [[Does HashMap guarantee its documented lookup time complexity]] is that assumption. [[What is the algorithmic complexity of HashMap operations]] is the rest of the cost table.

A present key is found by `getNode`: mix, index one slot, test the first node, then walk `next` until identity or `equals` hits. [[What is the worst case time complexity of get on a HashMap when the key is present]] is when that walk is the whole map. Average-case is the other end of the same loop.

```d2
direction: down
get: "get(existing key)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
one: "First node matches\n1 visit (typical)" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
few: "Short chain\n2–3 visits (uncommon)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
bad: "One overloaded bin\nΘ(n) (pathological hash)" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}

get -> one
get -> few
get -> bad
```

**Fig. 1.** Average under dispersed hashes is the left two boxes. The right box is a broken `hashCode`, not the mean.

## What OpenJDK expects of a random hash

Implementation notes treat well-distributed hashes as Poisson occupancy with parameter about **0.5** on average at the default 0.75 resize threshold (occupancy sits between “just doubled” and “about to double”). Ignoring resize jitter, the chance a bin has length k is `exp(-0.5) * 0.5^k / k!`:

```text
k = 0   0.6065
k = 1   0.3033
k = 2   0.0758
k = 3   0.0126
k = 8   6e-8     (more than 8: < 1 in 10 million)
```

**Listing 1.** Bin-length frequencies from the OpenJDK `HashMap` notes. These are occupancy of a **random bucket**, not a theorem in the public API.

A successful `get` does not sample empty buckets: the key’s bin has at least that node. Still, length 1 is the common occupied case, length 2 is already under 8% of all buckets, and length 8 is why tree bins are described as rare when user hashes are decent. [[How does HashMap handle collisions]] is the tree backstop, not the average path.

Load factor still moves the mean: pack more entries per bucket and the chain you walk on a hit gets longer. That is the javadoc’s “higher load factor, higher lookup cost.” It is not a license to quote a single magic number such as 1.5 as if `HashMap` specified it.

> [!warning] Average is not a contract
> Do not answer “exactly one” or “always O(1).” Do not answer “n/2.” The public text is “constant-time assuming dispersion.” The Poisson table is why, with a normal `hashCode`, you almost never walk a long list. Identical `hashCode`s make the average story false: [[What happens to HashMap if all keys share the same hashCode]].

> [!tip] Interview answer
> **On a successful `get`, `HashMap` visits the nodes of one bin until `equals` hits. With dispersed hashes that is typically the first node, sometimes a short chain. OpenJDK models default occupancy as Poisson with mean about 0.5, so bins of length 8 are negligible. The javadoc never states a node count—only expected constant time when hashes spread. Worst case remains a single colliding list of size n.**
