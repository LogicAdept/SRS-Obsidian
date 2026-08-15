<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/TreeMap #Java/HashCodeEquals  #Java/Versions/8 #SRS

# Does `HashMap` guarantee its documented lookup time complexity?

> [!abstract] Short answer
> **No.** The class documents constant-time `get` and `put` only **assuming** the hash function disperses keys among buckets. That is a precondition, not an unconditional bound. Contrast `TreeMap`, which documents **guaranteed** log(n) cost for the same operations. A bad `hashCode`, a crowded bin, or a `put` that rehashes the table can make a lookup or insert far more expensive than O(1).

## What the specification actually says

```text
HashMap:  constant-time get/put, assuming hashes disperse among buckets
TreeMap:  guaranteed log(n) for containsKey, get, put, remove
```

**Listing 1.** Paraphrase of the Java SE 21 class javadocs. `HashMap` uses “provides … assuming.” `TreeMap` uses “guaranteed.” The `Map` interface does not promise a complexity for `get`.

`get` and `containsKey` share the same node search. Neither method’s own javadoc adds a tighter bound. The constant-time sentence is class-level prose, not a worst-case theorem.

```d2
direction: down
doc: "Documented constant-time get/put" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
ok: "Hashes spread across buckets" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
bad: "Many keys, one bin\n(same hashCode or same index)" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
fast: "Typical lookup stays cheap" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
slow: "Walk a list or tree bin\nnot O(1)" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}

doc -> ok -> fast
doc -> bad -> slow
```

**Fig. 1.** The documented time holds when the assumption holds. It is not a guarantee that every `get` is O(1).

The same page already names the failure mode: many keys with the same `hashCode()` slow any hash table. [[What happens to HashMap if all keys share the same hashCode]] is that bin. `Comparable` keys **may** be used to break ties; that is optional mitigation, not a new complexity contract. [[How does HashMap handle collisions]] is chaining and Java 8+ tree bins.

## Other documented costs that are not O(1)

Iteration over key, value, or entry views takes time proportional to **capacity plus size**, not size alone. A large empty table makes iteration slower even when lookups are fine.

When `size` exceeds load factor times capacity, the table is rehashed: internal structures are rebuilt, about twice as many buckets. That `put` does work proportional to the live entries (and the old table), not constant work. Choosing initial capacity so that this never happens is documented advice, not a promise that every `put` is O(1).

`containsValue` is a different operation. `Map` already warns that it will probably take linear time for most implementations. Do not cite `get`’s sentence for scanning values.

[[What is the algorithmic complexity of HashMap operations]] collects expected versus worst-case figures. [[What is the time complexity of lookup by key in a TreeMap]] is the guaranteed log(n) counterpart.

> [!warning] Java 8 did not rewrite the contract
> Tree bins can improve a crowded bucket from a linear scan toward O(log n) when hashes differ or keys are `Comparable`. That change was an implementation (JEP 180 explicitly left the specification alone). Interview answers that say “`HashMap` is guaranteed O(1)” or “since Java 8 it is guaranteed O(log n)” are both stronger than the javadoc. [[What is the worst case time complexity of get on a HashMap when the key is absent]] is the miss that still walks the whole overloaded bin.

> [!tip] Interview answer
> **No. `HashMap` documents constant-time lookup only if hashes spread keys across buckets. That assumption can fail, and a rehashing `put` is not constant-time either. `TreeMap` is the map that actually says “guaranteed log(n).” Java 8 trees are an implementation backstop, not a new public guarantee.**
