<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #Java/Collections/Iteration #SRS

# How do you iterate all keys in a `Map`?

> [!abstract] Short answer
> **Walk `keySet()`.** That is a `Set<K>` **view** backed by the map: enhanced `for`, `iterator()`, `forEach`, or a stream. Removing from the view (or from its iterator) removes the mapping. `add` / `addAll` are unsupported. `Map.forEach` is for **entries** (key and value), not keys alone. Order is the map’s encounter order, if it has one.

## `keySet()` is the API

```java
for (K key : map.keySet()) {
    use(key);
}
```

**Listing 1.** The usual loop. `keySet()` implements `Iterable`, so the enhanced `for` is an iterator over that view. [[What is the Map interface in Java]]

The `Map` contract: the set is backed by the map, so changes to the map show in the set and vice versa. If the map is modified while iteration is in progress **except** through that iterator’s `remove`, the results are **undefined**. Removal via `Iterator.remove`, `Set.remove`, `removeAll`, `retainAll`, and `clear` deletes the corresponding mapping. `add` and `addAll` throw `UnsupportedOperationException`.

```d2
direction: down
map: "Map<K,V>" {
  width: 180
  height: 55
  style.fill: "#e3f2fd"
}
ks: "keySet()\nSet<K> view" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
loop: "for / iterator / forEach / stream" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
rm: "view.remove(k)\n→ map loses k" {
  width: 240
  height: 70
  style.fill: "#ffe0b2"
}

map -> ks -> loop
ks -> rm
```

**Fig. 1.** You do not copy the keys unless you do it yourself. The view writes through.

```java
map.keySet().forEach(this::use);           // Consumer<K>, Java 8
map.keySet().iterator();                   // Iterator.remove OK
map.keySet().stream().filter(...);         // snapshot only if you collect
map.forEach((k, v) -> use(k));             // still visits every entry
```

**Listing 2.** `Set.forEach` vs `Map.forEach`. The latter is a `BiConsumer` over mappings (default: walk `entrySet()`). Use it when you also need the value; for keys only, `keySet()` is the honest view. Pairs: [[How do you iterate all key value pairs in a Map]]. Values: [[How do you iterate all values in a Map]].

`HashMap` documents that iterating a collection view costs **capacity plus size** (empty buckets are visited). `LinkedHashMap` walks the encounter list, time ~ size. `TreeMap` yields keys in sort order. On a `SequencedMap` (Java 21), `keySet()` still reflects encounter order even though the return type is a plain `Set`; `sequencedKeySet()` is the `SequencedSet` view (`reversed()` for reverse). [[What are LinkedHashMap ordering guarantees]]

## What not to use for “all keys”

`Hashtable.keys()` returns an `Enumeration` that is **not** fail-fast; structural mutation during enumeration is undefined. Prefer `keySet()` even on `Hashtable`. [[How would you explain drawbacks of the legacy Hashtable class]]

Do not loop `0 .. size()-1` with a fake index. `Map` is not a `List`. Do not `get` inside a key loop if you already have `entrySet()` — that is a second lookup per key.

Typical hash-map iterators are fail-fast on a **best-effort** basis (`ConcurrentModificationException`). That is not a lock. `ConcurrentHashMap` iterators do not throw CME and reflect some state at or after creation; they are for one thread.

> [!warning] `keySet()` is not a snapshot
> `new HashSet<>(map.keySet())` copies. The view itself still sees later `put`/`remove`. Adding to `keySet()` does not insert a mapping — there is no value. Mutating the map from another thread while you iterate is undefined unless the map’s concurrency story says otherwise.

> [!tip] Interview answer
> **Iterate `map.keySet()`. It is a live `Set` of keys: enhanced `for`, iterator, or `forEach`. Removals write through; `add` does not work. Order follows the map (`HashMap` unspecified, `TreeMap` sorted, `LinkedHashMap` encounter). `Map.forEach` walks entries, not keys-only.**
