<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Java/Collections/Map/HashMap #Java/Versions/21 #SRS

# What are `LinkedHashMap` ordering guarantees?

> [!abstract] Short answer
> **Encounter order is well-defined: insertion-order by default, or access-order if you pass `accessOrder == true`.** Eldest (least recently inserted, or least recently accessed) is first; youngest is last. Re-`put` of an existing key does **not** change insertion-order. `HashMap` still makes no order promise. Iteration follows the list, in O(size).

## Insertion-order is the default

Ordinary constructors and `new LinkedHashMap<>(m)` build an **insertion-ordered** map. The doubly-linked list is the encounter order of iteration. A key is “reinserted” when `put` runs and `containsKey` was already true: the value updates, the node stays where it was. [[How do HashMap, TreeMap, and LinkedHashMap work at a high level]] is that list (`head` eldest, `tail` youngest).

```d2
direction: down
mode: "accessOrder flag" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
ins: "false: insertion-order\nput of a new key → tail\nre-put stays put" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
acc: "true: access-order\nget / put / … → move to tail" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}

mode -> ins
mode -> acc
```

**Fig. 1.** One boolean in `LinkedHashMap(int, float, boolean)`. Default constructors are insertion-order (`false`).

That is **not** sort order. `TreeMap` orders by `compare`. [[How do HashMap, TreeMap, and LinkedHashMap differ at a high level]] is the three-way choice.

## Access-order is opt-in

`LinkedHashMap(capacity, loadFactor, true)` orders entries from least-recently accessed to most-recently accessed. The javadoc lists what counts as an access (if the entry exists afterward): `put`, `putIfAbsent`, `get`, `getOrDefault`, `compute`, `computeIfAbsent`, `computeIfPresent`, `merge`. `replace` counts only when the value is actually replaced. `putAll` counts once per mapping from the source iterator.

**Not** an access: `containsKey`, `containsValue`, walking `keySet` / `values` / `entrySet`, and (Java 21) explicit positioning such as `putFirst` / `putLast` / `lastEntry`. Those positioning methods still **move** the mapping; they just are not classified as accesses.

In access-order, `get` is a **structural modification** (iteration order changes). In insertion-order, replacing a value is not. Fail-fast iterators care about that distinction.

`removeEldestEntry` sees the current eldest. That is the LRU hook. [[How do you build a cache with invalidation using LinkedHashMap]] is the policy.

## Java 21: `SequencedMap`

`putFirst` / `putLast` put the mapping first or last in encounter order, relocating it if the key was already present. `reversed()` is the opposite encounter order (youngest first). These do not replace the insertion- versus access-order flag; they move individual entries.

> [!warning] “`put` refreshes insertion-order”
> It does not. Only a **new** key goes to the tail in insertion-order. Use access-order (or `putLast`) if you want “this key was just used, so it is youngest.” `containsKey` will not refresh access-order. Copying `new LinkedHashMap<>(hashMap)` snapshots whatever order that `HashMap` happened to iterate—not insertion into the original.

> [!tip] Interview answer
> **Default `LinkedHashMap` iterates in insertion-order: eldest first, re-`put` does not move the key. Pass `accessOrder true` for LRU-style last-access order; then `get`/`put` (and the listed compute/merge methods) move the entry, and `get` is a structural modification. Views and `containsKey` do not count as accesses. `HashMap` still has unspecified order.**
