<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Caching #SRS

# Can `LinkedHashMap` fully implement an LRU cache?

> [!abstract] Short answer
> **Yes for the JDK’s LRU recipe: access-order plus `removeEldestEntry`.** `get` / `put` (and the other listed access methods) move that entry to youngest; eldest is least-recently accessed. The dump’s “no, because re-`put` does not move the entry” is **insertion-order**. It is not a complete cache product: `containsKey` is not an access, eviction runs only after a **new** insert, and the map is unsynchronized.

## Access-order is LRU; insertion-order is not

Default constructors are **insertion-order**. Eldest is least recently inserted. Re-`put` of a live key does **not** change encounter order. That mode plus `removeEldestEntry` is a size-capped FIFO, not LRU. [[What are LinkedHashMap ordering guarantees]]

The three-argument constructor with `accessOrder == true` orders by last access, least-recently accessed first. The class javadoc calls that well-suited to LRU caches. Accesses are `put`, `putIfAbsent`, `get`, `getOrDefault`, `compute`, `computeIfAbsent`, `computeIfPresent`, and `merge` (if the entry exists afterward). `putAll` accesses each copied mapping. `replace` accesses only if the value actually changes. **No other methods** are accesses: not `containsKey`, not `containsValue`, not iteration over `keySet` / `values` / `entrySet`. `putFirst` / `putLast` / `lastEntry` position explicitly and do not count as accesses.

```d2
direction: down
mode: "ordering mode" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
ins: "insertion-order (default)\nre-put leaves order\neldest = oldest insert" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
acc: "access-order (true)\nget/put move to youngest\neldest = LRU" {
  width: 300
  height: 90
  style.fill: "#c8e6c9"
}

mode -> ins
mode -> acc
```

**Fig. 1.** Same class, two encounter orders. Only `accessOrder=true` is LRU. Re-`put` is an access in that mode.

```java
LinkedHashMap<String, Integer> insertion = new LinkedHashMap<>();
insertion.put("a", 1);
insertion.put("b", 1);
insertion.put("a", 2); // still a then b — re-put does not move

LinkedHashMap<String, Integer> lru = new LinkedHashMap<>(16, 0.75f, true);
lru.put("a", 1);
lru.put("b", 1);
lru.put("a", 2); // b then a — put is an access
lru.get("b");    // a then b
lru.containsKey("a"); // still a then b — not an access
```

**Listing 1.** Conceptual: insertion-order re-`put` is the dump’s “cannot move” rule. Access-order `put` / `get` do move. `containsKey` does not.

Override `removeEldestEntry`, not `removeEldestEntries`. `put` and `putAll` call it **after inserting a new entry**. Return `true` to drop eldest. Default implementation returns `false` (never evicts). The documented 100-entry sample is `return size() > MAX_ENTRIES` after insert. Replacing the value of an existing key is not a new insert, so it does not consult the method — size does not grow; in access-order the entry still moves. [[How do you build a cache with invalidation using LinkedHashMap]]

Java 21 also lets you inspect or drop eldest with `firstEntry` / `pollFirstEntry` instead of the hook. Still unsynchronized: wrap with `Collections.synchronizedMap` if needed. [[Can IdentityHashMap be used as a cache]] is the opposite mistake (strong table, no eviction).

> [!warning] “Re-put does not move, so LinkedHashMap cannot be LRU”
> That sentence is true of **insertion-order** and false of **access-order**, where `put` is listed as an access. The real holes in “fully”: `containsKey` will not refresh LRU; view iteration will not; eviction is on **new** `put`/`putAll`, not on `get`; `replace` refreshes only when the value changes. Default `LinkedHashMap` is not access-order and never evicts.

> [!tip] Interview answer
> **Yes, if you construct it with `accessOrder=true` and override `removeEldestEntry` so size stays bounded — that is the JDK LRU cache.** Re-`put` not moving is the default insertion-order rule, not access-order. It is still not a full cache: `containsKey` is not an access, eviction runs only after a new insert, and it is not thread-safe.
