<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #Java/Collections/Map/HashMap #Java/JVM/Memory/References #SRS

# How does `WeakHashMap` work?

> [!abstract] Short answer
> **A `HashMap`-shaped table whose keys are weak.** The mapping does not keep the key alive. When the key is no longer strongly or softly reachable, the collector can clear that `WeakReference`, enqueue it, and a later `get`/`put` **polls** the queue and drops the row. Values stay strong. Null key and null values are allowed. It is a registry, not an LRU cache.

## Weak keys in a normal hash table

`WeakHashMap` is a hash-table `Map`. An entry is automatically removed when its key is no longer in ordinary use: presence of the mapping does **not** stop the collector from making that key finalizable and reclaiming it. After the key is discarded, the entry is effectively gone. Capacity and load factor work like `HashMap` (defaults 16 and 0.75). Not synchronized. Since 1.2. [[What is WeakHashMap used for]]

Keys live as referents of weak references (each `Entry` *is* a `WeakReference` registered on a `ReferenceQueue`). Weak refs are for canonicalizing mappings that must not pin keys. Soft refs are the cache tool. An object is weakly reachable only if it is **neither strongly nor softly** reachable. A leftover `SoftReference` to the key still keeps `get` working; “no strong refs” is incomplete. [[Why not build a SoftHashMap on SoftReferences the way WeakHashMap uses WeakReferences]]

```d2
direction: down
strong: "strong / soft ref\nelsewhere" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
key: "Key" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
map: "WeakHashMap\nEntry extends WeakReference\nstrong value" {
  width: 300
  height: 90
  style.fill: "#ffe0b2"
}
q: "ReferenceQueue\npoll on access" {
  width: 260
  height: 70
  style.fill: "#c8e6c9"
}

strong -> key
map -> key: weak
map -> q: enqueue after GC
```

**Fig. 1.** Drop ordinary reachability and the GC may enqueue the entry. The table unlinks it on the next access, not at the assignment `key = null`.

```java
WeakHashMap<Object, String> w = new WeakHashMap<>();
Object k = new Object();
w.put(k, "sidecar");
w.get(k);     // hit while k is strongly reachable
k = null;
// after GC: WeakReference cleared and enqueued
// next get/put/size polls the queue and drops the row
w.size();     // snapshot — may still count a stale entry until expunge
```

**Listing 1.** Conceptual lifecycle. `System.gc()` is not part of the contract; timing is the collector’s. [[How does WeakHashMap use ReferenceQueue]] [[How do you attach extra data to an object with WeakHashMap]]

Lookup still uses `equals` (null-safe), with an identity fast path on the referent. The class is aimed at keys whose `equals` is `==`, so a discarded instance cannot be recreated as a surprise miss. Recreatable keys such as `String` still “work,” and then automatic removal looks like a Heisenbug.

Values are **strong**. A value that points back at its key (or a cycle through other entries) pins that key forever. Documented workaround: store `new WeakReference(value)` and unwrap on `get`. The **null key** is a static sentinel, so that row is **not** weakly collected. Null values are fine. [[Does WeakHashMap allow null keys or values]] [[What happens to a WeakHashMap entry when the last strong reference to the key is dropped]]

`size()` / `isEmpty()` are snapshots and may count entries the GC has already logically discarded but the map has not expunged. Iterators are fail-fast for your structural mods; the collector can still look like a silent other thread (`containsKey` true then false with no mutator).

This is not `LinkedHashMap.removeEldestEntry` and not `IdentityHashMap` (strong table, `==` keys). [[How do you build a cache with invalidation using LinkedHashMap]] [[Can IdentityHashMap be used as a cache]]

> [!warning] “Ordinary use means I called System.gc()”
> “No longer in ordinary use” is the class javadoc, not a method you invoke. Enqueue happens after the collector decides the key is weakly reachable. Expunge happens on a later map access (`poll`, not blocking `remove`). Soft reachability delays that. Do not treat `WeakHashMap` as LRU.

> [!tip] Interview answer
> **`WeakHashMap` is a hash table that holds keys with weak references so the GC can drop mappings whose keys are otherwise unused.** Values stay strong, so they must not point back at the key. It polls a `ReferenceQueue` on access to expunge stale entries. Null keys/values are allowed; the null key is not weakly collected. It is a non-pinning registry, not a cache.
