<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/IdentityHashMap #Java/HashCodeEquals #SRS

# What is the difference between `HashMap` and `IdentityHashMap`?

> [!abstract] Short answer
> `HashMap` compares keys with **`equals`** (after `hashCode`). `IdentityHashMap` compares keys **and values** with **`==`** and hashes with **`System.identityHashCode`**. It implements `Map` but **intentionally violates** the `Map` contract that equality is `equals`. Use it only when you must distinguish references that would be `equals`. `HashMap` is the general-purpose map.

## Equality and hashing

```text
HashMap
  k1 and k2 same key iff  (k1==null ? k2==null : k1.equals(k2))
  bucket from key.hashCode() (then mixed)

IdentityHashMap
  k1 and k2 same key iff  (k1==k2)
  bucket from System.identityHashCode(key)
```

**Listing 1.** Documented key tests. `IdentityHashMap` also uses reference equality for values in `containsValue` / entry equality.

Two `String` copies with the same characters are one `HashMap` key and two `IdentityHashMap` keys. Overriding `equals`/`hashCode` on your class does **not** change `IdentityHashMap`. `System.identityHashCode` still reports the default hash after an override. [[How are hashCode and equals implemented in java.lang.Object]] is that default.

The class javadoc states it is **not** a general-purpose `Map`: `Map` mandates `equals`. Typical uses are a node table for serialization or deep copy (must not merge distinct objects that happen to be `equals`) and proxy tables. [[What is IdentityHashMap for]] is that niche.

```d2
direction: down
k: "Two instances\nequals true, != references" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
hm: "HashMap\none mapping" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
ihm: "IdentityHashMap\ntwo mappings" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

k -> hm
k -> ihm
```

**Fig. 1.** Same value, different references: `HashMap` coalesces, `IdentityHashMap` does not.

## Structure and tuning

`HashMap` is a bucket table with chaining and, in Java 8+, optional tree bins. You tune **initial capacity** and **load factor** (default 0.75). Iteration is proportional to capacity plus size.

An **implementation note** (not the `Map` contract) describes `IdentityHashMap` as a **linear-probe** table: one array of alternating keys and values. You tune **expected maximum size** (default 21), not a load factor. Iteration is proportional to the number of buckets. Both allow `null` keys and values; neither is synchronized; neither promises iteration order.

Constant-time `get`/`put` is assumed when hashes disperse: user `hashCode` for `HashMap`, identity hash for `IdentityHashMap`. [[Does HashMap guarantee its documented lookup time complexity]] is that assumption on the `equals` map.

Entry `hashCode` in `IdentityHashMap` is `identityHashCode(key) XOR identityHashCode(value)`, matching its `==` entry equality. `HashMap` entries use `Objects.hashCode` on key and value.

> [!warning] Do not swap them for “speed”
> The implementation note that linear probing can be faster for some mixes is not a license to drop `equals`. If you need value keys, `HashMap` is the contract you want. If you need reference keys, `IdentityHashMap` is the rare tool. Putting value objects into `IdentityHashMap` and expecting `get(new Key(id))` to hit is the usual bug.

> [!tip] Interview answer
> **`HashMap` is value equality: `hashCode` then `equals`. `IdentityHashMap` is reference equality: `==` and `identityHashCode`, and it admits it violates the `Map` contract. Use the first by default. Use the second for identity-sensitive tables (graph copy, proxies). Both allow null; they differ in comparison, hashing, and table shape (chains versus linear probe).**
