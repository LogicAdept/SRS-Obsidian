<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #Java/HashCodeEquals #SRS

# How does putting and getting values in a `Map` work internally?

> [!abstract] Short answer
> **`Map` has no one table.** `get` / `put` are a **locate, then read or write** contract: the key is the mapping with `Objects.equals(lookup, k)` (implementations may skip `equals` when `hashCode`s already differ). `get` returns that value or `null`. `put` **replaces** if the key is already there, otherwise inserts; it returns the **previous** value. How locate works is the implementation: hash bins, a red-black tree, or `==`.

## The contract, before any bucket

```java
V v = map.get(k);          // v, or null (absent or mapped to null)
V old = map.put(k, value); // previous v, or null; mapping is now value
```

**Listing 1.** `Map` javadoc (Java SE 21). A map contains a mapping for `k` iff `containsKey(k)`. `put` of an equal key does not add a second entry. [[What is the Map interface in Java]]

`get`: if there is a mapping `k → v` with `Objects.equals(key, k)`, return `v`; else `null`. At most one such mapping. If the map allows null values, that `null` is **not** “absent” — use `containsKey`.

`put` is optional (`UnsupportedOperationException` on unmodifiable maps). Ineligible keys/values throw (`NullPointerException`, `ClassCastException`, …). `AbstractMap.put` always throws; `AbstractMap.get` / `containsKey` walk `entrySet()` in **linear** time. Real JDK maps override both.

```d2
direction: down
call: "get(k) / put(k, v)" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
loc: "Locate mapping\nequals (maybe after hash / compare)" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
hit: "Found\nget → value\nput → overwrite, return old" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
miss: "Not found\nget → null\nput → insert, return null" {
  width: 280
  height: 90
  style.fill: "#ffe0b2"
}

call -> loc
loc -> hit
loc -> miss
```

**Fig. 1.** Same two outcomes on every `Map`. The search structure is not part of the interface. Keys: [[What constraints apply to keys in a Java Map]].

## Where implementations actually look

| Type | Locate | On `put` miss |
| --- | --- | --- |
| `HashMap` | mix `hashCode`, one bin, `==` / `equals` (list or tree) | new `Node`; maybe resize / treeify |
| `LinkedHashMap` | same bins | same, plus link at the tail (insertion-order) |
| `TreeMap` | `compareTo` / `Comparator`, red-black, guaranteed log(n) | insert + recolor/rotate |
| `IdentityHashMap` | reference `==`, not `equals` | identity table |

**Listing 2.** Machines, not a second `Map` API. Hash lookup in detail: [[How does HashMap access elements internally]]. Three-way picture: [[How do HashMap, TreeMap, and LinkedHashMap work at a high level]].

`HashMap` `get` is `getNode` then `node.value` (or `null`). `put` is `putVal`: same locate; on a hit, replace the node’s value and return the old one; on a miss, link a node and maybe grow the table. `get` returning `null` still cannot tell “no key” from “null value.”

`TreeMap` does **not** hash on the search path. Two keys with `compare == 0` are the same mapping. Ordering must be consistent with `equals` or the `Map` contract is broken even though the tree is well-defined.

`LinkedHashMap` `get` / `put` still hash. Access-order mode treats a successful `get` as an access (moves the entry). Insertion-order re-`put` only changes the value.

`Hashtable.put` / `get` take the same equals-and-hash path under a **whole-table** lock. `ConcurrentHashMap` does not; it is a different concurrency story.

`putIfAbsent` / `computeIfAbsent` are later `Map` methods that **do not** always write. [[What is the difference between HashMap put and computeIfAbsent]]

> [!warning] `put`’s `null` is as ambiguous as `get`’s
> Both mean “no previous mapping” **or** “was mapped to `null`.” `containsKey` before/after, or `putIfAbsent`, if you need the distinction. Do not assume `AbstractMap.get` is what `HashMap.get` does — that default is a scan of every entry. `containsValue` is the linear scan even on `HashMap`.

> [!tip] Interview answer
> **`get`/`put` locate one mapping by `equals` (hash maps may skip `equals` when hashes differ; `TreeMap` compares; `IdentityHashMap` uses `==`). Hit: `get` returns the value, `put` overwrites it and returns the old value. Miss: `get` returns `null`, `put` inserts. `HashMap` does that in a bin; `TreeMap` in a red-black tree. `null` from `get` or `put` is not automatically “absent.”**
