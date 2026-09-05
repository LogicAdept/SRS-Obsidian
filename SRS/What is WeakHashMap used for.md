<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #Java/Collections/Map/HashMap #Java/JVM/Memory/References #Java/HashCodeEquals #SRS

# What is `WeakHashMap` used for?

> [!abstract] Short answer
> **A hash map whose keys are weak: the mapping does not keep the key alive.** When the key is no longer in ordinary use, the GC can discard it and the entry disappears. Use it when the table must not pin objects you only want while something else still references them. It is not an LRU cache and not a drop-in `HashMap`. Values are ordinary strong references.

## The map must not be the last strong ref to the key

`WeakHashMap` is a hash table `Map` with **weak keys**. Presence of a mapping does not stop the collector from making that key finalizable and reclaiming it. After the key is discarded, the entry is effectively gone. Null key and null values are allowed. Capacity and load factor work like `HashMap`. Unsynchronized, same as most collection classes.

```d2
direction: down
out: "Ordinary strong refs\nelsewhere" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
key: "Key object" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
map: "WeakHashMap\nweak ref to key\nstrong ref to value" {
  width: 280
  height: 90
  style.fill: "#ffe0b2"
}

out -> key
map -> key: weak
```

**Fig. 1.** Drop the last ordinary reference and the GC may clear the key. The map will then behave as if that mapping was removed.

The javadoc’s intended keys are objects whose `equals` is identity (`==`). Once discarded, that key cannot be recreated, so you will not later `get` a look-alike and wonder why the entry vanished. It still **works** with recreatable keys such as `String`; automatic removal then looks like a Heisenbug. [[What is the difference between HashMap and WeakHashMap]] is the `Map` invariant list (`size` can shrink with no mutator).

Each key is the referent of a weak reference inside the map. The key is removed only after **all** weak references to it, inside and outside the map, have been cleared.

## Values can pin keys

Implementation note: values are **strong**. A value that refers back to its own key (directly or through other map entries) keeps that key alive, so the entry never drops. If values need not be pinned by the map, the documented workaround is to store `new WeakReference(value)` and unwrap on `get`.

`size()` / `isEmpty()` are snapshots and may still count entries the GC has already logically discarded but the map has not yet expunged.

This is not `LinkedHashMap.removeEldestEntry`. That cache evicts on **size** (and LRU if access-ordered). `WeakHashMap` evicts when the **key** is unreachable. [[How do you build a cache with invalidation using LinkedHashMap]] is the size policy. There is no JDK `SoftHashMap`; [[Why not build a SoftHashMap on SoftReferences the way WeakHashMap uses WeakReferences]] is that gap. JEP 180 did not treeify `WeakHashMap` bins.

> [!warning] “Use it as a cache for Strings”
> Interned or newly allocated equal `String`s can miss after the previous copy was collected. The class is aimed at identity keys. Also not thread-safe: even a locked instance can lose entries because the collector looks like a silent other thread.

> [!tip] Interview answer
> **`WeakHashMap` holds keys with weak references so the GC can drop mappings whose keys are otherwise unused. Values stay strong, so they must not point back at the key. Prefer identity-equals keys. It is a non-pinning table, not an LRU cache and not a `HashMap` with stable `size()`.**
