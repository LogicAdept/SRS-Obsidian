<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #Java/Collections/Iteration #SRS

# How do you iterate all key value pairs in a `Map`?

> [!abstract] Short answer
> **Walk `entrySet()`, or call `Map.forEach`.** `entrySet()` is a `Set<Map.Entry<K,V>>` **view**: each entry is a key–value pair (`getKey` / `getValue`). The iterator’s `remove` deletes the mapping; `Entry.setValue` is allowed during that iteration. `add` on the set is not. `forEach(BiConsumer)` is the Java 8 default over the same entries. Do not loop `keySet()` and `get` — that is a second lookup per key.

## `entrySet()` is the pairs view

```java
for (Map.Entry<K, V> e : map.entrySet()) {
    use(e.getKey(), e.getValue());
}
```

**Listing 1.** Enhanced `for` over the backed set. [[What is the Map interface in Java]]

`Map.entrySet` javadoc: the set is backed by the map. If the map is modified while iteration is in progress, results are **undefined**, except through that iterator’s `remove` **or** `setValue` on an entry the iterator returned. Removal via `Iterator.remove`, `Set.remove`, `removeAll`, `retainAll`, and `clear` drops the mapping. `add` / `addAll` are unsupported.

```d2
direction: down
map: "Map<K,V>" {
  width: 180
  height: 55
  style.fill: "#e3f2fd"
}
es: "entrySet()\nSet<Map.Entry>" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
e: "Entry\ngetKey / getValue / setValue" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
fe: "map.forEach((k, v) -> …)\nJava 8 default: same walk" {
  width: 300
  height: 80
  style.fill: "#ffe0b2"
}

map -> es -> e
map -> fe
```

**Fig. 1.** Pairs are `Map.Entry` objects from the view, or a `BiConsumer` that never materializes an `Entry` in your code.

```java
map.forEach((k, v) -> use(k, v));

map.replaceAll((k, v) -> transform(k, v)); // setValue on each entry
```

**Listing 2.** Default `forEach` is `for (Entry e : entrySet()) action.accept(e.getKey(), e.getValue())`. Default `replaceAll` calls `setValue` on each entry. Unmodifiable maps throw `UnsupportedOperationException` on `setValue`.

Keys-only: [[How do you iterate all keys in a Map]]. Values-only: [[How do you iterate all values in a Map]].

On a `SequencedMap` (Java 21), `entrySet()` iteration is still encounter order; `sequencedEntrySet()` is the `SequencedSet` view. `HashMap` view iteration is capacity plus size; `LinkedHashMap` is ~ size along the list; `TreeMap` is key order. [[What are LinkedHashMap ordering guarantees]]

Entries obtained while iterating typically stay connected to the map **for that iteration**. `setValue` then updates the live mapping. Snapshot methods such as `firstEntry()` / `lastEntry()` on `SequencedMap` do **not** support `setValue`. `Map.entry(k, v)` (Java 9) is an unmodifiable pair for `ofEntries`, not a view into an existing map.

## What not to do

```java
for (K k : map.keySet()) {
    use(k, map.get(k)); // extra lookup; racy if the map mutates
}
```

**Listing 3.** Anti-pattern. `entrySet` already has the value.

`Hashtable` has no separate “pairs enumeration” you should prefer over `entrySet()`. Fail-fast `ConcurrentModificationException` on `HashMap` views is best-effort, not a lock. `ConcurrentHashMap` iterators do not throw CME and must be used by one thread; they may see a mix of updates.

> [!warning] `Entry` is not a detached DTO
> Holding an `Entry` after the loop and calling `setValue` later is unspecified. `Map.Entry` from `entrySet()` is not `Map.entry()`. Adding an `Entry` to `entrySet()` does not insert a mapping. Copy if you need a snapshot: `new ArrayList<>(map.entrySet())` still holds live entries from some implementations — copy key and value instead.

> [!tip] Interview answer
> **Iterate `map.entrySet()` for `Map.Entry` pairs, or `map.forEach((k, v) -> …)` since Java 8. Removals and `setValue` during that iterator are the supported in-flight edits. Do not `keySet` plus `get`. Order follows the map; the view is live, not a copy.**
