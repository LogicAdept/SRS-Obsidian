<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Immutability #SRS

# How can you lose a value in a `HashMap`?

> [!abstract] Short answer
> **Four different “losses.”** An equal key **replaces** the old value. `remove` / `clear` / a remapping function that returns `null` **deletes** the mapping. Mutating a key’s `equals` / `hashCode` state can make `get` miss while the node **still sits in the table**. `get` returning `null` can also mean the map **stores** `null`. The value object is not wiped from the heap in the unreachable-key case. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]]

## Replaced or removed

`put` associates a value with a key. If the map already contained that key (`containsKey` would be true), the old value is **replaced**. `putAll` does the same per key. There is at most one mapping per equal key. [[Can a HashMap contain two equal keys at the same time]]

`remove` drops the mapping if present. `clear` drops all. `compute`, `computeIfPresent`, and `merge` **remove** the mapping when the remapping function returns `null` (`computeIfPresent` only runs when the current value is non-null).

```java
map.put("k", "old");
map.put("k", "new");           // "old" replaced; get("k") is "new"
map.remove("k");               // mapping gone
map.put("k", "v");
map.compute("k", (key, v) -> null); // mapping removed
```

**Listing 1.** Conceptual API loss: replace vs delete. `HashMap` permits a `null` value; that is not deletion.

```d2
direction: down
q: "get(k) is null or unexpected" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
rep: "put/putAll replaced\nan equal key" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
del: "remove / clear /\ncompute* / merge → null" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
miss: "equals/hashCode of the\nstored key changed, or\nlookup key is not equal" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
nul: "mapping exists, value is null\nuse containsKey" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
q -> rep
q -> del
q -> miss
q -> nul
```

**Fig. 1.** Interview “lost” usually means one of these four, not a `HashMap` leak.

## Unreachable, not deleted

`Map` leaves behavior **unspecified** if you change a stored key in a way that affects `equals`. `HashMap` keeps the insertion-time hash on the node; a later `get` hashes the key’s **current** state and typically never matches. `size()` and iteration still see the entry. Restore is not a supported API. Use a stable key. [[What requirements apply to keys used in a HashMap]]

A lookup key that is not `equals` to the stored key (second `byte[]`, broken `hashCode`) is the same symptom with a different cause: `get` is specified to return `null` when no key `k` satisfies `(key==null ? k==null : key.equals(k))`. [[Can you use byte array as key in Java HashMap]]

## `null` is not absence

`HashMap.get`: returns the mapped value, or `null` if there is no mapping. A return of `null` **does not necessarily** mean there is no mapping; the key may map to `null`. Distinguish with `containsKey`. `remove` has the same ambiguity on its return value.

> [!warning] Unsynchronized threads
> `HashMap` is not synchronized. Concurrent structural mutation is not a specified way to “lose” a value; the result is undefined. Use a lock, `synchronizedMap`, or `ConcurrentHashMap`. [[Is java.util.HashMap thread safe]]

> [!tip] Interview answer
> **Replace (`put` of an equal key), delete (`remove` / remapping `null`), unreachable after mutating the key’s `equals` state, or `get`/`null` while `containsKey` is true. Iteration still finds a mapping that `get` misses after key mutation. The heap object is not gone.**
