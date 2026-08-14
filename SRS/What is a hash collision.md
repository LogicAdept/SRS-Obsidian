<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #DSA/Algorithms/Hashing #SRS

# What is a hash collision?

> [!abstract] Short answer
> A **hash collision** is two **distinct** inputs that a hash function maps to the **same** hash value. In Java that usually means two objects that are not `equals` yet return the same `int` from `hashCode()`. Hash tables still store both: they use the integer only to choose a bucket, then identity or `equals` to tell keys apart. A collision is expected, not a JVM bug and not a proof of equality.

## The general event

A hash function compresses a large key space into a smaller range of integers. By the pigeonhole principle, once more distinct keys exist than hash values, some pair **must** collide. `hashCode` returns `int`, so there are only 2³² possible results. [[Why can two unequal objects share the same hashCode value]] is that bound plus the contract.

`Object.hashCode` requires equal objects to share a hash. It does **not** require unequal objects to differ. Distinct hashes are recommended because they usually make hash tables faster.

```d2
direction: down
a: "Key A" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
b: "Key B\n(not equals A)" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
h: "hash function\nsame int" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
bin: "Same hash-table bucket\n(until equals decides)" {
  width: 260
  height: 80
  style.fill: "#ffe0b2"
}

a -> h
b -> h
h -> bin
```

**Fig. 1.** Collision is equal hashes for unequal keys. Membership is still `equals`, not the integer.

`"Aa"` and `"BB"` are a specified `String` example: different text, `hashCode` `2112`.

## In Java hash tables the word is used more loosely

`Hashtable` documents an open hash table: on a “hash collision”, one bucket holds several entries and they are searched sequentially. That sentence is about **sharing a bucket**, which can also happen when `hashCode()` values differ but the index `(n - 1) & hash` matches. [[When does a hashCode collision occur in a HashMap]] keeps those two events apart. [[What are hash collisions in HashMap bucket chains]] is the chain itself.

`HashMap` still treats a matching hash as a candidate set, not as equality. Many keys with the same `hashCode()` slow any hash table. Java 8+ may treeify a crowded bin; that does not redefine collision. [[How does HashMap handle collisions]] is chaining and trees.

> [!warning] Collision is not equality, and not cryptography
> Same hash does not mean `equals` is true; `put` overwrites only when `equals` is true. Cryptographic “collision” (two messages, same digest, attack on a hash algorithm) is a different claim. Interview answers that stop at “two keys in one `HashMap` bucket” mix a `hashCode` collision with a mere index collision.

> [!tip] Interview answer
> **A hash collision is two unequal keys with the same hash value. In Java, `hashCode` is allowed to collide; hash tables put those keys in one bucket and separate them with `equals`. Different `hashCode` values can still share a `HashMap` index, which is a bucket collision, not the same event.**
