<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #Java/HashCodeEquals #SRS

# Can keys be duplicated in a Java `Map`?

> [!abstract] Short answer
> **No. A `Map` cannot contain duplicate keys: each key maps to at most one value.** A second `put` of a key that `containsKey` would accept **replaces** the value; `size` does not grow. Values may repeat. Distinct objects still collide as one key when `equals` is true. Factories `Map.of` / `ofEntries` reject duplicates with `IllegalArgumentException` instead of replacing. Hash-table `put`: [[Can a HashMap contain two equal keys at the same time]].

## Duplicate means equal, not `==`

`get` / `containsKey` / `remove` are specified with `Objects.equals` (null-safe `equals`) and “at most one such mapping.” `put` replaces when the map already contained that key. Two `new String("a")` instances are one key. Two `byte[]` with the same bytes are **two** keys, because array `equals` is identity. [[What constraints apply to keys in a Java Map]]

```java
map.put("a", 1);
map.put("a", 2);           // replaces; size still 1; get("a") is 2
map.put("b", 2);           // different key; values may duplicate
Map.of("a", 1, "a", 2);    // IllegalArgumentException
```

**Listing 1.** Conceptual `put` vs `Map.of`. Replacement is the mutable-map rule; factories fail fast at creation.

```d2
direction: down
put: "put(k, v)" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
q: "containsKey(k)?" {
  width: 200
  height: 55
  style.fill: "#fff3e0"
}
rep: "replace value\nsize unchanged" {
  width: 220
  height: 70
  style.fill: "#ffe0b2"
}
add: "new mapping\nsize + 1" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
put -> q
q -> rep: yes
q -> add: no
```

**Fig. 1.** There is never a second mapping for an equal key. `keySet()` is a `Set`.

## When it looks like duplicates

`IdentityHashMap` uses `==`. Two `equals` objects can be two keys. The class javadoc says that violates the general `Map` contract. [[What is IdentityHashMap for]]

A `SortedMap` treats `compareTo` / `compare == 0` as the same key. If that disagrees with `equals`, the tree is well-defined but **fails** the `Map` contract (`Comparable` / `SortedMap` javadocs). You can observe one mapping where `equals` would have wanted two, or the reverse.

A broken `equals` / `hashCode` pair can make a `HashMap` store two keys that `equals` considers equal, because the table filters by stored hash first. That is a contract violation, not a supported “duplicate keys” mode. [[How can you lose a value in a HashMap]]

> [!warning] “Two objects, so two keys”
> `Map` uniqueness is `equals` (or `==` in `IdentityHashMap`, or compare in a sorted map). `size() == 2` after two `put`s means the implementation did **not** treat those keys as the same.

> [!tip] Interview answer
> **No duplicate keys: `put` replaces. Values can duplicate. Equal objects are one key. `Map.of` throws on duplicate keys. `IdentityHashMap` and an inconsistent `TreeMap` ordering are the documented ways uniqueness diverges from `equals`.**
