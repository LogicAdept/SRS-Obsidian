<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Collections/Map/HashMap #Java/Language/Enum #SRS

# How do you create an `EnumMap`?

> [!abstract] Short answer
> **Pass the key enum’s `Class`, or copy another map that can reveal that type.** There is no no-arg constructor. `new EnumMap<>(State.class)` builds an empty map. Copying an `EnumMap` reuses its key type even if it is empty. Copying a plain `Map` requires **at least one** mapping, or you get `IllegalArgumentException`.

## The key type is fixed at construction

All keys must come from a single enum type, specified explicitly or implicitly when the map is created. Internally it is an array; basic ops are constant-time and likely faster than `HashMap`. Iteration is declaration order of the constants. Since 1.5. Not synchronized. [[Why prefer EnumMap when the keys are enum constants]] [[Must EnumMap keys all come from the same enum type]]

Three constructors:

```text
EnumMap(Class<K> keyType)           empty; NPE if keyType is null
EnumMap(EnumMap<K, ? extends V> m)  same key type as m, copy mappings
EnumMap(Map<K, ? extends V> m)      if m is EnumMap → same as above
                                    else m must be non-empty (infer key type)
```

**Listing 1.** Constructor catalog from the `EnumMap` class javadoc (Java SE 21).

```java
enum State { NEW, RUNNING, WAITING, FINISHED }

EnumMap<State, String> empty = new EnumMap<>(State.class);
empty.put(State.RUNNING, "running");
empty.get(State.RUNNING); // "running"
empty.size();             // 1
empty.containsKey(State.NEW); // false

EnumMap<State, String> copy = new EnumMap<>(empty);

Map<State, String> hash = new HashMap<>();
hash.put(State.NEW, "new");
EnumMap<State, String> fromMap = new EnumMap<>(hash);

// new EnumMap<State, String>();           // no such constructor
// new EnumMap<>(new HashMap<State, String>()); // IAE — empty, not an EnumMap
```

**Listing 2.** Conceptual: `Class` token for empty; `EnumMap` copy always; other maps only when they already contain a key so the enum type is known.

```d2
direction: down
need: "need an EnumMap" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
cls: "Class token\nempty map" {
  width: 200
  height: 70
  style.fill: "#c8e6c9"
}
em: "another EnumMap\ncopy, type known" {
  width: 220
  height: 70
  style.fill: "#c8e6c9"
}
map: "plain Map\nmust have ≥1 entry" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

need -> cls
need -> em
need -> map
```

**Fig. 1.** Empty `HashMap` cannot tell `EnumMap` which enum to size the array for.

After construction, `put` / `get` / `size` / `containsKey` are ordinary `Map` operations. `put` throws `NullPointerException` on a null key; null values are allowed. `get` matches keys with `==` (enum constants). Prefer this over `HashMap` when every key is a constant of one enum. [[What is the difference between EnumMap and HashMap]] [[Does EnumMap allow null keys or null values]] [[What special collections exist for Java enums]]

> [!warning] `new EnumMap<>()` or `new EnumMap<>(new HashMap<>())`
> There is no void constructor. The `Class` token is how an **empty** map learns its key type. An empty non-`EnumMap` copy throws `IllegalArgumentException`. Passing a null `Class` or a null source map is `NullPointerException`.

> [!tip] Interview answer
> **Create an `EnumMap` with the key enum’s class, like `new EnumMap<>(State.class)`.** You can also copy another `EnumMap`, or a non-empty `Map` so the key type can be inferred. There is no no-arg constructor. If the keys are one enum, prefer it over `HashMap`.
