<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Immutability #SRS

# What requirements apply to keys used in a `HashMap`?

> [!abstract] Short answer
> A key must have a **consistent `equals` and `hashCode`**, and that pair must stay **stable while the object is in the map**. `HashMap` allows one `null` key. Many identical hashes slow the table. The `Map` contract leaves behavior unspecified if you mutate a key in an `equals`-relevant way. Arrays and other identity-`equals` types only look up with the **same reference**.

## What `HashMap` asks of a key

`containsKey` / `get` treat keys `k1` and `k2` as the same when `(k1==null ? k2==null : k1.equals(k2))`, after using `hashCode` to pick a bin. Implementations may skip `equals` when hashes already differ. Therefore:

1. **Contract pair.** Equal keys must have equal hashes. Override both or neither. [[Why should equals and hashCode be overridden together]]
2. **Stability in the map.** Great care if the key is mutable: behavior is not specified if you change it so that `equals` comparisons change. A special case: a map must not contain itself as a key. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]]
3. **Dispersion.** Many keys with the same `hashCode()` slow any hash table. `Comparable` keys may help tree bins break ties; that is optional mitigation. [[What happens to HashMap if all keys share the same hashCode]]
4. **`null`.** `HashMap` permits the `null` key (mixed hash `0`). `Hashtable` does not.

```text
legal:   immutable value, equals + hashCode on those fields
legal:   identity Object (lookup only with the same reference)
legal:   null  (one mapping)
unsafe:  mutate equals/hashCode fields after put
poor:    byte[] / T[] as keys (identity equals, mutable contents)
forbidden as key: the map itself
```

**Listing 1.** Practical key policy. [[Why is a byte array a poor or unsafe choice for a HashMap key]] is the array case.

```d2
direction: down
k: "Candidate key" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
eq: "equals / hashCode\nstable for the stay in the map" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
spread: "Hashes not all identical" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
map: "HashMap put / get" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}

k -> eq -> map
k -> spread -> map
```

**Fig. 1.** Correctness is the contract plus stability. Speed is dispersion.

`HashMap` is not synchronized. Concurrent structural mutation is a threading requirement, not a key-type rule. Iteration order is unspecified.

Values have no `hashCode` requirement for `get`; `containsValue` scans with `equals` on values. Do not confuse key rules with value rules.

> [!warning] “Immutable record, so any fields are fine”
> Records hash **all components**. If a component is a mutable list, mutating the list still changes `equals`/`hashCode`. Shallow immutability of the record is not deep immutability of the key. Prefer components that are themselves values.

> [!tip] Interview answer
> **Keys need a stable `equals`/`hashCode` pair for as long as they remain in the map. `HashMap` allows `null` and uses `equals` after the hash. Mutating equality state while the key is stored is unspecified. Identical hashes work but are slow. Arrays compare by identity, so they are poor keys unless you always pass the same instance.**
