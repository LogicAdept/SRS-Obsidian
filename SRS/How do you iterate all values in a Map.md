<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #Java/Collections/Iteration #SRS

# How do you iterate all values in a `Map`?

> [!abstract] Short answer
> **Walk `values()`.** That is a `Collection<V>` **view**, not a `Set`: values need not be unique. Enhanced `for`, `iterator()`, `forEach`, or a stream. Removing from the view (or from its iterator) removes **one corresponding mapping**. `add` / `addAll` are unsupported. `Map.forEach` walks **entries**; use it when you also need the key.

## `values()` is the API

```java
for (V value : map.values()) {
    use(value);
}
```

**Listing 1.** The usual loop. `values()` implements `Iterable`, so the enhanced `for` is an iterator over that view. [[What is the Map interface in Java]]

The `Map` contract: the collection is backed by the map, so changes to the map show in the collection and vice versa. If the map is modified while iteration is in progress **except** through that iterator’s `remove`, the results are **undefined**. Removal via `Iterator.remove`, `Collection.remove`, `removeAll`, `retainAll`, and `clear` deletes the corresponding mapping. `add` and `addAll` throw `UnsupportedOperationException`.

Unlike `entrySet()`, there is no `setValue` exception in that rule: you are iterating values, not `Map.Entry`. To replace a value in place, walk entries or call `put` / `replace` with the key.

```d2
direction: down
map: "Map<K,V>" {
  width: 180
  height: 55
  style.fill: "#e3f2fd"
}
vs: "values()\nCollection<V> view" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
loop: "for / iterator / forEach / stream" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
rm: "view.remove(v)\n→ one mapping gone" {
  width: 250
  height: 70
  style.fill: "#ffe0b2"
}

map -> vs -> loop
vs -> rm
```

**Fig. 1.** Duplicate values stay; that is why the return type is `Collection`, not `Set`. `Collection.remove` drops a **single** instance (`Objects.equals`), hence one mapping.

```java
map.values().forEach(this::use);           // Consumer<V>, Java 8
map.values().iterator();                   // Iterator.remove OK
map.values().stream().filter(...);         // snapshot only if you collect
map.forEach((k, v) -> use(v));             // still visits every entry
```

**Listing 2.** `Collection.forEach` vs `Map.forEach`. The latter is a `BiConsumer` over mappings (default: walk `entrySet()`). Keys: [[How do you iterate all keys in a Map]]. Pairs: [[How do you iterate all key value pairs in a Map]].

`HashMap` documents that iterating a collection view costs **capacity plus size** (empty buckets are visited). `LinkedHashMap` walks the encounter list, time ~ size. `TreeMap` yields values in **key** sort order, not value order. On a `SequencedMap` (Java 21), `values()` still reflects encounter order even though the return type is a plain `Collection`; `sequencedValues()` is the `SequencedCollection` view (`reversed()` for reverse). [[What are LinkedHashMap ordering guarantees]]

## What not to use for “all values”

`Hashtable.elements()` returns an `Enumeration` that is **not** fail-fast; structural mutation during enumeration is undefined. Prefer `values()` even on `Hashtable`. [[How would you explain drawbacks of the legacy Hashtable class]]

Do not loop `keySet()` and `get` just to collect values — that is a second lookup per key. Do not assume `values()` is a `Set` or that `contains` / `remove` are cheap: they scan mappings (`containsValue` is linear in typical hash maps).

Typical hash-map iterators are fail-fast on a **best-effort** basis (`ConcurrentModificationException`). That is not a lock. `ConcurrentHashMap` iterators do not throw CME and reflect some state at or after creation; they are for one thread.

> [!warning] `values()` is not a snapshot
> `new ArrayList<>(map.values())` copies. The view itself still sees later `put`/`remove`. Adding to `values()` does not insert a mapping — there is no key. Two keys with equal values produce two elements. `sequencedValues()` inherits `equals` / `hashCode` from `Object`; do not treat the view as a content-equal `List`.

> [!tip] Interview answer
> **Iterate `map.values()`. It is a live `Collection` of values (duplicates allowed): enhanced `for`, iterator, or `forEach`. Removals write through one mapping at a time; `add` does not work. Order follows the map (`HashMap` unspecified, `TreeMap` by key, `LinkedHashMap` encounter). `Map.forEach` walks entries, not values-only.**
