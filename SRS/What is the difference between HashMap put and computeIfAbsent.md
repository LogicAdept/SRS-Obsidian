<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Versions/8 #SRS

# What is the difference between `HashMap` `put` and `computeIfAbsent`?

> [!abstract] Short answer
> **`put` always writes the value you pass.** **`computeIfAbsent` (Java 8) writes only if the key is missing or mapped to `null`, and only if the function returns non-null.** `put` returns the **previous** value. `computeIfAbsent` returns the **current** value (old non-null, or newly computed). A `null` from the function means “do not record.” `HashMap` is not atomic about this; do not mutate the map inside the function.

## When a mapping is written

```text
put(k, v)                  always associate k → v (replace if present)
                           v may be null; that is a real mapping

computeIfAbsent(k, f)      if get(k) is a non-null value → leave it, skip f
                           else v = f.apply(k)
                             if v != null → store it
                             if v == null → store nothing (absent stays absent;
                                            a null mapping stays null)
```

**Listing 1.** `Map` contracts (Java SE 21). `computeIfAbsent` treats “mapped to `null`” like “absent” for the purpose of running `f`.

```d2
direction: down
key: "key k" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
present: "non-null value already?" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
keep: "computeIfAbsent: return it\nput: overwrite anyway" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
fn: "f.apply(k)" {
  width: 200
  height: 50
  style.fill: "#ffe0b2"
}
store: "store if f returned non-null" {
  width: 280
  height: 70
  style.fill: "#ffe0b2"
}

key -> present
present -> keep: yes
present -> fn: no
fn -> store
```

**Fig. 1.** `put` does not look at “already have a useful value.” `computeIfAbsent` does.

```java
map.put(k, expensive(k));                 // runs every time; replaces
map.computeIfAbsent(k, this::expensive);  // runs only on miss / null value
```

**Listing 2.** Memoization is the documented `computeIfAbsent` use. The javadoc example `computeIfAbsent(key, k -> new HashSet<>()).add(v)` is a multi-map: create the set once, then `add`.

Return values:

* `put` → previous `V`, or `null` if there was no mapping (or it was `null`).
* `computeIfAbsent` → existing non-null `V`, or the computed `V`, or `null` if `f` returned `null`.

`putIfAbsent` is the third method: associate a **ready** value if absent-or-null, without a function. It is not `put`.

## What OpenJDK `HashMap` actually does

`put` → `putVal(..., onlyIfAbsent=false)`. Existing key: `e.value = value`. New key: `newNode`, maybe resize / treeify. [[How does HashMap access elements internally]] is the matching `getNode` path. [[How many new objects may be allocated when inserting a new entry into HashMap]] is allocation on the new-key branch.

`computeIfAbsent`: find the node. If it exists **and** `value != null`, return that value (`afterNodeAccess` — empty on `HashMap`). Otherwise call `f`. If `modCount` changed, throw `ConcurrentModificationException` (best-effort; `HashMap` documents this). If `f` returns `null`, return `null` without inserting. If there was a null mapping, a non-null result **fills that node**; a new key is inserted like `put`.

The mapping function must not modify this map. `NullPointerException` if `f` is `null`. `HashMap` does **not** promise that `f` runs at most once under races; that sentence is for `ConcurrentMap` implementations that document it.

> [!warning] `put` is not “create if missing”
> `put(k, new ArrayList<>())` allocates a list even when `k` is already present, then throws the old list away. `computeIfAbsent` skips `f` when a non-null value exists. The other trap: `put(k, null)` stores null; `computeIfAbsent` that returns `null` stores nothing, so a later `containsKey` stays false. `get` returning `null` still cannot tell those two `put` cases apart.

> [!tip] Interview answer
> **`put` always writes and returns the previous value. `computeIfAbsent` (Java 8) runs a function only when the key is absent or mapped to `null`, stores the result only if it is non-null, and returns the value now in the map. Use it to build the value once. Do not modify the `HashMap` inside the function; it is not a concurrent atomic compute.**
