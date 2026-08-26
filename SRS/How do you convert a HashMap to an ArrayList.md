<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/Map/HashMap #SRS

# How do you convert a `HashMap` to an `ArrayList`?

> [!abstract] Short answer
> **You do not convert the map as one object.** Choose a collection view — `keySet()`, `values()`, or `entrySet()` — then copy it with `new ArrayList<>(…)`. That constructor walks the view’s iterator and builds an independent `List`. A `Map` is not a `Collection`.

## Pick the view, then copy

```d2
direction: down
map: "HashMap<K,V>" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
keys: "keySet()\nSet<K>" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
vals: "values()\nCollection<V>" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
ents: "entrySet()\nSet<Map.Entry<K,V>>" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
list: "new ArrayList<>(view)\nindependent List" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

map -> keys
map -> vals
map -> ents
keys -> list
vals -> list
ents -> list
```

**Fig. 1.** `Map` exposes three views; `ArrayList(Collection)` copies whatever the view’s iterator yields.

```java
Map<String, String> map = new HashMap<>();
map.put("John Kevin", "Average");

List<String> keys = new ArrayList<>(map.keySet());
List<String> values = new ArrayList<>(map.values());
List<Map.Entry<String, String>> entries =
        new ArrayList<>(map.entrySet());
```

**Listing 1.** Standard copy via `ArrayList(Collection)`. Order follows the view iterator — for `HashMap` that order is **unspecified** and may change ([[What is a HashMap]]; use `LinkedHashMap` when encounter order matters).

The views themselves are **backed by the map** (`keySet` / `values` / `entrySet` javadoc): mutating the view can mutate the map. The `ArrayList` constructor materializes a **new list** of the current elements, so later `map.put` / `map.remove` do not change the list’s size or membership. See [[How do you iterate all key value pairs in a Map]] for walking without copying.

> [!warning] Copied `entrySet()` entries may still be tied to the map
> `Map.Entry` javadoc: entries obtained by copying the entry-set into another collection have **unspecified** connection to the backing map — `setValue` may or may not write through, depending on the map implementation. To guarantee a disconnected snapshot (Java 17+), use `Map.Entry.copyOf`. That method rejects null keys/values (`NullPointerException`), so it is a poor fit when the `HashMap` actually stores nulls — copy into your own pair type instead.

```java
List<Map.Entry<String, String>> snapshot = map.entrySet().stream()
        .map(Map.Entry::copyOf)
        .toList(); // unmodifiable List (Java 16+); or collect to ArrayList
```

**Listing 2.** Official-style detached snapshot with `Map.Entry.copyOf` (Java 17+). Requires non-null keys and values.

> [!tip] Interview answer
> **There is no single “map → ArrayList” API.** Copy `keySet()`, `values()`, or `entrySet()` with `new ArrayList<>(view)`. That gives an independent list in the view’s iteration order — unspecified for `HashMap`. If you need entry pairs that cannot affect the map, snapshot with `Map.Entry.copyOf` (Java 17+) or your own type.
