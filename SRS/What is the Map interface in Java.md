<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #SRS

# What is the `Map` interface in Java?

> [!abstract] Short answer
> **A Collections Framework type that maps keys to values: no duplicate keys, each key maps to at most one value.** It replaced the obsolete `Dictionary` class. It does **not** extend `Collection`. You look at contents through three backed views: `keySet()`, `values()`, `entrySet()`. Key sameness is `equals` (implementations may skip `equals` when hashes already differ). Since 1.2. [[What is the main purpose of the Map interface]]

## Unique keys, not a `Collection`

`Collection` is a group of elements. `Map` is a set of key–value mappings. `put` of an equal key replaces the value; it does not add a second mapping. Values may repeat. [[Can keys be duplicated in a Java Map]]

```text
Map
  not a Collection (no add of a lone element)
  three views: keySet  values  entrySet
  optional mutators → UnsupportedOperationException
  key equals; map equals = same entrySet
```

**Listing 1.** Shape of `java.util.Map` (Java SE 21). `Dictionary` is obsolete; new code implements `Map`.

```d2
direction: down
m: "Map<K,V>" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
ks: "keySet()\nSet<K>" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
vs: "values()\nCollection<V>" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
es: "entrySet()\nSet<Map.Entry<K,V>>" {
  width: 240
  height: 80
  style.fill: "#ffe0b2"
}
m -> ks
m -> vs
m -> es
```

**Fig. 1.** Views are backed by the map: change the map, the view changes, and allowed view removes write through. `add` on those views is unsupported.

Order of a map is the order of iterators on those views. `HashMap` does not guarantee it. `TreeMap` does (sorted). Maps with a defined encounter order are generally `SequencedMap` (Java 21), e.g. `LinkedHashMap`. [[What is a HashMap]]

## What the interface requires of implementations

Destructive methods are optional: an unmodifiable map throws `UnsupportedOperationException`. Implementations may forbid `null` keys or values (`NullPointerException` / `ClassCastException`). Querying an ineligible key may throw or return `false`.

Mutable keys: behavior is **unspecified** if you change a key so `equals` comparisons change while it is in the map. A map must not contain itself as a key. Containing itself as a value is allowed but `equals` / `hashCode` of that map are no longer well defined. [[What requirements apply to keys used in a HashMap]]

Two maps are `equals` when both are maps and `entrySet()`s are equal — same mappings, **independent of encounter order**. `Map.hashCode` is the sum of entry hash codes.

`Map.of` / `ofEntries` / `copyOf` (Java 9) build unmodifiable, value-based maps: no `null`s, duplicate keys at creation are `IllegalArgumentException`, iteration order unspecified. Mutable keys or values can still make even those maps look inconsistent.

> [!warning] “Map is a Collection of entries”
> `entrySet()` is a `Set`. `Map` itself is not a `Collection`. You cannot pass a `Map` where a `Collection` is required without taking a view.

> [!tip] Interview answer
> **`Map` maps unique keys to values. It is in the Collections Framework but does not extend `Collection`. Access is `get`/`put` plus three backed views. Key identity is `equals`. Order is an implementation property; `SequencedMap` is the Java 21 subtype that promises encounter order.**
