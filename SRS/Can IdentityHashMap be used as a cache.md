<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Caching #SRS

# Can `IdentityHashMap` be used as a cache?

> [!abstract] Short answer
> **Not as a memory-sensitive or LRU cache.** It is a `Map` with `==` keys, so you *can* store computed values, but unused keys stay reachable: `put` writes the key and value into a strong `Object[]` table and never drops them. `WeakHashMap` is the JDK map that releases unused keys. `LinkedHashMap` in access-order with `removeEldestEntry` is the documented LRU cache.

## Strong table, no eviction

`IdentityHashMap` is for identity-sensitive tables: a serializer or deep-copy node map, or a per-instance proxy table. It is **not** a general-purpose `Map`. Nothing in that job description is cache eviction. [[What is IdentityHashMap for]]

`put` stores the key and value as adjacent slots of `table` (`tab[i] = k; tab[i + 1] = value`). Those array slots are ordinary strong references. Drop every other pointer to the key and the map still pins it. If the mapping count exceeds the expected maximum size, the table **grows** (rehash); it does not drop eldest or unreachable entries.

`WeakHashMap` is the contrast. An entry is removed when its key is no longer in ordinary use: the mapping does not prevent the collector from reclaiming the key. Keys live as weak-reference referents, not as strong array slots. That is still not LRU and not a `SoftReference` cache. [[What is WeakHashMap used for]] [[Why not build a SoftHashMap on SoftReferences the way WeakHashMap uses WeakReferences]]

```d2
direction: down
drop: "Caller drops last\nordinary ref to key" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
ihm: "IdentityHashMap\nstrong table[i] = key\nentry stays" {
  width: 280
  height: 90
  style.fill: "#ffcdd2"
}
whm: "WeakHashMap\nweak ref to key\nGC may drop the entry" {
  width: 280
  height: 90
  style.fill: "#c8e6c9"
}
lru: "LinkedHashMap\naccess-order +\nremoveEldestEntry" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}

drop -> ihm
drop -> whm
drop -> lru: size policy,\nnot GC
```

**Fig. 1.** Same “I no longer use this key” event. Identity maps keep the mapping. Weak maps may lose it. LRU maps evict on **size**, not on unreachability.

```java
IdentityHashMap<Object, String> byRef = new IdentityHashMap<>();
WeakHashMap<Object, String> weak = new WeakHashMap<>();

Object k1 = new Object();
Object k2 = new Object();
byRef.put(k1, "memo");
weak.put(k2, "memo");

k1 = null;
k2 = null;
// byRef still reaches its key through table[]; size stays 1
// after GC, weak may lose its mapping (timing unspecified)
```

**Listing 1.** Conceptual: identity maps pin; weak maps do not. Do not treat the `WeakHashMap` side as a cache either — the collector is not an eviction policy.

Bounded caches belong on `LinkedHashMap`. The access-order constructor is documented as well-suited to LRU caches; override `removeEldestEntry` so `put` / `putAll` drop the eldest after a new insert. [[How do you build a cache with invalidation using LinkedHashMap]] `IdentityHashMap` has no `removeEldestEntry`, no access order, and no iteration-order guarantee.

> [!warning] “IdentityHashMap as a unique-object cache”
> “Not a cache” means **no GC eviction and no size cap**, not “never store a computed value.” A node table that must keep every seen instance *should* pin. A cache that should free memory when callers drop keys will leak: the map is the last strong ref. Value-equal look-alikes (`new String("a")`) miss; lookup is `==`. Not synchronized.

> [!tip] Interview answer
> **Do not use `IdentityHashMap` as a cache.** It holds keys and values with strong references in its table and never auto-evicts, so unused entries leak. For GC-dropped keys use `WeakHashMap`; for an LRU size cap use access-ordered `LinkedHashMap` and `removeEldestEntry`. `IdentityHashMap` is an identity node or proxy table, not a cache.
