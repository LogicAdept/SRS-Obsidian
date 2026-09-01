<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/HashMap #Java/HashCodeEquals #SRS

# Why can `IdentityHashMap` be faster than `HashMap`?

> [!abstract] Short answer
> **It never calls the key’s `hashCode()` or `equals()`.** Lookup uses `System.identityHashCode` and `==`. That skips work when those methods are expensive. The table is also a linear-probe array of alternating keys and values, which the javadoc says is often faster than `HashMap`’s chaining — for many JREs and operation mixes, not as a guarantee.

## What `HashMap` pays for that identity maps skip

`HashMap.get` / `put` hash with the key’s `hashCode()`, then match with `equals` (null-safe). A `String`, a value object, or a custom key with a deep `equals` does that work on every probe in the bucket. [[What is the internal structure of HashMap]] [[When does a hashCode collision occur in a HashMap]]

`IdentityHashMap` javadoc: two keys are the same iff `k1 == k2`. Basic ops are constant-time if **`System.identityHashCode`** spreads. That function returns the *default* `Object.hashCode()` even when the class overrides `hashCode()`; null’s identity hash is 0. No user `hashCode()`, no user `equals()`. [[How does IdentityHashMap decide whether two keys are the same]] [[Does IdentityHashMap use the hashCode method]] [[Does overriding equals change IdentityHashMap lookup]]

```d2
direction: down
key: "lookup key" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
hm: "HashMap\nkey.hashCode() → bucket\nthen equals" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
id: "IdentityHashMap\nidentityHashCode → slot\nthen ==" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}

key -> hm
key -> id
```

**Fig. 1.** Same “hash then compare” shape. Identity maps hash and compare *references*, not value equality.

Implementation note on `IdentityHashMap` (Java SE 21): simple **linear-probe** table, keys at even indexes and values at odd ones (better locality than two arrays). “For many Java implementations and operation mixes, this class will yield better performance than `HashMap`, which uses chaining rather than linear-probing.” That is the second, table-shape reason — independent of a slow `equals`. [[How does IdentityHashMap resolve collisions]]

```java
final class SlowKey {
    final byte[] payload;
    SlowKey(byte[] payload) { this.payload = payload; }

    @Override public boolean equals(Object o) {
        return o instanceof SlowKey s && java.util.Arrays.equals(payload, s.payload);
    }

    @Override public int hashCode() {
        return java.util.Arrays.hashCode(payload); // scans the array
    }
}

Map<SlowKey, String> valueEq = new HashMap<>();
Map<SlowKey, String> byRef = new IdentityHashMap<>();
SlowKey k = new SlowKey(new byte[10_000]);
valueEq.put(k, "v");
byRef.put(k, "v");
valueEq.get(k); // hashCode + equals walk the array
byRef.get(k);   // identityHashCode + ==
```

**Listing 1.** Conceptual: `HashMap` pays the key’s value hash and equality. `IdentityHashMap` does not. If you needed *value* equality, this map is the wrong tool — two `equal` but distinct `SlowKey`s are two keys. [[Can two equal String objects both be keys in an IdentityHashMap]]

When the key type does **not** override `hashCode` / `equals`, `HashMap` already hashes with `Object.hashCode()` (identity-based) and compares with `==`. The remaining gap is probe vs chain, plus locality of the interleaved array — “can be faster,” not “always is.”

> [!warning] Faster is not a reason to replace `HashMap`
> This class is **not** a general-purpose `Map`. It intentionally violates the `Map` contract that keys compare with `equals`. Use it when you *need* reference equality (object-graph / proxy tables). Ordinary `String` / value keys belong in `HashMap`. Iteration cost tracks **bucket count** (expected maximum size), and a too-large table or clustered identity hashes can lose the win. “Sometimes” is the honest FAQ. [[Does IdentityHashMap violate the Map contract]] [[What is IdentityHashMap for]] [[What is the difference between HashMap and IdentityHashMap]]

> [!tip] Interview answer
> **`IdentityHashMap` can be faster because it hashes with `System.identityHashCode` and compares keys with `==`, so it never runs a custom `hashCode` or `equals`. It also linear-probes an interleaved key/value array, which the JDK says often beats `HashMap` chaining. That is “can,” not “use it instead of HashMap”: it is not a general-purpose map and it violates `equals`-based `Map` semantics.**
